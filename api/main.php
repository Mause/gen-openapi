<?php

declare(strict_types=1);
require __DIR__ . '/../vendor/autoload.php';

use PhpParser\Error;
use PhpParser\NodeDumper;
use PhpParser\ParserFactory;
use PhpParser\Node;
use PhpParser\NodeFinder;
use PhpParser\ConstExprEvaluator;
use PhpParser\ConstExprEvaluationException;
use Doctrine\Common\Annotations\DocParser;
use Symfony\Component\Yaml\Yaml;
use OpenApi\Annotations\Property;
use Monolog\Logger;

class Genny
{
    public function __construct(Logger $logger)
    {
        $this->logger = $logger;
        $this->parser = (new ParserFactory())->create(ParserFactory::PREFER_PHP7);
        $nameResolver = new PhpParser\NodeVisitor\NameResolver();
        $this->nodeTraverser = new PhpParser\NodeTraverser();
        $this->nodeTraverser->addVisitor($nameResolver);

        $this->nodeFinder = new NodeFinder();
        $this->evaluator = new ConstExprEvaluator();
        $this->docParser = new DocParser();
        $this->docParser->setImports(array("oa" => "OpenApi\Annotations"));
    }

    public function get_data(String $modelName, String $baseSchemaName)
    {
        $code = file_get_contents("https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Models/$modelName.php");
        $ast = $this->parser->parse($code);

        $ast = $this->nodeTraverser->traverse($ast);

        $classes = $this->nodeFinder->findInstanceOf($ast, Node\Stmt\Class_::class);
        $class = $classes[0];
        $this->logger->info("class: " . $class->name->toString());

        $name = "fillable";

        $field = $this->nodeFinder->findFirst($ast, function (Node $node) use ($name) {
            return $node instanceof Node\Stmt\PropertyProperty
            && $node->name->toString() === $name;
        });

        $array = $this->evaluator->evaluateSilently($field->default);

        $this->logger->info(implode(", ", $array));

        $code = file_get_contents("https://github.com/invoiceninja/invoiceninja/raw/v5-develop/app/Http/Controllers/OpenAPI/$baseSchemaName.php");

        $annotations = $this->docParser->parse($code, $baseSchemaName);

        return array("fillable" => $array, "annotations" => $annotations);
    }
}

function back_to_string(OpenApi\Annotations\Schema $anno)
{
    if ($anno->type == "object") {
        $props = implode(",\n", array_map(function (OpenApi\Annotations\Property $prop) {
            return "        @OA\Property(property=\"$prop->property\", type=\"$prop->type\", example=\"$prop->example\", description=\"$prop->description\")";
        }, $anno->properties));
    }
    return "@OA\Schema(\n    schema=\"Fillable$anno->schema\",\n    type=\"$anno->type\",\n$props\n)";
}

function wrap_with_comment(String $comment)
{
    $lines = explode("\n", $comment);

    return "<?php\n/**\n * " . implode("\n * ", $lines) . "\n */";
}

function main(Logger $logger, String $modelName, String $baseSchemaName)
{
    $data = (new Genny($logger))->get_data($modelName, $baseSchemaName);
    $anno = $data["annotations"][0];

    $anno->properties = array_filter(
        $anno->properties,
        function (Property $property) use ($data, $logger) {
            $fillable = in_array($property->property, $data["fillable"], true);
            if (!$fillable) {
                $logger->info("$property->property is not fillable\n");
            }
            return $fillable;
        }
    );

    $stringer =  back_to_string($anno);
    return wrap_with_comment($stringer) . "\n";
}
