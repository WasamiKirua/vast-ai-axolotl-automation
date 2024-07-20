# vast-ai-axolotl-automation

This repo is intended to provide tools to automate the fine tuning of LLM models using Vast.ai

# Update 20.7.24

1) The script supports now instance tagging. You can run the script against the needed instance, seat and enjoy
2) Fixed an issue with the ssh port extraction logic, i was parsing the wrong value for the port

## Notes

With a few changes, if you want you could adapt the code to train your model of choice !

The following docker base image has been selected:

winglian/axolotl:main-py3.10-cu121-2.1.2
[Vast.ai link](https://cloud.vast.ai/templates/edit?templateHashId=886c5741378aa948e0e41edeac0caaab)


## !! Important !!

!! The script destroy instance after completition and push to hub !!

1) I push ALWAYS to HF the full model or the Lora adapters
2) I always ship metrics to Wandb
3) I do not suggest to merge Lora adapters to base it tends to give higher perplexity, load the base in 4bits via Bitsandbytes
   and load the adapters on top instead
4) I love Ollama since it also allows you to load the adapters via Model config file, if you want additional info on how to do that, drop a message I will be happy to help


### Installation

1) move your datasets into datasets folder (I reccomend jsonl)
2) move the axolotl config yaml file into the root repo's folder
3) set the following vars as needed
```
preparation.py:

VASTAI_KEY = "your-key"
YAML_FILE = "fft-1.6b.yaml"
YAML_PATH = '/workspace/axolotl/examples/stablelm-2/1.6b'
TARGET_TAG = 'axolotl-stablelm'

run_training.py:

HF_TOKEN = ""
WANDB_TOKEN = ""
VASTAI_KEY = ""
YAML_FILE = "fft-1.6b.yaml"
YAML_PATH = f"examples/stablelm-2/1.6b/"
TARGET_TAG = 'axolotl-stablelm'
```

```
$ conda create --name axolotl-vastai python=3.10
$ conda activate axolotl-vastai
$ pip install colorama vastai
```
4) Instanciate your instance and wait for availability, ensure to tag the instance with the corresponding value of TARGET_TAG
   
```
$ python preparation.py
```

NOTE: The script will log you in automatically

```
$ cd /workspace/axolotl
$ chmod +x deps.sh
$ ./deps.sh
$ chmod +x run_training.sh
$ python run_training.py
```
 

