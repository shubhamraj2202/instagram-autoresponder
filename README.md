![build](https://github.com/shubhamraj2202/instagram-autoresponder/actions/workflows/ci-test.yml/badge.svg)
[![codecov](https://codecov.io/gh/shubhamraj2202/instagram-autoresponder/branch/main/graph/badge.svg?token=ciJFM9MV99)](https://codecov.io/gh/shubhamraj2202/instagram-autoresponder)
# Instagram Direct Message Autoresponder

This project allows you to automatically respond to direct messages (DMs) on Instagram based on predefined rules. It uses the `instagrapi` library to interact with Instagram's API.

## Features

- Automatic response to incoming direct messages based on predefined rules.
- Configuration settings for auto-reply, check interval, keep-alive duration, and log file path.
- Logs for all messages and responses.
- Test cases using Pytest.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
    pip install -r requirements.txt

## Usage

1. Create a configuration JSON file with your Instagram credentials, rules, and settings. Here's an example configuration:

```json
{
    "username": "your_instagram_username",
    "password": "your_instagram_password",
    "rules": {
        "hi|hello|hey": "Hi there! How are you doing?",
        "how are you|how r u": "I'm doing well, thanks for asking! How about you?",
        "default": "Sorry, I didn't understand that."
    },
    "settings": {
        "auto_reply": true,
        "check_interval_seconds": 60,
        "keep_alive_minutes": 5,
        "log_file": "instagram_bot_logs.txt"
    }
}
```

Run the script with the path to your configuration file:

```bash
python run.py --config path/to/your/config.json
````

## Configuration

- `username`: Your Instagram username.
- `password`: Your Instagram password.
- `rules`: Dictionary containing message patterns and corresponding responses.
- `settings`:
    - `auto_reply`: Whether to automatically reply to messages. Default is true. if false, it will prompt before confirm sending the response to the user.
    - `check_interval_seconds`: Interval (in seconds) to check for new messages. Default is 60.
    - `keep_alive_minutes`: Duration (in minutes) to keep the application running. Set to null to run indefinitely.
    - `log_file`: Path to the log file. Default is instagram_bot_logs.txt.

## Testing

To run the test cases, use the following command:

```bash
pytest
```

## Disclaimer
Please note that this project utilizes the [instagrapi]([https://github.com/subzeroid/instagrapi) library, which is a third-party tool for interacting with Instagram's API. This is an unofficial tool, and its usage might not be in compliance with Instagram's terms of service. Users should proceed with caution and review Instagram's policies to understand the potential risks, including the possibility of account restrictions or bans for automating direct message responses. This tool is provided "as is", and users should use it at their own risk, ensuring they are aware of and accept the potential implications of using unofficial APIs to interact with Instagram services.

## Additional Advice
Review Instagram's Policy: Before using the autoresponder, it's crucial to review Instagram's Platform Policy and Community Guidelines to ensure compliance and avoid potential violations.
Consider Privacy and Security: Be mindful of the security implications of storing and using Instagram credentials in scripts or applications. Ensure that your implementation follows best practices for data security and privacy.
Stay Updated: Since this relies on an unofficial library, be prepared for the possibility of future changes to Instagram's API affecting the functionality of your autoresponder. Keep the library and your scripts updated and monitor for any announcements from the library maintainers regarding compatibility or new features.
