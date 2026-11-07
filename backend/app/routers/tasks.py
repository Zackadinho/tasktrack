"""The REST endpoints for tasks.

REST maps HTTP methods to actions on a "resource" (here, tasks):

    GET     /tasks        -> list all tasks           (Read)
    POST    /tasks        -> create a task            (Create)
    GET     /tasks/{id}   -> get one task             (Read)
    PATCH   /tasks/{id}   -> change part of a task    (Update)
    DELETE  /tasks/{id}   -> delete a task            (Delete)

That's "CRUD". Almost every app is CRUD plus rules.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Task
from ..schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    # The ORM builds: SELECT * FROM tasks ORDER BY created_at DESC
    return db.scalars(select(Task).order_by(Task.created_at.desc())).all()


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()       # write to the database (end the transaction)
    db.refresh(task)  # reload so we get DB-generated values (id, created_at)
    return task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return _get_task_or_404(db, task_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    for field, value in payload.model_dump(exclude_unset=True).items():  # only fields the client actually sent
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()
