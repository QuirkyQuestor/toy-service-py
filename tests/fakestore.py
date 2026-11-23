from toy_service_py.schemas import Item, ItemIn


class FakeItemsStore:
    items: dict[int, Item]
    _next_id: int

    def __init__(self) -> None:
        self.items = {}
        self._next_id = 1

    async def get_one(self, item_id: int) -> Item | None:
        return self.items.get(item_id, None)

    async def get_all(self) -> list[Item]:
        return list(self.items.values())

    async def add(self, item_name: str) -> Item:
        self.items[self._next_id] = Item(id=self._next_id, name=item_name)
        self._next_id += 1
        return self.items[self._next_id - 1]

    async def update(self, item_id: int, item: ItemIn) -> Item | None:
        if item_id in self.items:
            self.items[item_id] = Item(id=item_id, name=item.name)
            return self.items[item_id]
        else:
            return None

    async def delete(self, item_id: int) -> bool:
        item = self.items.pop(item_id, None)
        return item is not None
