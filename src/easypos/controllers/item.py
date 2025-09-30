
from easypos.models.item import ItemModel, ItemService

class ItemController:
    
    def __init__(self):
        self.items = ItemService.get_items()


    def get_items(self):
        return self.items