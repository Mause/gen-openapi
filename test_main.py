from pytest import mark

from main import transform


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
