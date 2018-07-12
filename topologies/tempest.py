"""
Tempes Base Topology
-----------------
Build crawling sequences
"""

import os
import importlib
from utils.configuration import Job
from utils.commons import iterModules
from streamparse import Grouping, Topology

_JOB_CONF="topologies/job_config.yaml"
if os.getenv("STORM_DEBUG"):
    _JOB_CONF="topologies/dev_config.yaml"


class Tempest(Topology):
    """
    """
    job=Job(_JOB_CONF)
    job.load()
    for config in job.components:
        if config["type"] == "spout":
            #module=importlib.import_module(config["module"], package=spouts)
            spout_module="spouts.{}".format(config["module"])
            module=importlib.import_module(spout_module)
            streamObj=getattr(module,  config["class"]).spec()
        elif config["type"] == "bolts":
            groupingMode=config.get(config["grouping"], "SHUFFLE")
            if groupingMode == "fields":
                grouping_field=config["grouping_field"]
                grouping=getattr(Grouping, groupingMode)(grouping_field)
            else:
                grouping=getattr(Grouping, groupingMode)
            bolt_module="bolts.{}".format(config["module"])
            module=importlib.import_module(bolt_module)
            streamObj=iterModules(module,  config["class"]).spec(
                                            inputs={streamObj:grouping},
                                            par=config.get("par", 1))
