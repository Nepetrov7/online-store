from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repository.promotional_repository import PromotionalRepository
from app.schemas.promotional_schemas import (
    PromotionalCreate,
    PromotionalDelete,
    PromotionalOut,
)
from app.utils.db import get_db
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("/create", response_model=PromotionalOut)
def create_promotional(
    promotional_data: PromotionalCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = PromotionalRepository(db)

    new_promotional = repo.create_promotional(
        promotion_name=promotional_data.promotion_name,
        discount_type=promotional_data.discount_type,
        discount_value=promotional_data.discount_value,
        start_date=promotional_data.start_date,
        end_date=promotional_data.end_date,
    )
    return new_promotional


@router.get("/all", response_model=List[PromotionalOut])
def get_all_promotional(db: Session = Depends(get_db)):
    repo = PromotionalRepository(db)
    promotional = repo.get_all_promotional()

    return promotional


@router.delete("/{promotional_id}", response_model=PromotionalDelete)
def delete_promotional(
    promotional_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = PromotionalRepository(db)
    deleted = repo.delete_promotional(promotional_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promotional not found"
        )
    return {"id": promotional_id}
