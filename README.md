## Description:

Parses the output of the SLURM command `scontrol show job <a job id>` reliably with a context-free grammar.

The context-free grammar is coded in lark: https://github.com/lark-parser/lark.

## Usage:

Call `scontrol_parser.call(a_job_id)` if you need to call the function once or rarely. You can also call `scontrol_parser.parse(output_of_scontrol_show_job)`.

You can call `scontrol_parser.call()` if the script is running in the job you want the info of.

If parsing multiple times is needed, it is recommended to do instantiate an `scontrol_parser.Parser()` and call the functions on it.

**Example:**

Print a table with the info of a few jobs:
```python
import scontrol_parser

job_ids = [12232, 31231, 32123]

parser = scontrol_parser.Parser()

job_id_to_info = {job_id: parser(job_id) for job_id in job_ids}

for job_id, info in job_id_to_info.items():
  print(f"job_id: {job_id}")
  for key, value in info.items()
    print(f"{key}: {value}")
  print()
```

Find out if the current job was launched with `sbatch`:
```python

import scontrol_parser

batch_flag = scontrol_parser.call()["BatchFlag"]

if batch_flag == "1":
  print("Called with sbatch")
else:
  print("Interactive or Srun")
  
```
