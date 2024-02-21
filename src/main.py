from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.utils.dynamic_router import Routers
from src.modules.shared.shared import router_urls as core_urls
from src.modules.cyc.cyc import router_urls as cyc_urls
from src.modules.acat.acat import router_urls as acat_urls

from src.core.config import settings


URLS_ENDPOINTS = core_urls + cyc_urls + acat_urls


app = FastAPI(**settings.fastapi_kwargs)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

Routers(
    app=app,
    absolute_routes=URLS_ENDPOINTS,
    prefix=settings.API_STR
)()


@app.get('/')
def root():
    return 'Hello world!'


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)