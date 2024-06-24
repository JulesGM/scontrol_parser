import os
import subprocess as sp
from typing import Optional, Union


import fire
import lark

_GRAMMAR = r"""
start: kv_pair*
        
kv_pair: key "=" value

key: /[\w\/:]+/

value:    /[^ \n"]+/
        | STRING

%import common.ESCAPED_STRING   -> STRING
%import common.WS
%ignore WS
"""


Parsed = dict[str, str]


class _Transformer(lark.Transformer):
    def start(self, items) -> Parsed:
        return dict(items)
    
    def kv_pair(self, items):
        # print(f"{items = }")
        assert len(items) == 2
        key = items[0].children[0].value
        value = items[1].children[0].value
        
        return (key, value)


class Parser:

    def __init__(self):
        self._transformer = _Transformer()
        self._parser = lark.Lark(_GRAMMAR, start="start", parser="lalr")

    def parse(self, command_output: str, sort: bool = False) -> Parsed:
        parse_tree = self._parser.parse(command_output)
        parsed =  self._transformer.transform(parse_tree)

        if sort:
            parsed = dict(sorted(parsed.items()))

        return parsed

    def call(self, job_id: Optional[Union[str,int]] = None, sort: bool = False) -> Parsed:

        if job_id is None:
            if not "SLURM_JOB_ID" in os.environ:
                raise ValueError("`call` needs either a job id or a value in the SLURM_JOB_ID environment valriable.")
        
            job_id = os.environ["SLURM_JOB_ID"]
            
        output = sp.check_output(["scontrol", "show", "job", str(job_id)], text=True)
        
        parsed = self.parse(output, sort=sort)

        return parsed

    __call__ = call


def parse(output: str, sort=False) -> Parsed:
    # Transformer to convert the parse tree into a dictionary
    parser = Parser()
    return parser.parse(output, sort=sort)


def call(job_id: Optional[Union[int, str]] = None, sort: bool = False) -> Parsed:
    parser = Parser()
    return parser.call(job_id, sort=sort)


def test():
    # Example usage
    scontrol_output = """
    JobId=4925680 JobName=interactive
    UserId=gagnonju(1471600291) GroupId=gagnonju(1471600291) MCS_label=N/A EscapedString="he h \\" ehhah a" 
    Priority=53686 Nice=0 Account=mila QOS=normal
    JobState=RUNNING Reason=None Dependency=(null)
    Requeue=1 Restarts=0 BatchFlag=0 Reboot=0 ExitCode=0:0
    RunTime=00:06:23 TimeLimit=7-00:00:00 TimeMin=N/A
    SubmitTime=2024-06-23T21:45:57 EligibleTime=2024-06-23T21:45:57
    AccrueTime=Unknown
    StartTime=2024-06-23T21:45:57 EndTime=2024-06-30T21:45:57 Deadline=N/A
    PreemptEligibleTime=2024-06-23T21:45:57 PreemptTime=None
    SuspendTime=None SecsPreSuspend=0 LastSchedEval=2024-06-23T21:45:57 Scheduler=Main
    Partition=long AllocNode:Sid=cn-c032:1910528
    ReqNodeList=(null) ExcNodeList=(null)
    NodeList=cn-c015
    BatchHost=cn-c015
    NumNodes=1 NumCPUs=4 NumTasks=1 CPUs/Task=4 ReqB:S:C:T=0:0:*:*
    ReqTRES=cpu=4,mem=48G,node=1,billing=1,gres/gpu=1
    AllocTRES=cpu=4,mem=48G,node=1,billing=1,gres/gpu=1
    Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
    MinCPUsNode=4 MinMemoryNode=48G MinTmpDiskNode=0
    Features=x86_64 DelayBoot=00:00:00
    OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)
    Command=/bin/sh
    WorkDir=/home/mila/g/gagnonju/marglicot
    Power=
    TresPerNode=gres/gpu:rtx8000:1
    TresPerTask=cpu:4
    """

    return parse(scontrol_output)


    
if __name__ == "__main__":
    fire.Fire({
        "parse": parse,
        "call": call,
        "test": test,
    })
