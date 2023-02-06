import logging
import os

import beeline


def post_worker_init(worker):
    logging.info(f"beeline initialization in process pid {os.getpid()}")
    beeline.init(
        writekey=os.environ.get("HONEYCOMB_WRITEKEY"),
        dataset=os.environ.get("HONEYCOMB_DATASET"),
        service_name="django",
    )
