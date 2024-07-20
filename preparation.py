# Vast.ai reference image
# winglian/axolotl:main-py3.10-cu121-2.1.2
# https://cloud.vast.ai/templates/edit?templateHashId=886c5741378aa948e0e41edeac0caaab

# $ conda create --name axolotl-vastai python=3.10
# $ conda activate axolotl-vastai
# $ pip install -r requirments.txt
# -- Instanciate your instance and wait for availability
# $ python preparation.py
# from the instance: 
    # $ chmod +x run_training.sh
    # $ cd axolotl
    # $ python run_training.py

from colorama import Fore, Style
from time import sleep
import os
import json

VASTAI_KEY = ""
YAML_FILE = "fft-1.6b.yaml"
YAML_PATH = '/workspace/axolotl/examples/stablelm-2/1.6b'
TARGET_TAG = 'axolotl-stablelm'

print(f"{Fore.GREEN}Setting Vast.ai api key{Style.RESET_ALL}\n")
os.system(f"vastai set api-key {VASTAI_KEY}")
print()

print(f"{Fore.GREEN}Getting Instance info{Style.RESET_ALL}\n")
instance_infos = os.system("vastai show instances --raw > infos.json")
print()

print(f"{Fore.GREEN}Instance infos:{Style.RESET_ALL}\n")
with open("infos.json", "r") as f:
    data = json.load(f)

    # Extract the desired fields
    extracted_data = []
    for instance in data:
        ssh_port = instance["ports"]['22/tcp'][0]['HostPort']
        instance_info = {
            "instance_id": instance["id"],
            "public_ip": instance["public_ipaddr"],
            "ssh_host": instance["ssh_host"],
            "ssh_port": ssh_port,
            "label": instance["label"],
            "-----": "-----"
        }
        extracted_data.append(instance_info)

for instance in extracted_data:
    # Print each key-value pair for the current instance
    for key, value in instance.items():
        print(f"{Fore.GREEN}{key.replace('_', ' ').capitalize()}: {value}{Style.RESET_ALL}")
        print()
        if key == "label" and value == TARGET_TAG:
            print("************")
            print(f"{Fore.CYAN}Found {Fore.RED}{instance['label']}{Style.RESET_ALL} target instance !{Style.RESET_ALL}\n")
            print("************")
            print(f"{Fore.CYAN}Copying datasets to instance {instance['label']}{Style.RESET_ALL}\n")
            os.system(f"scp -P {instance['ssh_port']} -o StrictHostKeyChecking=accept-new datasets/*.jsonl root@{instance['public_ip']}:/workspace")
            print()
            print(f"{Fore.CYAN}Copying yaml conf to instance {instance['label']}{Style.RESET_ALL}\n")
            os.system(f"scp -P {instance['ssh_port']} -o StrictHostKeyChecking=accept-new {YAML_FILE} root@{instance['public_ip']}:{YAML_PATH}")
            print()
            print(f"{Fore.CYAN}Copying training script to instance {instance['label']}{Style.RESET_ALL}\n")
            os.system(f"scp -P {instance['ssh_port']} -o StrictHostKeyChecking=accept-new run_training.py root@{instance['public_ip']}:/workspace/axolotl")
            print()
            print(f"{Fore.CYAN}Copying JSON to instance {instance['label']}{Style.RESET_ALL}\n")
            os.system(f"scp -P {instance['ssh_port']} -o StrictHostKeyChecking=accept-new infos.json root@{instance['public_ip']}:/workspace/axolotl")
            print()
            print(f"{Fore.CYAN}Copying deps.sh to instance {instance['label']}{Style.RESET_ALL}\n")
            os.system(f"scp -P {instance['ssh_port']} -o StrictHostKeyChecking=accept-new deps.sh root@{instance['public_ip']}:/workspace/axolotl")
            print()
            print(f"{Fore.CYAN}Connecting to the instance...{Style.RESET_ALL}\n")
            os.system(f"ssh -p {instance['ssh_port']} -o StrictHostKeyChecking=accept-new root@{instance['public_ip']}")
            print()
