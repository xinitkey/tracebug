from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy import select

from app.api.routers.auth import get_current_user
from app.db.session import SessionDep
from app.db.models.user import UserModel
from app.db.models.task import TaskModel
from app.schemas.task import TaskCreate, TaskRead

router: APIRouter = APIRouter(prefix="/task", tags=["task"])

CurrentUser = Annotated[UserModel, Depends(get_current_user)]


@router.post(path="/task", response_model=TaskRead)
async def create_task(data: TaskCreate, session: SessionDep, current_user: CurrentUser):
    task = TaskModel(
        title=data.title,
        description=data.description,
        owner_id=current_user.id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get("/tasks", response_model=list[TaskRead])
async def read_my_tasks(current_user: CurrentUser, session: SessionDep):
    result = await session.execute(
        select(TaskModel).where(TaskModel.owner_id == current_user.id)
    )

    tasks = result.scalars().all()
    return tasks
