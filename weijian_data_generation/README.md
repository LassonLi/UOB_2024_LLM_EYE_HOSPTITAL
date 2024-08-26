# Brief
This process can be run on a windows system

# install python environment
```bash
pip install -r requirements.txt
```

# generate seed_tasks.jsonl
Open the 
```txt
process_txt_json_into_seed_task.ipynb
 ```
and only run the code in part "使用 mak的700多条数据，生成prompt，放入seed_tasks.jsonl文件里".
Then your final result will be saved in 
```txt
seed_tasks.jsonl
```


# modify the line 118 in lasson_papilledema_generate_instruction.py
```python 
seed_cnt = 701 # lasson add, since we already have 3 data in regen.json
```
you should change the seed_cnt to 0 if you haven't generate any data.
701 means already have 700 data in 
```txt
regen.json
 ```
701 is the next serial number of the data you generate.

# run the following command to generate data
```bash
python -m lasson_papilledema_generate_instruction generate_instruction_following_data --output_dir ./lasson/ --num_instructions_to_generate 699 --model_name="gpt-4o"
```
the output file will be in 
```txt
./lasson/regen.json
 ```

# process the data into the format of llama2 needed
Open the process_txt_json_into_seed_task.ipynb, and go to the part "读取 ./lasson/regen.json"
to the end part "保存 test".

Then the final format data will be in the directory
```txt
 ../weijian_LLM/train_data_735
 ../weijian_LLM/test_data_735
 ```