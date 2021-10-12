from main import transform


def test_simple(snapshot):
    schemata = transform("""Schema(hello="world")""")
    assert schemata
    snapshot.assert_match(schemata)
