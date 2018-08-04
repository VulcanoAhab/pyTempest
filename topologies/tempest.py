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

TYPE_SPOUT="spout"
TYPE_BOLD="bolt"

class Tempest(Topology):
    """
    """
    job=Job(_JOB_CONF)
    job.load()

    last_type=None
    tempestBolt=None
    tempestSpout=None

    for config in job.components:

        if config["type"] == TYPE_SPOUT:
            print("[+] ADDING SPOUT:{}".format(config["module"]))
            #module=importlib.import_module(config["module"], package=spouts)
            spout_module="spouts.{}".format(config["module"])
            module=importlib.import_module(spout_module)
            tempestSpout=getattr(module,  config["class"]).spec()
            last_type=config["type"]

        elif config["type"] ==TYPE_BOLD:
            print("[+] ADDING BOLT:{}".format(config["module"]))
            groupingMode=config.get(config["grouping"], "SHUFFLE")
            if groupingMode == "fields":
                grouping_field=config["grouping_field"]
                grouping=getattr(Grouping, groupingMode)(grouping_field)
            else:
                grouping=getattr(Grouping, groupingMode)
            bolt_module="bolts.{}".format(config["module"])
            module=importlib.import_module(bolt_module)
            if last_type == TYPE_SPOUT:
                insDict={tempestSpout:grouping}
            else:
                insDict={tempestBolt:grouping}
            tempestBolt=iterModules(module, config["class"]).spec(
                                            inputs=insDict,
                                            par=config.get("par", 1))
            if not tempestBolt:break
            last_type=config["type"]
