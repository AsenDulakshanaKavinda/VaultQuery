


from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

def get_prompt_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(PROMPTS_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )

def render_prompt(template_name: str, **content) -> str:
    template = get_prompt_env().get_template(template_name)
    return template.render(**content).strip()




