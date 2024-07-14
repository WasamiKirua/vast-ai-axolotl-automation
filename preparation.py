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


print(f"{Fore.GREEN}Setting Vast.ai api key{Style.RESET_ALL}\n")
os.system(f"vastai set api-key {VASTAI_KEY}")
print()

print(f"{Fore.GREEN}Getting Instance info{Style.RESET_ALL}\n")
instance_infos = os.system("vastai show instances --raw > infos.json")
print()

print(f"{Fore.GREEN}Instance infos:{Style.RESET_ALL}\n")
with open("infos.json", "r") as f:
    data = json.load(f)
    for instance in data:
        instance_details = {
            "instance_id": instance["id"],
            "public_ip": instance["public_ipaddr"],
            "ssh_host": instance["ssh_host"],
            "ssh_port": instance["ssh_port"]
        }

        # Print each key-value pair for the current instance
        for key, value in instance_details.items():
            print(f"{Fore.GREEN}{key.replace('_', ' ').capitalize()}: {value}{Style.RESET_ALL}")
        print()

print(f"{Fore.CYAN}Copying datasets into /workspace{Style.RESET_ALL}\n")
os.system(f"scp -P {instance_details['ssh_port']} -o StrictHostKeyChecking=accept-new datasets/*.jsonl root@{instance_details['ssh_host']}:/workspace")
print()

print(f"{Fore.CYAN}Copying configuration file into axolotl example's folder{Style.RESET_ALL}\n")
os.system(f"scp -P {instance_details['ssh_port']} -o StrictHostKeyChecking=accept-new {YAML_FILE} root@{instance_details['ssh_host']}:{YAML_PATH}")
print()

print(f"{Fore.CYAN}Copying py training script{Style.RESET_ALL}\n")
os.system(f"scp -P {instance_details['ssh_port']} -o StrictHostKeyChecking=accept-new run_training.py root@{instance_details['ssh_host']}:/workspace/axolotl")
print()

print(f"{Fore.GREEN}Done !{Style.RESET_ALL}\n")
sleep(3)
print()

print(f"{Fore.CYAN}Connecting to the instance...{Style.RESET_ALL}\n")
os.system(f"ssh -p {instance_details['ssh_port']} -o StrictHostKeyChecking=accept-new root@{instance_details['ssh_host']}")
print()
