from protozoo.configtask import ConfigAction

Python3Action=ConfigAction()
Python3Action.codename='python3'
Python3Action.name='Python Language'
Python3Action.description='Script language very powerful, very used for spanel for internal tasks'
Python3Action.script_path='libraries/install_python.sh'
Python3Action.script_interpreter='sh'
Python3Action.parameters=[]
Python3Action.extra_files=[]

ApacheAction=ConfigAction()

ApacheAction.codename='apache'
ApacheAction.name='Apache Webserver'
ApacheAction.description='Script for install the most famous webserver in the world for debian jessie'
ApacheAction.script_path='libraries/install_apache.py'
ApacheAction.script_interpreter='python3'
ApacheAction.parameters=[]
ApacheAction.extra_files=['files/spanel.conf']

#ConfigPanel::$scripts['agent']['apache']=array('name' => 'Apache Webserver', 'description' => 'Script for install the most famous webserver in the world for debian jessie', 'script_path' => 'libraries/install_apache.py', 'script_interpreter' => 'python3', 'service' => 'webserver');

#ConfigPanel::$scripts['agent']['python3']=array('name' => 'Python Language', 'description' => 'Script language very powerful, very used for spanel for internal tasks', 'script_path' => 'libraries/install_python.sh', 'script_interpreter' => 'sh');

#ConfigPanel::$scripts['agent']['php']=array('name' => 'PHP', 'description' => 'Language used in web applications', 'script_path' => 'libraries/install_php.py', 'script_interpreter' => 'python3', 'parameters' => array(), 'extra_files' => array('files/spanel.conf'));