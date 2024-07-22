"""
batch_selfinstruct_generate.py

run:
python -m lasson_papilledema_generate_instruction generate_instruction_following_data --output_dir ./lasson/ --num_instructions_to_generate 3 --model_name="gpt-3.5-turbo-0125"

or

python -m lasson_papilledema_generate_instruction generate_instruction_following_data --output_dir ./lasson/ --num_instructions_to_generate 3 --model_name="gpt-4o"

"""
import time
import json
import os
import random
import re
import string
from functools import partial
from multiprocessing import Pool

import numpy as np
import tqdm
from rouge_score import rouge_scorer
import lasson_utils

import fire

# lasson, use only output
def encode_prompt(prompt_instructions):
    """Lasson only encode one prompt into a single string."""
    prompt = ""

    for idx, task_dict in enumerate(prompt_instructions):
        (instruction, input, output) = task_dict["instruction"], task_dict["input"], task_dict["output"]
        # instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        # prompt += f"###\n"
        prompt += f"{instruction}\n"
    # prompt += f"###\n"
    return prompt


# lasson, use only output
def post_process_gpt3_response(num_prompt_instructions, response):
    if response is None:
        return []
    raw_outputs = [response["text"]] # lasson modify
    outputs = []
    # lasson gpt output must contain all following words
    whitelist = [
        # "is_referral_letter",
        "is_Papilledema",
        "whole_letter",
        "referral_content",
    ]

    for idx, output_text in enumerate(raw_outputs): # 遍历 raw_outputs
        # lasson, check if output contains all whitelist words
        if not all(find_word_in_string(w, output_text) for w in whitelist):
            print(f"output does not contain all whitelist words, skip: {output_text}")
            continue
        # if the decoding stops due to length, the last example is likely truncated so we discard it
        if idx == len(raw_outputs) - 1 and response["finish_reason"] == "length":
            print(f"output is truncated, skip:")
            continue
        # filter out too short or too long outputs
        if len(output_text.split()) <= 50 or len(output_text.split()) > 300:
            print(f"output is too short or too long, skip: {output_text}")
            continue
        outputs.append({"output": output_text})
    return outputs


def find_word_in_string(w, s):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search(s)


def generate_instruction_following_data(
    output_dir="./lasson/", 
    seed_tasks_path="./seed_tasks.jsonl",
    num_instructions_to_generate=8, # 可设置的 最终要生成的指令数量
    model_name="gpt-3.5-turbo-0125",  # gpt-4o
    num_prompt_instructions=1, # lasson  原始值为3
    request_batch_size=1, # lasson  原始值为5
    temperature=1.0,
    top_p=1.0,
    num_cpus=16,
):
    seed_tasks = [json.loads(l) for l in open(seed_tasks_path, "r")]
    seed_instruction_data = [
        {"instruction": t["instruction"], "input": t["instances"][0]["input"], "output": t["instances"][0]["output"],
         "name": t["name"]} # lasson 加了一个name
        for t in seed_tasks
    ]
    print(f"Loaded {len(seed_instruction_data)} human-written seed instructions_outputs") # lasson modify

    os.makedirs(output_dir, exist_ok=True)
    request_idx = 0
    machine_output_data = []
    if os.path.exists(os.path.join(output_dir, "regen.json")):
        machine_output_data = lasson_utils.jload(os.path.join(output_dir, "regen.json"))
        print(f"Loaded {len(machine_output_data)} machine-generated instructions_outputs")

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False) # lasson modify

    progress_bar = tqdm.tqdm(total=num_instructions_to_generate)
    if machine_output_data:
        progress_bar.update(len(machine_output_data))

    # ------------------ this is where lasson differs from the original code ------------------

    all_outputs = [d["output"] for d in seed_instruction_data] + [
        d["output"] for d in machine_output_data
    ]
    if len(all_outputs) > 12: # lasson add
        all_outputs = all_outputs[:12] # lasson add
    all_output_tokens = [scorer._tokenizer.tokenize(out) for out in all_outputs]

    seed_cnt = 701 # lasson add, since we already have 3 data in regen.json
    while len(machine_output_data) < num_instructions_to_generate:
        request_idx += 1

        batch_inputs = []
        for _ in range(request_batch_size):
            # prompt_instructions = random.sample(seed_instruction_data, num_prompt_instructions)
            prompt_instructions = seed_instruction_data[seed_cnt - 1: seed_cnt] # lasson modify to use all seed_tasks.jsonl
            prompt = encode_prompt(prompt_instructions) # 单条指令
            name_list = [task_dict["name"] for task_dict in prompt_instructions] # lasson add
            batch_inputs.append(prompt)

        decoding_args = lasson_utils.OpenAIDecodingArguments(
            temperature=temperature,
            n=1,
            max_tokens=3072,
            top_p=top_p,
            stop=["\n20", "20.", "20."],
        )
        request_start = time.time()
        results = lasson_utils.openai_completion(
            prompts=batch_inputs,
            model_name=model_name,
            batch_size=request_batch_size,
            decoding_args=decoding_args,
            logit_bias={"50256": -100}
        )
        request_duration = time.time() - request_start

        process_start = time.time()
        after_process_gpt_data = []
        for result in results:
            new_outputs = post_process_gpt3_response(num_prompt_instructions, {"text": result, "finish_reason": "stop"})
            after_process_gpt_data += new_outputs

        total = len(after_process_gpt_data)
        keep = 0
        for index,data_entry in enumerate(after_process_gpt_data): # lasson modify
            new_output_tokens = scorer._tokenizer.tokenize(data_entry["output"])
            with Pool(num_cpus) as p:
                rouge_scores = p.map(
                    partial(rouge_scorer._score_lcs, new_output_tokens),
                    all_output_tokens,
                )
            rouge_scores = [score.fmeasure for score in rouge_scores]
            most_similar_outputs = {
                all_outputs[i]: rouge_scores[i] for i in np.argsort(rouge_scores)[-5:][::-1]
            }
            if max(rouge_scores) > 0.85: # lasson modify, original value is 0.7
                continue
            else:
                keep += 1
            # data_entry["most_similar_outputs"] = most_similar_outputs
            data_entry["avg_similarity_score"] = float(np.mean(rouge_scores))
            data_entry["name"] = name_list[index] # lasson add
            machine_output_data.append(data_entry)

            # we only have 12 data is generate by lasson,
            # from 13, datas are generated by mak, so the other don't need to do similarity check
            if seed_cnt < 12:
                all_outputs.append(data_entry["output"])
                all_output_tokens.append(new_output_tokens)
            progress_bar.update(1)
        process_duration = time.time() - process_start
        print(f"Request {request_idx} took {request_duration:.2f}s, processing took {process_duration:.2f}s")
        print(f"Generated {total} outputs, kept {keep} outputs")
        seed_cnt += 1
        lasson_utils.jdump(machine_output_data, os.path.join(output_dir, "regen.json"))


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
