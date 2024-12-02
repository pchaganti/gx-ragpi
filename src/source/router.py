from fastapi import APIRouter, status, Depends

from src.config import settings
from src.source.schemas import (
    SourceCreateInput,
    SourceSearchInput,
    SourceTaskResponse,
    SourceUpdateInput,
)
from src.source.service import SourceService


router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)


@router.get("/")
def get_all_sources(source_service: SourceService = Depends()):
    sources = source_service.get_all_sources()
    return sources


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def create_source(
    source_input: SourceCreateInput,
    source_service: SourceService = Depends(),
):
    source, task_id = source_service.create_source(source_input)

    return SourceTaskResponse(
        source=source,
        task_id=task_id,
        message="Source has been created and documents are being synced. Check the task status for updates.",
    )


@router.get("/{source_name}")
def get_source(source_name: str, source_service: SourceService = Depends()):
    results = source_service.get_source(source_name)
    return results


@router.delete("/{source_name}")
def delete_source(source_name: str, source_service: SourceService = Depends()):
    source_service.delete_source(source_name)
    return {"message": f"Source '{source_name}' deleted"}


@router.put("/{source_name}", status_code=status.HTTP_202_ACCEPTED)
def update_source(
    source_name: str,
    source_input: SourceUpdateInput | None = None,
    source_service: SourceService = Depends(),
):
    source, task_id = source_service.update_source(source_name, source_input)

    return SourceTaskResponse(
        source=source,
        task_id=task_id,
        message="A task has been created to sync the source documents. Check the task status for updates.",
    )


@router.get("/{source_name}/documents")
def get_source_documents(
    source_name: str,
    limit: int | None = None,
    offset: int | None = None,
    source_service: SourceService = Depends(),
):
    results = source_service.get_source_documents(source_name, limit, offset)
    return results


@router.get("/{source_name}/search")
def search_source(
    source_name: str,
    query_input: SourceSearchInput,
    source_service: SourceService = Depends(),
):
    results = source_service.search_source(
        source_name,
        query_input.query,
        query_input.limit or settings.RETRIEVAL_LIMIT,
    )
    return results
