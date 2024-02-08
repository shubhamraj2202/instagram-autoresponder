import pytest
from instagrapi import DirectThread


@pytest.fixture
def mock_thread():
    # Create a mock DirectThread object with messages
    thread = DirectThread()
    thread.add_text_message("Test message 1")
    thread.add_text_message("Test message 2")
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
    from instagram_autoresponder import handle_message

    message = "Random message"
    rules = {"hi": "Hello!"}
    response = handle_message(message, rules)
    assert response == "Sorry, I didn't understand that."


def test_handle_message_matched_response():
    from instagram_autoresponder import handle_message

    message = "hi"
    rules = {"hi": "Hello!"}
    response = handle_message(message, rules)
    assert response == "Hello!"


def test_get_unread_message(mock_thread):
    from instagram_autoresponder import get_unread_message

    unread_message = get_unread_message(mock_thread)
    assert unread_message == "Test message 1\nTest message 2"


def test_get_sender_name(mock_client, mock_thread):
    from instagram_autoresponder import get_sender_name

    sender_name = get_sender_name(mock_client, mock_thread)
    assert sender_name == "sender_username"


# Add more test cases as needed...
