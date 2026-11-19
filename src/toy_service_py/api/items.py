from fastapi import APIRouter, HTTPException, status

from ..schemas import Item, ItemIn
from ..store import StoreDep

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
async def list_items(store: StoreDep) -> list[Item]:
    return await store.get_all()


@router.get("/{item_id}")
async def get_item(store: StoreDep, item_id: int) -> Item:
    the_item = await store.get_one(item_id)
    if the_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    return the_item


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_item(store: StoreDep, item: ItemIn) -> Item:
    the_item = await store.add(item.name)
    return the_item


@router.put("/{item_id}")
async def update_item(store: StoreDep, item_id: int, item: ItemIn) -> Item:
    the_item = await store.update(item_id, item)
    if the_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    return the_item
