from pytest import mark, xfail

from main import main, parse_txt_into_swagger, tokeneyes, transform

strings = [
    ("""Schema(hello="world")"""),
    ("""Schema(world=true,Property(hello=true))"""),
    ("""Schema(Property(hello=true))"""),
]


@mark.parametrize("schema", strings)
def test_simple(snapshot, schema):
    schemata = transform(schema)
    assert schemata
    snapshot.assert_match(schemata)


def test_php(snapshot):
    php = r"""
    <?php
/**
 * @OA\Schema(
 *   schema="Invoice",
 *   type="object",
 *   @OA\Property(property="id", type="string", example="Opnel5aKBz", description="_________")
 * )
 */
 """
    res = list(parse_txt_into_swagger(php))
    assert all(res)
    snapshot.assert_match(res)


@mark.xfail(raises=SyntaxError)
def test_main(snapshot):
    with open("invoiceninja/InvoiceSchema.php") as fh:
        res = list(parse_txt_into_swagger(fh.read()))
    snapshot.assert_match(res)


@mark.parametrize(
    "schema",
    strings
    + [
        ("""Schema(Property(hello=true,),)"""),
    ],
)
def test_tokeneyes(snapshot, schema):
    tokens = list(iter(tokeneyes(schema), None))

    snapshot.assert_match(tokens)
