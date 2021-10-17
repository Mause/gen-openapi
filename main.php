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

class Genny
{
    public function __construct()
    {
        $this->parser = (new ParserFactory())->create(ParserFactory::PREFER_PHP7);
        $nameResolver = new PhpParser\NodeVisitor\NameResolver();
        $this->nodeTraverser = new PhpParser\NodeTraverser();
        $this->nodeTraverser->addVisitor($nameResolver);

        $this->nodeFinder = new NodeFinder();
        $this->evaluator = new ConstExprEvaluator();
        $this->docParser = new DocParser();
        $this->docParser->setImports(array("oa" => "OpenApi\Annotations"));
    }

    public function get_data()
    {
        $code = file_get_contents("https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Models/Invoice.php");
        try {
            $ast = $this->parser->parse($code);
        } catch (Error $error) {
            echo "Parse error: {$error->getMessage()}\n";
            return;
        }

        $ast = $this->nodeTraverser->traverse($ast);

        $classes = $this->nodeFinder->findInstanceOf($ast, Node\Stmt\Class_::class);
        $class = $classes[0];
        echo "class: " . $class->name->toString() . "\n";

        $name = "fillable";

        $field = $this->nodeFinder->findFirst($ast, function (Node $node) use ($name) {
            return $node instanceof Node\Stmt\PropertyProperty
            && $node->name->toString() === $name;
        });

        $array = $this->evaluator->evaluateSilently($field->default);

        echo implode(", ", $array) . "\n";
        echo "\n";

        $code = file_get_contents("https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/InvoiceSchema.php");

        $annotations = $this->docParser->parse($code, 'InvoiceSchema.php');
        echo $annotations[0]->toYaml() . "\n";

        return array("fillable" => $array);
    }
}

use Symfony\Component\Yaml\Yaml;

echo (new Yaml())->dump((new Genny())->get_data());
