from easypos.controllers.item import ItemController
from easypos.controllers.sale import SaleController

class EasyPOSApp():

    def __init__(self):
        self.item_controller = ItemController()
        self.sale_controller = SaleController()

    def run(self):

        # Display items        
        items = self.item_controller.get_items()
        
        while True:
            for item in items:
                print(f"ID: {item.id}, Name: {item.name}, Price: {item.price}")

            print("\n")
            print("Make a sale")
            item_id = int(input("ID: "))
            quantity = int(input("Quantity: "))

            sale_controller = SaleController()
            sale_controller.make_sale(item_id, quantity)
            