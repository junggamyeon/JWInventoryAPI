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
        self._inventory: UIInventory = UIInventory(type.container_size,
                                                   slot_updated=self._on_slot_changed)
        self._listener: Optional[Callable[[Player, int, ItemStack, UIInventory], None]] = None
        self._place_listener: Optional[Callable[[Player, int, ItemStack, UIInventory], None]] = None
        self._open_listener: Optional[Callable[[Player], None]] = None
        self._close_listener: Optional[Callable[[Player], None]] = None
        self._sessions: set['Session'] = set()
        self._slot_listeners: dict[int, Callable[[Player, int, ItemStack, UIInventory], None]] = {}

    @property
    def inventory(self):
        return self._inventory

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def set_name(self, name: str):
        """
        Set the display name of the menu.

        Args:
            name: The new display name to show at the top of the menu.
        """
        self._name = name

    def set_item(self, slot: int, item: ItemStack, on_click: Optional[Callable[[Player, int, ItemStack, UIInventory], None]] = None) -> 'Menu':
        """
        Set an item in the menu and optionally register a click listener for it.
        """
        self._inventory.set_item(slot, item)
        if on_click is not None:
            self._slot_listeners[slot] = on_click
        else:
            self._slot_listeners.pop(slot, None)
        return self

    def add_item(self, item: ItemStack, on_click: Optional[Callable[[Player, int, ItemStack, UIInventory], None]] = None) -> 'Menu':
        """
        Add an item to the first empty slot and optionally register a click listener for it.
        """
        slot = self._inventory.first_empty
        if slot != -1:
            self.set_item(slot, item, on_click)
        return self

    def _handle_click(self, player: Player, slot: int, item: ItemStack) -> None:
        if slot in self._slot_listeners:
            self._slot_listeners[slot](player, slot, item, self._inventory)
        if self._listener is not None:
            self._listener(player, slot, item, self._inventory)

    def set_listener(self, listener: Callable[[Player, int, ItemStack, UIInventory], None]):
        self._listener = listener

    def set_place_listener(self, listener: Callable[[Player, int, ItemStack, UIInventory], None]):
        """
        Set the callback for when a player clicks an item from their own inventory
        while this menu is open.
        """
        self._place_listener = listener

    def set_open_listener(self, listener: Callable[[Player], None]):
        """
        Set the callback for menu open events.

        Args:
            listener: A function called when a player opens this menu.
        """

        self._open_listener = listener

    def set_close_listener(self, listener: Callable[[Player], None]):
        """
        Set the callback for menu close events.

        Args:
            listener: A function called when a player closes this menu.
        """
        self._close_listener = listener

    def send_to(self, player: Player):
        """
        Display this menu to a player.

        If the player already has a menu open, this menu is queued and will
        be shown after the current menu is closed. Otherwise, a new session
        is created and the menu is displayed immediately.

        Args:
            player: The player to show the menu to.
        """
        existing_session = find_session(player)
        if existing_session is not None:
            existing_session.pending.append(self)
        else:
            session = create_session(player)
            session.menu = self
            session.send_menu()

    def close(self, player: Player) -> bool:
        """
        Close this specific menu for a player.

        Only closes the menu if it matches the player's currently open menu
        and the session is not already in a closing state.
        """
        from jwinventoryapi.manager import Session
        session = find_session(player)
        if session is not None:
            if session.menu == self and session.state != Session.State.CLOSING:
                session.close()
                return True
        return False

    def close_all(self) -> None:
        """
        Close this menu for all players currently viewing it.
        """
        from jwinventoryapi.manager import Session
        for s in self._sessions:
            if s.state != Session.State.CLOSING:
                s.close()

    def get_viewers(self) -> list[Player]:
        """
        Get a list of players who currently have this menu open.
        """
        from jwinventoryapi.manager import Session
        players = []
        for s in self._sessions:
            if s.state == Session.State.OPEN:
                players.append(s.player)
        return players

    def _on_slot_changed(self, slot: int) -> None:
        from jwinventoryapi.manager import Session
        for session in self._sessions:
            if session.state == Session.State.OPEN:
                session.update_slot(slot)

    def _add_session(self, session: 'Session') -> None:
        self._sessions.add(session)

    def _remove_session(self, session: 'Session') -> None:
        self._sessions.discard(session)
