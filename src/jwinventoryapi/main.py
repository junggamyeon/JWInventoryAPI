from endstone.plugin import Plugin

from jwinventoryapi.listener import EventListener


class JWInventoryAPI(Plugin):
    prefix = "JWInventoryAPI"
    api_version = "0.10"
    load = "POSTWORLD"

    def on_enable(self) -> None:
        self.register_events(EventListener(self))

    def on_disable(self) -> None:
        from jwinventoryapi.manager.player_manager import sessions
        # Đảm bảo đóng tất cả session (dọn dẹp tài nguyên) khi plugin bị tắt (Rule S6)
        sessions.clear()
