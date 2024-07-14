from colorama import Fore, Style
from time import sleep
import os
import wandb

HF_TOKEN = ""
WANDB_TOKEN = ""
VASTAI_KEY = ""
YAML_FILE = "fft-1.6b.yaml"

print(f"{Fore.CYAN}Installing colorama python pkg{Style.RESET_ALL}\n")
os.system("pip install colorama")

print(f"{Fore.CYAN}Setting Huggingface Token{Style.RESET_ALL}\n")
os.system(f"huggingface-cli login --token {HF_TOKEN}")

print(f"{Fore.CYAN}Wandb Login{Style.RESET_ALL}\n")
wandb.login(key = WANDB_TOKEN)

print(f"{Fore.CYAN}Preprocessing Datasets{Style.RESET_ALL}\n")
os.system(f'CUDA_VISIBLE_DEVICES="" python -m axolotl.cli.preprocess examples/stablelm-2/1.6b/{YAML_FILE}')

print(f"{Fore.CYAN}Running training{Style.RESET_ALL}\n")
os.system(f"accelerate launch -m axolotl.cli.train examples/stablelm-2/1.6b/{YAML_FILE}")
sleep(60)

print(f"{Fore.GREEN}Done !{Style.RESET_ALL}\n")


print(f"{Fore.CYAN}Setting Vast.ai api-key{Style.RESET_ALL}\n")
os.system(f"vastai set api-key {VASTAI_KEY}")
print(os.system("show instances"))

print(f"{Fore.RED}Destroying instance{Style.RESET_ALL}\n")
os.system("vastai destroy instance $CONTAINER_ID")
