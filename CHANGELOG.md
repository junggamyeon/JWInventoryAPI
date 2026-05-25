# Changelog

## v3.0.0

### Breaking Changes
- Minimum dependency: `bedrock-protocol-packets-ng==0.0.8`

### New Features
- **Lock Mode:** Fully exploit-proof read-only mode. Sends `ItemStackResponse` rejection packets so items snap back instantly on client. No visual drag possible.
- **Edit Mode:** Players can freely move items between GUI and player inventory. Supports Take, Place, Swap actions.
- **Realtime Sync:** Multiple viewers of the same menu see slot changes instantly via dirty-slot tracking and per-slot `InventorySlotPacket` updates.
- **Batch Mode with Dirty Tracking:** `begin_batch()` / `end_batch()` now tracks which slots changed and only notifies those on flush.
- **Menu Queuing:** Opening a menu while another is active queues it automatically.
- **`send_player_inventory()`:** Resends player inventory to fix ghost items after cancel.
- **Monotonic Stack IDs:** Each item sent to client gets a unique incrementing stack ID, preventing protocol desync and client crashes.

### Improvements
- Extracted packet handlers into separate methods for cleaner architecture
- `UIInventory.set_item()` now accepts `None` to clear a slot
- `is_air()` handles `None` safely
- `ItemStackWrapper` no longer crashes on unknown item types (falls back to air)
- `on_disable` properly closes all active sessions before clearing
- Removed unused `server` variable from utils
- Simplified `player_manager` using `dict.get()` / `dict.pop()`
- All setters on `Menu` return `self` for chaining
- `close_all()` and `refresh_contents()` iterate over copy of sessions set to avoid mutation during iteration
- Event handler priority set to `HIGHEST` for reliable packet interception

### Removed
- Removed all docstrings and section divider comments
- Removed `__del__` from Session (unreliable destructor)

## v2.0.0

- Initial public release with click-only mode, per-slot callbacks, and basic inventory sync.
