# UOB_2024_LLM_EYE_HOSPTITAL
This is the 2024 summer project for "Natural language processing to track ophthalmology referrals to the Bristol Eye Hospital"

# Importance
Never upload any bristol eye hospital data to this repository. If you accidentally upload it, delete it immediately

All the code here belong to UOB project, never send our code to other people. 

# How to launch the web application
Go to the directory lewis_qiyue_web. Then follow the readme file in that folder.

# How to generate training data for this project
Go to the directory weijian_data_generation. Then follow the readme file in that folder.

# How to train the llama2 model
Go to the directory weijian_LLM. And run the finetune_llama2.ipynb file.
Notice, all the operations should be on Amazon Web Service sagemaker

# How to deploy a finetuned llama2 model
Go to the directory lewis_llm. And run the 
```txt
lewis_deploy_finetuned_llama2_7b-f.ipynb
 ```

## Citation

If you use the this framework, cite us.

```bibtex
@misc{UOB_2024_LLM_EYE_HOSPTITAL,
  title={Natural Language Processing to Track Ophthalmology Referrals to the Bristol Eye Hospital},
  author={Weijian Li, Jianzhao Mai, Haoyu Zhu, Lewis Kwok, Li-Hsin Chien, Qiyue Cao},
  year={2024}
}
```