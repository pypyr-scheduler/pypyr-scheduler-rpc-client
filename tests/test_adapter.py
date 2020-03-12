from pyrsched.rpc import RPCScheduler

class TestAdapter:
    def test_state(self, scheduler_server):
        conn = RPCScheduler()