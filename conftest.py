import pytest
from dotenv import load_dotenv
import os

@pytest.fixture(scope="session")
def load_dv():
    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    return login, password
