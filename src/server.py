from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.core.utils.dynamic_router import Routers
from src.core.config import settings
from src.core.database.session import connect_and_init_db, close_db_connection
from src.core.deps import get_current_user
from src.modules.shared.shared import router_urls as core_urls


urls_endpoints = core_urls

if settings.CYC_NGO:
    from src.modules.cyc.cyc import router_urls as cyc_urls
    urls_endpoints += cyc_urls
if settings.ACAT_NGO:
    from src.modules.acat.acat import router_urls as acat_urls
    urls_endpoints += acat_urls

dependencies: list[Depends] = [
    Depends(get_current_user)
]

app = FastAPI(**settings.fastapi_kwargs)

app.add_event_handler('startup', connect_and_init_db)
app.add_event_handler('shutdown', close_db_connection)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# @app.middleware('http')
# async def create_and_commit_mongo_session(request: Request, call_next):
#     """
#     Esta funcionalidad solo funciona si se configura un db de mongodb con replica sets.
#     """
#     client_db = get_client()
#     async with await client_db.start_session() as s:
#         async with s.start_transaction():
#             try:
#                 request.state.mongo_session = s
#                 response = await call_next(request)
#                 await s.commit_transaction()
#                 return response
#             except HTTPException:
#                 await s.abort_transaction()
#             finally:
#                 await s.end_session()


Routers(
    app=app,
    absolute_routes=urls_endpoints,
    prefix=settings.API_STR
)()


@app.get('/')
def root():
    return 'Hello world!'
