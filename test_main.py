from pytest import mark

from main import parse_txt_into_swagger, transform


@mark.parametrize(
    "schema",
    [
        """Schema(hello="world")""",
        """Schema(world=true,Property(hello=true))""",
        """Schema(Property(hello=true))""",
    ],
)
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
    assert res
    snapshot.assert_match(res)
