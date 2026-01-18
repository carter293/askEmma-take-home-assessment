from fastapi import APIRouter


router = APIRouter(prefix='', tags=['health'])


@router.get("/")
async def main():
    return {"info": "Incident Report Backend for the AskEmma take home task"}


@router.get("/health")
async def read_root():
    return {"status": "healthy"}
