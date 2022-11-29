from typing import Any, Iterable, List
import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from family_budget.models.budget import Budget as BudgetModel
from family_budget.schemas.v1.budget import Budget as BudgetSchema
from family_budget.schemas.v1.budget import BudgetCreateRequest


async def get_budget_by_user_id(
    db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> List[BudgetSchema]:
    query = db.query(BudgetModel).filter(BudgetModel.created_by == user_id)
    return query.offset(skip).limit(limit).all()


async def create_budget(db: Session, request: BudgetCreateRequest, **extra_attrs: Any):
    data = {**jsonable_encoder(request, by_alias=False), **extra_attrs}
    budget = BudgetModel(**data)
    db.add(budget)
    return budget
