<?php

use PhangoApp\PhaModels\Webmodel;
use PhangoApp\PhaRouter\Routes;

Routes::$root_url='/';

Routes::$app='chorizon/pastafari';

Routes::$apps=['chorizon/pastafari'];

/**
* Configure database. You can configure multiple databases for different models.
*/ 

Webmodel::$host_db['default']='localhost';
	
Webmodel::$db['default']='default';

Webmodel::$login_db['default']='root';

Webmodel::$pass_db['default']='';

define('ADMIN_FOLDER', 'admin');

# Secret key of this server

define('SECRET_KEY', 'secret_key');

define('SECRET_KEY_HASHED_WITH_PASS', 'the_pass');

?>
