# TelegramNotifier

This is a simple Telegram bot that sends notifications to a Telegram chat. 

## Installation

1. Clone the repository
2. Install the requirements
3. Create a Telegram bot and get both the bot token and the chat id
4. Create a `.env` file in the main directoryy with the following content:
```
CHAT_ID=<your_chat_id>
BOT_TOKEN=<your_bot_token>
```

## Usage

The main class is a context manager that sends a message when the block of code is executed. 

```python
from telegram_notifier import Notifier

with Notifier(name="Simulation Name") as notifier:
    # Simulation code
```

this will send a message notifying when the simulation starts and when it ends, even if the code raises an exception.