<?php

declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use PhpParser\Error;
use PhpParser\NodeDumper;
use PhpParser\ParserFactory;
use PhpParser\Node;
use PhpParser\NodeFinder;
use PhpParser\ConstExprEvaluator;
use PhpParser\ConstExprEvaluationException;
use Doctrine\Common\Annotations\DocParser;

$code = file_get_contents("https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Models/Invoice.php");

$parser = (new ParserFactory())->create(ParserFactory::PREFER_PHP7);
try {
    $ast = $parser->parse($code);
} catch (Error $error) {
    echo "Parse error: {$error->getMessage()}\n";
    return;
}

$nameResolver = new PhpParser\NodeVisitor\NameResolver();
$nodeTraverser = new PhpParser\NodeTraverser();
$nodeTraverser->addVisitor($nameResolver);
$ast = $nodeTraverser->traverse($ast);

$nodeFinder = new NodeFinder();

$classes = $nodeFinder->findInstanceOf($ast, Node\Stmt\Class_::class);
$class = $classes[0];
echo "class: " . $class->name->toString() . "\n";

$name = "fillable";

$field = $nodeFinder->findFirst($ast, function (Node $node) use ($name) {
    return $node instanceof Node\Stmt\PropertyProperty
        && $node->name->toString() === $name;
});

$evaluator = new ConstExprEvaluator();
$array = $evaluator->evaluateSilently($field->default);

echo implode(", ", $array) . "\n";
// $dumper = new NodeDumper;
// echo $dumper->dump($field) . "\n";

echo "\n";

$code = file_get_contents("https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/InvoiceSchema.php");

$docParser = new DocParser();
$docParser->setImports(array("oa" => "OpenApi\Annotations"));
$annotations = $docParser->parse($code, 'InvoiceSchema.php');
echo $annotations[0]->toYaml() . "\n";
