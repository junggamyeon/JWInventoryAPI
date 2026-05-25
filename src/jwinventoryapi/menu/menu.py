from typing import Optional, Callable, TYPE_CHECKING

from endstone import Player
from endstone.inventory import ItemStack

from jwinventoryapi.manager.player_manager import find_session, create_session
from jwinventoryapi.menu.inventory import UIInventory
from jwinventoryapi.menu.menu_type import MenuType

if TYPE_CHECKING:
    from jwinventoryapi.manager import Session


class Menu:

    def __init__(self, type: MenuType, name: str = ""):
        self._name = name
        self._type = type
        self._inventory: UIInventory = UIInventory(
            type.container_size,
            slot_updated=self._on_slot_changed
        )
        self._listener: Optional[Callable[[Player, int, ItemStack, UIInventory], None]] = None
        self._place_listener: Optional[Callable[[Player, int, ItemStack, UIInventory], None]] = None
        self._open_listener: Optional[Callable[[Player], None]] = None
        self._close_listener: Optional[Callable[[Player], None]] = None
        self._sessions: set['Session'] = set()
        self._slot_listeners: dict[int, Callable[[Player, int, ItemStack, UIInventory], None]] = {}
        self._editable: bool = False
        self._locked: bool = False

    @property
    def inventory(self) -> UIInventory:
        return self._inventory

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> MenuType:
        return self._type

    def set_name(self, name: str) -> 'Menu':
        self._name = name
        return self

    def set_item(self, slot: int, item: ItemStack, on_click=None) -> 'Menu':
        self._inventory.set_item(slot, item)
        if on_click is not None:
            self._slot_listeners[slot] = on_click
        else:
            self._slot_listeners.pop(slot, None)
        return self

    def add_item(self, item: ItemStack, on_click=None) -> 'Menu':
        slot = self._inventory.first_empty
        if slot != -1:
            self.set_item(slot, item, on_click)
        return self

    def _handle_click(self, player: Player, slot: int, item: ItemStack) -> None:
        if slot in self._slot_listeners:
            self._slot_listeners[slot](player, slot, item, self._inventory)
        if self._listener is not None:
            self._listener(player, slot, item, self._inventory)

    def set_listener(self, listener) -> 'Menu':
        self._listener = listener
        return self

    def set_place_listener(self, listener) -> 'Menu':
        self._place_listener = listener
        return self

    def set_open_listener(self, listener) -> 'Menu':
        self._open_listener = listener
        return self

    def set_close_listener(self, listener) -> 'Menu':
        self._close_listener = listener
        return self

    def set_editable(self, editable: bool) -> 'Menu':
        self._editable = editable
        return self

    def set_locked(self, locked: bool) -> 'Menu':
        self._locked = locked
        return self

    @property
    def is_editable(self) -> bool:
        return self._editable

    @property
    def is_locked(self) -> bool:
        return self._locked

    def send_to(self, player: Player):
        existing_session = find_session(player)
        if existing_session is not None:
            existing_session.pending.append(self)
        else:
            session = create_session(player)
            session.menu = self
            session.send_menu()

    def close(self, player: Player) -> bool:
        from jwinventoryapi.manager import Session
        session = find_session(player)
        if session is not None and session.menu == self:
            if session.state != Session.State.CLOSING:
                session.close()
                return True
        return False

    def close_all(self) -> None:
        from jwinventoryapi.manager import Session
        for s in list(self._sessions):
            if s.state != Session.State.CLOSING:
                s.close()

    def refresh_contents(self) -> None:
        from jwinventoryapi.manager import Session
        for session in list(self._sessions):
            if session.state == Session.State.OPEN:
                session.send_contents()

    def get_viewers(self) -> list[Player]:
        from jwinventoryapi.manager import Session
        return [s.player for s in self._sessions if s.state == Session.State.OPEN]

    def _on_slot_changed(self, slot: int) -> None:
        from jwinventoryapi.manager import Session
        for session in list(self._sessions):
            if session.state == Session.State.OPEN:
                session.update_slot(slot)

    def _add_session(self, session: 'Session') -> None:
        self._sessions.add(session)

    def _remove_session(self, session: 'Session') -> None:
        self._sessions.discard(session)
