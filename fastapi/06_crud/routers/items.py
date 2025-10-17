from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import select, Session
from models import Item, ItemCreate
from database import get_session

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/" , response_model=Item)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    new_item = Item(**item.model_dump())
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item


@router.get("/" , response_model=list[Item])
async def get_all_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

@router.get("/{item_id}" , response_model=Item)
async def get_item(item_id: int , session:Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found....")
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int , session: Session = Depends(get_session)):
    item = session.get(Item , item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"deleted" : item_id}

