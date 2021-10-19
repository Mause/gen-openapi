<?php

declare(strict_types=1);
use PHPUnit\Framework\TestCase;

final class MainTest extends TestCase
{
    public function testMain(): void
    {
        $_SERVER['http-host'] = 'localhost';
        $_SERVER['request-uri'] = "http://localhost/api/main/model/Invoice/schema/InvoiceSchema";
        $_SERVER['request-method'] = 'GET';

        $thing = require __DIR__  . '/../api/index.php';
        $this->assertNotNull($thing);
    }
}
