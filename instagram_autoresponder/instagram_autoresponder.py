import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from instagrapi import Client


@dataclass
class BotSettings:
    auto_reply: bool = True
    check_interval_seconds: int = 60
    keep_alive_minutes: int = 10
    log_file: str = "instagram_bot_logs.txt"


@dataclass
class InstagramConfig:
    username: Optional[str] = None
    password: Optional[str] = None
    rules: Dict[str, str] = field(default_factory=dict)
    settings: BotSettings = field(default_factory=BotSettings)


def login_instagram(username: str, password: str) -> Client:
    """
    Log in to Instagram using instagrapi and return the client object
    """
    cl = Client()
    cl.login(username=username, password=password)
    return cl


def load_data(file_path: str) -> InstagramConfig:
    """
    Load configuration from a JSON file
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return InstagramConfig(**data)


def save_data(data: InstagramConfig, file_path: str) -> None:
    """
    Save configuration to a JSON file
    """
    with open(file_path, "w") as file:
        json.dump(data.__dict__, file, indent=4)


def reply_to_unread_threads(cl: Client, config: InstagramConfig) -> str:
    """
    Reply to unread messages based on predefined rules and return the last unread message
    """
    unread_threads = cl.direct_threads(selected_filter="unread")
    for thread in unread_threads:
        if not thread.messages:
            continue
        unread_message = get_unread_message(thread)
        sender_name = get_sender_name(cl, thread)
        print(f"Received message from {sender_name}: {unread_message}")
        response = handle_message(unread_message, config.rules)
        handle_response(cl, thread, sender_name, response, config)
    return unread_message


def get_unread_message(thread) -> str:
    """
    Extract and return the last unread message from a thread
    """
    unread_message = "\n".join([msg.text for msg in thread.messages[::-1]])
    return unread_message


def get_sender_name(cl: Client, thread) -> str:
    """
    Get and return the username of the sender from a thread
    """
    sender_id = thread.messages[0].user_id
    sender_name = cl.user_info(sender_id).username
    return sender_name


def handle_message(message: str, rules: Dict[str, str]) -> str:
    """
    Handle incoming message based on predefined rules
    """
    for pattern, response in rules.items():
        if re.search(pattern, message, re.IGNORECASE):
            return response
    return rules.get("default", "Sorry, I didn't understand that.")


def handle_response(
    cl: Client, thread, sender_name: str, response: str, config: InstagramConfig
) -> None:
    """
    Handle the response based on auto-reply settings
    """
    if config.settings.auto_reply:
        send_reply(cl, thread.id, response)
        write_logs(sender_name, response, config.settings.log_file)
    else:
        confirm_send_response(
            cl, thread, sender_name, response, config.settings.log_file
        )


def send_reply(cl: Client, thread_id: str, response: str) -> None:
    """
    Send the reply to the given thread ID
    """
    cl.direct_answer(thread_id=thread_id, text=response)


def confirm_send_response(
    cl: Client, thread, sender_name: str, response: str, log_file_path: str
) -> None:
    """
    Prompt user to confirm before sending the reply
    """
    print(f"About to send reply to {sender_name}: {response}")
    confirm_send = input(
        "Press 'y' to send the reply, or any other key to skip: "
    ).lower()
    if confirm_send == "y":
        print(f"Replied to {sender_name}: {response}")
        send_reply(cl, thread.id, response)
    else:
        print("Reply skipped.")
        write_logs(sender_name, response, log_file_path, skipped=True)


def write_logs(
    sender_name: str, response: str, log_file_path: str, skipped: bool = False
) -> None:
    """
    Write the message and response to the log file
    """
    with open(log_file_path, "a") as log_file:
        log_file.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {sender_name}: {response}\n"
        )
        if skipped:
            log_file.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Bot(SKIPPED): {response}\n"
            )
        else:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Bot: {response}\n")


def main(args):
    # Load data from the JSON file
    config = load_data(args.config)

    # Login to Instagram
    cl = login_instagram(config.username, config.password)

    # Keep the application running until it's closed
    while True:
        # Reply to unread messages based on rules and get the last unread message
        unread_message = reply_to_unread_threads(cl, config)

        # Display or process the last unread message as needed
        print(f"Last unread message: {unread_message}")

        # Close the application if keep_alive_minutes is specified
        if config.settings.keep_alive_minutes:
            print(f"Closing application in {keep_alive_minutes} minutes...")
            time.sleep(keep_alive_minutes * 60)
            break  # Exit the loop after the specified time

        # Wait for the specified interval before checking for unread messages again
        print(
            f"Waiting for {config.settings.check_interval_seconds} seconds before checking for new messages..."
        )
        time.sleep(config.settings.check_interval_seconds)
