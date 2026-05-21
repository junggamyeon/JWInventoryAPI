# JWInventoryAPI v2.0.0

A read-only Inventory UI plugin for Endstone servers. This version (v2.0.0) brings a simpler, easier to understand, and more powerful API!

---

## 🛠 API Usage

### 1. Menu Types (MenuType)
You can create UI menus with various container sizes:
- `MenuType.CHEST` - Single chest (27 slots)
- `MenuType.DOUBLE_CHEST` - Double chest (54 slots)
- `MenuType.DISPENSER` - Dispenser (9 slots)
- `MenuType.HOPPER` - Hopper (5 slots)

### 2. Creating a Menu

```python
from jwinventoryapi import Menu, MenuType

# Create a Single Chest menu with the title "My Menu"
my_menu = Menu(type=MenuType.CHEST, name="My Menu")
```

### 3. Adding Items and Click Listeners (New & Convenient Method)

Instead of checking each `slot` globally when a player clicks, you can now **attach actions (functions) directly when adding an Item!**

**A. Set an Item at a specific slot:**
```python
from endstone.inventory import ItemStack

def on_diamond_click(player, slot, item, inventory):
    player.send_message("You clicked the Diamond!")
    my_menu.close(player)

# Place a diamond in slot 4 and call the above function when clicked
my_menu.set_item(4, ItemStack("minecraft:diamond"), on_click=on_diamond_click)
```

**B. Quick attachment (using lambda):**
```python
my_menu.set_item(
    0, 
    ItemStack("minecraft:apple"), 
    on_click=lambda p, s, i, inv: p.send_message("Yummy apple!")
)
```

**C. Automatically find the first empty slot to add:**
```python
my_menu.add_item(ItemStack("minecraft:stone"), on_click=lambda p, s, i, inv: p.send_message("A stone!"))
```

### 4. Displaying and Closing the Menu

- **Open Menu:**
```python
my_menu.send_to(player)
```

- **Close Menu:**
```python
my_menu.close(player)      # Close for a specific player
my_menu.close_all()        # Close for ALL players currently viewing
```

---

## 🚀 Other `Menu` Methods

- `set_name(name: str)` - Change the title of the menu.
- `set_listener(listener)` - Listen to GLOBAL click events on any slot in the menu.
- `set_place_listener(listener)` - Listen to events when a player clicks their OWN inventory (bottom section) while the menu is open.
- `set_open_listener(listener)` - Action to perform when a player OPENS the menu.
- `set_close_listener(listener)` - Action to perform when a player CLOSES the menu.
- `get_viewers()` - Returns a list (`list[Player]`) of players currently viewing this menu.

---

## 📌 Full Example

```python
from endstone import Player
from endstone.inventory import ItemStack
from endstone.plugin import Plugin
from jwinventoryapi import Menu, MenuType

class MyPlugin(Plugin):
    def on_enable(self):
        # 1. Create Menu
        self.menu = Menu(MenuType.CHEST, "§l§bWeapon Shop")
        
        # 2. Add items and actions
        self.menu.set_item(
            4, 
            ItemStack("minecraft:diamond_sword"), 
            on_click=self.buy_sword
        )

        self.menu.set_item(
            8, 
            ItemStack("minecraft:barrier"), 
            on_click=lambda p, s, i, inv: self.menu.close(p)
        )

    def buy_sword(self, player: Player, slot: int, item: ItemStack, inventory):
        player.send_message("Successfully purchased a Diamond Sword!")
        # You can add logic to deduct money here
        self.menu.close(player)
```