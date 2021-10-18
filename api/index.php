<?php

use Pecee\SimpleRouter\SimpleRouter;

require_once __DIR__ . '/main.php';

SimpleRouter::get(
    "/api/main",
    function () {
        return main($logger);
    }
);

SimpleRouter::start();
