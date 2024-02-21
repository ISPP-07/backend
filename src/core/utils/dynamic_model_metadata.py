import importlib.util
from pathlib import Path


def find_and_import_models(start_path='src/modules'):
    base_path = Path(start_path)
    for path in base_path.rglob('*'):
        if path.is_file() and path.name == 'model.py':
            import_path = path.relative_to(Path('src')).with_suffix(
                '').as_posix().replace('/', '.')
            spec = importlib.util.spec_from_file_location(import_path, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
