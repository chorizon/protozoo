<?php

ConfigPanel::$scripts['apache']['python3']=array('name' => 'Python Language', 'description' => 'Script language very powerful, very used for spanel for internal tasks', 'script_path' => 'libraries/install_python.sh', 'script_interpreter' => 'sh');

ConfigPanel::$scripts['apache']['apache']=array('name' => 'Apache Webserver', 'description' => 'Script for install the most famous webserver in the world for debian jessie', 'script_path' => 'libraries/install_apache.py', 'script_interpreter' => 'python3', 'service' => 'webserver');

ConfigPanel::$scripts['apache']['git']=array('name' => 'Git', 'description' => 'A modern CVS system created by Linus Torlvards', 'script_path' => 'libraries/install_git.py', 'script_interpreter' => 'python3');

//Install apaches that are basic scripts. The basic scripts are mysql and php websites servers.

//More scripts can be add_servers for add the servers created to a mysql database.

/*ConfigPanel::$scripts['apache']['apache']=array('name' => 'WPanel apache', 'description' => 'API used by the hosting control panel made with Phango Framework and python scripts', 'script_path' => 'apache/install_apache.sh', 'script_command' => 'sh install_apache.sh', 'parameters' => '--hostname_father=', 'extra_files' => 'webserver/apache.conf');*/

?>