import importlib.util
import os
from typing import Any, List
from fastapi import FastAPI


class Routers:
    def __init__(
        self,
        app: FastAPI,
        absolute_routes: list,
        prefix: str
    ) -> None:
        self.app = app
        self.absolute_routes = absolute_routes
        self.prefix = prefix

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._create_route_methods()
        return self

    def _create_route_methods(self):
        def add_route_method(router, prefix):
            return self.app.include_router(
                router=router,
                prefix=f'{self.prefix}{prefix}',
            )
        for path in self.absolute_routes:
            module_name = os.path.splitext(os.path.basename(path))[0]
            module_dir = os.path.dirname(path)
            module_spec = importlib.util.spec_from_file_location(
                module_name,
                path
            )
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            route_module = getattr(module, 'router')
            api_module, api_resource = module_dir.split(os.path.sep)[-2:]
            route_method_name = f'{api_module}_{api_resource}_router'
            prefix = f'{api_module}/{api_resource}' if api_resource != 'root' else api_module

            setattr(self, route_method_name, add_route_method)
            getattr(self, route_method_name)(route_module, prefix)


def search_routers(module_path: str) -> List[str]:
    abs_paths = []
    for root, _, files in os.walk(module_path):
        for file in files:
            if file == "router.py":
                abs_path = os.path.abspath(os.path.join(root, file))
                abs_paths.append(abs_path)
    return abs_paths


def get_current_directory(current_file: str) -> str:
    return os.path.dirname(current_file)
