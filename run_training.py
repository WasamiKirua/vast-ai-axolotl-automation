from colorama import Fore, Style
from time import sleep
import os
import wandb

HF_TOKEN = ""
WANDB_TOKEN = ""
VASTAI_KEY = ""
YAML_FILE = "fft-1.6b.yaml"
YAML_PATH = f"examples/stablelm-2/1.6b/"
TARGET_TAG = 'axolotl-stablelm'

print(f"{Fore.CYAN}Installing colorama python pkg{Style.RESET_ALL}\n")
os.system("pip install colorama")

print(f"{Fore.CYAN}Setting Huggingface Token{Style.RESET_ALL}\n")
os.system(f"huggingface-cli login --token {HF_TOKEN}")

print(f"{Fore.CYAN}Wandb Login{Style.RESET_ALL}\n")
wandb.login(key = WANDB_TOKEN)

print(f"{Fore.CYAN}Preprocessing Datasets{Style.RESET_ALL}\n")
os.system(f'CUDA_VISIBLE_DEVICES="" python -m axolotl.cli.preprocess {YAML_PATH}{YAML_FILE}')

print(f"{Fore.CYAN}Running training{Style.RESET_ALL}\n")
os.system(f"accelerate launch -m axolotl.cli.train {YAML_PATH}{YAML_FILE}")
sleep(120)

print(f"{Fore.GREEN}Done !{Style.RESET_ALL}\n")


print(f"{Fore.GREEN}Instance infos:{Style.RESET_ALL}\n")
with open("infos.json", "r") as f:
    data = json.load(f)

    # Extract the desired fields
    extracted_data = []
    for instance in data:
        instance_info = {
            "instance_id": instance["id"],
            "public_ip": instance["public_ipaddr"],
            "ssh_host": instance["ssh_host"],
            "ssh_port": instance["direct_port_start"],
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
            print(f"{Fore.CYAN}Setting Vast.ai api-key{Style.RESET_ALL}\n")
            os.system(f"vastai set api-key {VASTAI_KEY}")

            print(f"{Fore.RED}Destroying instance{Style.RESET_ALL}\n")
            os.system(f"vastai destroy instance {instance['instance_id']}")
