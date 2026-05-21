# JWInventoryAPI v2.0.0

Một plugin tạo giao diện Inventory (Chest, Hopper,...) cho Endstone. Phiên bản này (v2.0.0) mang đến API đơn giản, dễ hiểu và mạnh mẽ hơn!

---

## 🛠 Hướng Dẫn Sử Dụng (API)

### 1. Các loại Menu (MenuType)
Bạn có thể tạo các dạng UI với kích thước khác nhau:
- `MenuType.CHEST` - Rương đơn (27 ô)
- `MenuType.DOUBLE_CHEST` - Rương đôi (54 ô)
- `MenuType.DISPENSER` - Máy phân phát (9 ô)
- `MenuType.HOPPER` - Phễu (5 ô)

### 2. Khởi tạo Menu

```python
from jwinventoryapi import Menu, MenuType

# Tạo một menu Rương Đơn với tiêu đề "My Menu"
my_menu = Menu(type=MenuType.CHEST, name="My Menu")
```

### 3. Thêm Item và Gắn Sự Kiện Click (Cách Mới Rất Tiện Lợi)

Thay vì phải kiểm tra từng `slot` người chơi click, giờ đây bạn có thể **gắn trực tiếp hành động (function) vào lúc bạn thêm Item!**

**A. Đặt Item ở một ô (slot) cụ thể:**
```python
from endstone.inventory import ItemStack

def on_diamond_click(player, slot, item, inventory):
    player.send_message("Bạn vừa bấm vào Kim Cương!")
    my_menu.close(player)

# Đặt kim cương ở ô số 4 và gọi hàm trên khi click
my_menu.set_item(4, ItemStack("minecraft:diamond"), on_click=on_diamond_click)
```

**B. Gắn nhanh (dùng lambda):**
```python
my_menu.set_item(
    0, 
    ItemStack("minecraft:apple"), 
    on_click=lambda p, s, i, inv: p.send_message("Táo ngon!")
)
```

**C. Tự động tìm ô trống để thêm:**
```python
my_menu.add_item(ItemStack("minecraft:stone"), on_click=lambda p, s, i, inv: p.send_message("Cục đá!"))
```

### 4. Hiển Thị và Đóng Menu

- **Mở Menu:**
```python
my_menu.send_to(player)
```

- **Đóng Menu:**
```python
my_menu.close(player)      # Đóng với 1 người chơi
my_menu.close_all()        # Đóng với TẤT CẢ người chơi đang xem
```

---

## 🚀 Các Phương Thức (Methods) Khác Của `Menu`

- `set_name(name: str)` - Đổi lại tên (tiêu đề) của menu.
- `set_listener(listener)` - Lắng nghe SỰ KIỆN CHUNG khi click vào bất kỳ ô nào trong menu.
- `set_place_listener(listener)` - Lắng nghe sự kiện khi người chơi click vào kho đồ CỦA HỌ (túi đồ ở dưới) khi menu đang mở.
- `set_open_listener(listener)` - Hành động khi có người MỞ menu.
- `set_close_listener(listener)` - Hành động khi có người ĐÓNG menu.
- `get_viewers()` - Trả về danh sách (`list[Player]`) những người đang xem menu này.

---

## 📌 Ví dụ Đầy Đủ

```python
from endstone import Player
from endstone.inventory import ItemStack
from endstone.plugin import Plugin
from jwinventoryapi import Menu, MenuType

class MyPlugin(Plugin):
    def on_enable(self):
        # 1. Tạo Menu
        self.menu = Menu(MenuType.CHEST, "§l§bShop Vũ Khí")
        
        # 2. Thêm đồ và hành động
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
        player.send_message("Đã mua Kiếm Kim Cương thành công!")
        # Bạn có thể code logic trừ tiền ở đây
        self.menu.close(player)
```
