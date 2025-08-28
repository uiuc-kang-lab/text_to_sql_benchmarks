from pathlib import Path
from typing import Dict

TEMPLATE_DIR = Path("alphasql/templates")

TEMPLATE_DICT = {}

for template_file in TEMPLATE_DIR.glob("*.txt"):
    with open(template_file, "r") as f:
        TEMPLATE_DICT[template_file.stem] = f.read()

def get_prompt(template_name: str, template_args: Dict[str, str]) -> str:
    template = TEMPLATE_DICT[template_name]
    return template.format(**template_args)
