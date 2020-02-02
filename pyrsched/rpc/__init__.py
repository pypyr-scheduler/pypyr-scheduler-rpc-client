import logging
import rpyc
from pathlib import Path
from copy import deepcopy

class RPCScheduler(object):
    CACHE_FILE = Path.home() / ".pypyr-scheduler-cli"

    def __init__(self, host="localhost", port=12345):        
        self._conn = None
        self.host = host
        self.port = port
        self.logger = logging.getLogger("pyrsched.rpc-client")
        self._previous_job_id = None

    def get_previous_job_id(self):
        if not self._previous_job_id:
            self._load_previous_job_id()
        return self._previous_job_id

    def set_previous_job_id(self, job_id):
        self._previous_job_id = job_id
        self._store_previous_job_id()

    previous_job_id = property(fget=get_previous_job_id, fset=set_previous_job_id)

    def _store_previous_job_id(self):
        with open(self.CACHE_FILE, "w") as outfile:
            outfile.write(str(self._previous_job_id))

    def _load_previous_job_id(self):
        with open(self.CACHE_FILE, "r") as infile:
            self._previous_job_id = infile.read()

    def connect(self):
        try:    
            self._conn = rpyc.connect(self.host, self.port, )
        except ConnectionError as ce:
            raise ce

    @property
    def state(self):
        state = self._conn.root.state()     
        return {k:state[k] for k in state}  # make a local object

    def list_jobs(self):
        job_list = self._conn.root.list_jobs()
        return list(job_list)

    def add_job(self, pipeline_filename, interval):
        job_id = self._conn.root.add_job(pipeline_filename, interval)
        self.previous_job_id = job_id
        return job_id

    def start_job(self, job_id):
        self.logger.debug(f"start_job({job_id})")
        if job_id == "-":
            # special case: use the stored job_id if it was stored before:
            if not self.previous_job_id:
                self.logger.error("No previous job id found.")
                raise ValueError("No previous job id found.")
            job_id = self.previous_job_id
            self.logger.debug(f"using previous job_id {job_id}")

        res = self._conn.root.start_job(job_id)        
        return res 