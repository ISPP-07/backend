from fastapi import APIRouter

router = APIRouter(
    tags=['cyc']
)


@router.get('/', status_code=200)
def root():
    return 'Hello user cyc!!'
