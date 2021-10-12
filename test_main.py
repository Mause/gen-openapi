from main import transform


def test_simple(snapshot):
    snapshot.assert_match(
        transform(
            """

Schema(hello="world")

    """
        )
    )
