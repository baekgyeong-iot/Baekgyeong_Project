# Baekgyeong_Project

## Backend

- `app.py`: Flask API server for the React dashboard.
- `mqtt_client.py`: MQTT bridge between LCD/IoT events and `game_logic`.

### API

- `GET /api/state`
- `GET /api/logs`
- `GET /api/rankings`
- `GET /api/inventory`
- `POST /api/event`

### Game Logic Event Entry

Use `game_logic.event_handler.handle_event(event_message)` for all game events.
