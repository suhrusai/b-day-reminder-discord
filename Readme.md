# Birthday Reminder Bot for Discord

This Python-based Discord bot automates birthday tracking and notifications. It integrates with a web interface built using **Vuetify** and **Vue.js**, which allows users to manage servers and birthdays while ensuring privacy and customization.

## Features

- **Web Interface**: Manage servers, add birthdays, and configure notification settings through an easy-to-use interface built in **Vuetify** and **Vue.js**.
- **Birthday Tracking**: Automatically tracks birthdays stored in a Firebase database.
- **Customizable Notifications**: Choose which servers receive birthday notifications for privacy and flexibility.
- **Firebase Integration**: Persistent storage of birthday data using Firebase ensures reliability.
- **Automated Reminders**: Sends birthday notifications to the selected Discord servers based on the schedule configured via the web interface.

## Folder Structure

- `Constants.py`: Stores configuration details such as Discord API tokens and Firebase credentials.
- `FirebaseConnect.py`: Manages interaction with the Firebase database for storing and retrieving birthday data.
- `Helpers/`: Contains utility functions for scheduling, formatting, and handling repetitive tasks.
- `Models/`: Defines the structure for birthday and server data.
- `Services/`: Provides the core services for managing birthday notifications and interacting with Discord.
- `main.py`: The main execution file that connects the bot to Discord and schedules notifications.
- `requirements.txt`: Lists all the dependencies required to run the bot.

## Prerequisites

- Python 3.x
- A Discord bot token (available via the [Discord Developer Portal](https://discord.com/developers/docs/intro))
- Firebase account for storing birthday data
- Vuetify and Vue.js for managing the web interface (though this part of the repository is private)
- Python libraries listed in `requirements.txt`

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/b-day-reminder-discord.git
    cd b-day-reminder-discord
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Firebase**:
    - Create a Firebase project and download the credentials file.
    - Update `FirebaseConnect.py` with your Firebase configuration.

4. **Configure Discord Bot**:
    - Generate a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
    - Update the `Constants.py` file with your bot token.

5. **Run the bot**:
    ```bash
    python main.py
    ```

## Web Interface

The bot is controlled via a private web interface built with **Vuetify** and **Vue.js**. This interface allows users to:
- Add birthdays and manage them.
- Add and manage servers where notifications are sent.
- Select which servers should receive birthday notifications.

For privacy reasons, the web interface code and URL are hidden.

## How It Works

- The bot continuously monitors a Firebase database for upcoming birthdays and sends notifications to the selected servers.
- The web interface provides a simple way to manage birthday data and control which servers receive the notifications.

## License

This project is licensed under the MIT License.
