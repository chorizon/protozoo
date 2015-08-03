#!/usr/bin/python3

from protozoo.configtask import ConfigTask, ConfigAction
from protozoo.configtasks.prebuildtask import Python3Action
from protozoo.configtasks.prebuildtask import ApacheAction

ConfigTask.task='apache'

ConfigTask.action=[Python3Action, ApacheAction]