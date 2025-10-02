import random

JOB_RUNNING = False
CURRENT_JOB_ID = None

def read_watts():
    """
    Returns simulated power draw in Watts.
    Idle: 95.0 - 105.0 W
    Workload: 350.0 - 500.0 W
    """
    if not JOB_RUNNING:
        return round(random.uniform(95.0, 105.0), 2)
    else:
        return round(random.uniform(350.0, 500.0), 2)

def set_job_status(status, job_id):
    """
    Set the global job running status and current job ID.
    status: bool
    job_id: str or None
    """
    global JOB_RUNNING, CURRENT_JOB_ID
    JOB_RUNNING = status
    CURRENT_JOB_ID = job_id

def get_current_job_id():
    return CURRENT_JOB_ID
