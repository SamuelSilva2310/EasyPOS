from easypos.controllers.item import ItemController
from easypos.controllers.sale import SaleController

#from tkinter import *
from easypos.ui.ui_app import UIApp

import logging

logger = logging.getLogger(__name__)

class EasyPOSApp():

    def __init__(self, ticket_queue, printer_connection_type):
        self.item_controller = ItemController()
        self.sale_controller = SaleController(ticket_queue, printer_connection_type)
        self.queue = ticket_queue

    def run(self):

        # Display items        
        logger.info(f"Loading items...")
        items = self.item_controller.get_items()
        logger.info(f"Loaded {len(items)} items")


        ui_app = UIApp(items)
        ui_app.run()

        
        # while True:
        #     for item in items:
        #         print(f"ID: {item.id}, Name: {item.name}, Price: {item.price}")

        #     print("\n")
        #     print("Make a sale")
        #     item_id = int(input("ID: "))
        #     quantity = int(input("Quantity: "))

            
        #     self.sale_controller.make_sale(item_id, quantity)
        #     #self.sale_controller.make_sale(3, quantity)
            