#!/usr/bin/python3

from protozoo.configtask import ConfigTask, ConfigAction
from protozoo.configtasks.prebuildtask import UpdateAction

ConfigTask.task='alive'
ConfigTask.info="Updating servers..."

ConfigTask.action=[UpdateAction]