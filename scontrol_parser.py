import os
import json
import subprocess as sp


def call(job_id=None):
  if job_id is None:
    assert "SLURM_JOB_ID" in os.environ, "Either need a value for the argument job_id or a value for the argument $SLURM_JOB_ID"
    job_id = os.environ["SLURM_JOB_ID"]

  output = sp.check_output(["scontrol", "--json", "show", "job", str(job_id)], text=True).strip()
  parsed = json.loads(output)["jobs"]
  assert len(parsed) == 1, parsed
  parsed = parsed[0]

  return parsed
