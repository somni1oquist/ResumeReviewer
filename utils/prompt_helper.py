import os


PROMPT_DIR = "prompts"
# Load prompts from folder
def load_prompt(file_name, prompts_dir=None):
    """Load prompts from the prompts directory."""
    prompts_dir = f"{prompts_dir or PROMPT_DIR}/{file_name}.txt"
    prompt_content = ""
    if not os.path.exists(prompts_dir):
        raise FileNotFoundError(f"Prompt file '{prompts_dir}' does not exist.")
    
    with open(prompts_dir, "r", encoding="utf-8") as f:
        prompt_content = f.read()
    return prompt_content