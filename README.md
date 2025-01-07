# CialloSecurityChat

A real-time chat application built with Flask and WebSocket, featuring a dark theme and random Chinese usernames.

## Features

- Real-time messaging using WebSocket
- Random Chinese username assignment
- Message history storage
- Dark theme UI
- Live logging system
- Multiple views (Chat, Settings, About, Logs)
- Auto-reconnect mechanism
- Message sanitization
- Loading animations
- Responsive design

## Prerequisites

- Python 3.7+
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CNMengHan/CialloSecurityChat.git
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses several configuration settings that can be modified in `app.py`:

- `APPLICATION_ROOT`: Set to '/ciallosecurity'
- `SECRET_KEY`: Session secret key
- `PERMANENT_SESSION_LIFETIME`: Session lifetime (24 hours by default)
- Default port: 43816

## Usage

1. Start the server:
```bash
python app.py
```

2. Access the application at:
```
http://localhost:43816/ciallosecurity/
```

## Features in Detail

### Chat System
- Real-time message delivery using Socket.IO
- Message length limit (500 characters)
- Automatic scrolling to latest messages
- Unique color assignment for each username

### Security Features
- XSS protection
- Content Security Policy (CSP)
- Session management
- Proxy support
- Message sanitization

### Logging System
- Real-time log viewing
- Log refresh functionality
- Log clearing option
- Timestamp and level-based logging

### UI Features
- Dark theme
- Loading animations
- Custom scrollbar design
- Responsive layout
- Multiple view tabs

## API Endpoints

- `/ciallosecurity/` - Main chat interface
- `/ciallosecurity/logs` - Log viewing endpoint
- `/ciallosecurity/socket.io` - WebSocket endpoint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
