import importlib.util
import os
from pathlib import Path


def find_and_import_models(start_path='src/modules'):
    base_path = Path(start_path).absolute()
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = Path(root) / file
                module_name = file_path.relative_to(base_path.parent).with_suffix('').as_posix().replace('/', '.').replace('\\', '.')
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
