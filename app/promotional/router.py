from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.promotional.schema import (
    PromotionalCreate,
    PromotionalResponse,
    PromotionalUpdate,
)
from app.promotional.service import PromotionalService
from app.utils.dependencies import get_current_user, get_db

router = APIRouter()


def get_promotional_service(db: Session = Depends(get_db)) -> PromotionalService:
    return PromotionalService(db)


@router.get("/", response_model=List[PromotionalResponse])
def list_promotional(
    service: PromotionalService = Depends(get_promotional_service),
):
    return service.list_promos()


@router.post(
    "/",
    response_model=PromotionalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_promotional(
    data: PromotionalCreate,
    service: PromotionalService = Depends(get_promotional_service),
    current_user=Depends(get_current_user),
):
    return service.create_promo(data)


@router.get("/{promo_id}", response_model=PromotionalResponse)
def get_promotional(
    promo_id: int,
    service: PromotionalService = Depends(get_promotional_service),
):
    promo = service.get_promo(promo_id)
    if not promo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promotional not found"
        )
    return promo


@router.put("/{promo_id}", response_model=PromotionalResponse)
def update_promotional(
    promo_id: int,
    data: PromotionalUpdate,
    service: PromotionalService = Depends(get_promotional_service),
    current_user=Depends(get_current_user),
):
    updated = service.update_promo(promo_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promotional not found"
        )
    return updated


@router.delete("/{promo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotional(
    promo_id: int,
    service: PromotionalService = Depends(get_promotional_service),
    current_user=Depends(get_current_user),
):
    if not service.delete_promo(promo_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promotional not found"
        )
