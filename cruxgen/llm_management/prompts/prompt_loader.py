from pathlib import Path

def load_and_format_prompt(file_path: str, **kwargs) -> str:
   template = Path(file_path).read_text().strip()
   return template.format(**kwargs)