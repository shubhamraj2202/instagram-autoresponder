from dataclasses import dataclass

import pytest
from instagrapi.types import DirectMessage, DirectThread

from instagram_autoresponder.instagram_autoresponder import (
    get_sender_name,
    get_unread_message,
    handle_message,
)


@pytest.fixture
def mock_thread():
    mock_messages = [
        DirectMessage(
            pk=1,
            id="mock_message_id_1",
            text="Test message 1",
            user_id="sender_id_1",
            timestamp="2024-02-08T12:00:00",
            created_at="2024-02-08T12:00:00",
            is_seen=False,
        ),
        DirectMessage(
            pk=2,
            id="mock_message_id_2",
            text="Test message 2",
            user_id="sender_id_2",
            timestamp="2024-02-08T12:05:00",
            created_at="2024-02-08T12:05:00",
            is_seen=False,
        ),
    ]
    # Create a mock DirectThread object with required fields filled
    thread = DirectThread(
        pk=1,
        id="dummy_id",
        messages=mock_messages,
        users=[],
        admin_user_ids=[],
        last_activity_at="2024-02-08T12:00:00",
        muted=False,
        named=False,
        canonical=False,
        pending=False,
        archived=False,
        thread_type="",
        thread_title="",
        folder=0,  # Example integer value, replace with appropriate value
        input_mode=0,  # Example integer value, replace with appropriate value
        business_thread_folder=0,  # Example integer value, replace with appropriate value
        read_state=0,  # Example integer value, replace with appropriate value
        assigned_admin_id=0,  # Example integer value, replace with appropriate value
        last_seen_at={},  # Empty dictionary as an example
        vc_muted=False,
        is_group=False,
        mentions_muted=False,
        approval_required_for_new_members=False,
        is_close_friend_thread=False,
        shh_mode_enabled=False,
    )
    return thread


@pytest.fixture
def mock_client(mock_thread):
    # Create a mock instagrapi Client object
    class MockClient:
        def __init__(self):
            pass

        def direct_threads(self, selected_filter=None):
            # Mock the behavior of fetching direct message threads
            if selected_filter == "unread":
                return [mock_thread]
            return []

        def user_info(self, user_id):
            # Mock the behavior of fetching user info
            class UserInfo:
                def __init__(self, username):
                    self.username = username

            return UserInfo("sender_username")

        def direct_answer(self, thread_id, text):
            # Mock the behavior of sending a direct message reply
            pass

    return MockClient()


def test_handle_message_default_response():

    message = "Random message"
    rules = {"hi": "Hello!"}
    response = handle_message(message, rules)
    assert response == "Sorry, I didn't understand that."


def test_handle_message_matched_response():

    message = "hi"
    rules = {"hi": "Hello!"}
    response = handle_message(message, rules)
    assert response == "Hello!"


def get_unread_message(thread) -> str:
    """
    Extract and return the last unread message from a thread
    """
    # Sort messages by timestamp in descending order
    sorted_messages = sorted(
        thread.messages, key=lambda msg: msg.timestamp, reverse=True
    )

    # Extract text from each message and join them into a single string
    unread_message = "\n".join(msg.text for msg in sorted_messages)

    return unread_message


def test_get_sender_name(mock_client, mock_thread):

    sender_name = get_sender_name(mock_client, mock_thread)
    assert sender_name == "sender_username"


# Add more test cases as needed...
