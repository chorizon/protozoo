#!/usr/bin/python3

from protozoo.configtask import ConfigTask, ConfigAction
from protozoo.configtasks.prebuildtask import AliveAction

ConfigTask.task='alive'
ConfigTask.info="Checking if all server are up..."

ConfigTask.action=[AliveAction]