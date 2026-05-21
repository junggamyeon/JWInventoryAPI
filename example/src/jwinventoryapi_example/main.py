from endstone import Player
from endstone.inventory import ItemStack
from endstone.command import CommandSender, Command
from endstone.plugin import Plugin

from jwinventoryapi import *


class Main(Plugin):
    prefix = "JWInventoryAPI Example"
    api_version = "0.10"
    load = "POSTWORLD"
    commands = {
        "chestmenu": {
            "description": "Opens chest menu",
            "usages": ["/chestmenu"],
        }
    }

    chest_menu = Menu(MenuType.DOUBLE_CHEST, "chest menu")

    def on_command(self, sender: CommandSender, command: Command, _):
        match command.name:
            case "chestmenu":
                if isinstance(sender, Player):
                    self.chest_menu.add_item(ItemStack("minecraft:diamond_sword"))
                    self.chest_menu.add_item(ItemStack("minecraft:diamond_axe"))
                    self.chest_menu.add_item(ItemStack("minecraft:diamond_pickaxe"))
                    self.chest_menu.add_item(ItemStack("minecraft:hopper"), on_click=self.on_hopper_click)

                    ench_item = ItemStack("minecraft:diamond_sword")
                    meta = ench_item.item_meta
                    meta.add_enchant("sharpness", 5)
                    ench_item.set_item_meta(meta)
                    self.chest_menu.set_item(5, ench_item, on_click=lambda p, s, i, inv: p.send_message("Sharpness V Sword!"))

                    self.chest_menu.send_to(sender)
        return True

    def on_hopper_click(self, player: Player, slot: int, item: ItemStack, inventory: UIInventory):
        player.send_message(f"You clicked on hopper")
        menu = Menu(MenuType.HOPPER, "hopper menu")
        menu.set_item(0, ItemStack("minecraft:diamond_sword"))
        menu.set_item(1, ItemStack("minecraft:diamond_axe"))
        menu.set_item(2, ItemStack("minecraft:diamond_pickaxe"))
        self.chest_menu.close(player)
        menu.send_to(player)
