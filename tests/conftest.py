import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import threading



@pytest.fixture(scope="function")
def scheduler_server():
    # start server in background
    # server = ServerWrapper(conf_dir)

    # t = threading.Thread(target=server.start)

    # yield server

    # server.shutdown()
    pass