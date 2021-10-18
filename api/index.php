<?php

use Pecee\SimpleRouter\SimpleRouter;
use Monolog\Logger;
use Monolog\Handler\StreamHandler;

require_once __DIR__ . '/main.php';

$logger = new Logger('SimpleLogger');
if (getenv("VERCEL")) {
    $filename = '/tmp/server.log';
} else {
    $filename = __DIR__.'/server.log';
}
$logger->pushHandler(new StreamHandler($filename, Logger::DEBUG));

SimpleRouter::get(
    "/api/main",
    function () use ($logger) {
        return main($logger);
    }
);

SimpleRouter::start();
