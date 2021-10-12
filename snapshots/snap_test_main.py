# snapshottest: v1 - https://goo.gl/zC4yUc

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_php 1"] = [
    {
        "args": [
            ("schema", "Invoice"),
            ("type", "object"),
            {
                "args": [
                    ("property", "id"),
                    ("type", "string"),
                    ("example", "Opnel5aKBz"),
                    ("description", "_________"),
                ],
                "type": "Property",
            },
        ],
        "type": "Schema",
    }
]

snapshots["test_simple[Schema(Property(hello=true))] 1"] = {
    "args": [{"args": [("hello", "true")], "type": "Property"}],
    "type": "Schema",
}

snapshots['test_simple[Schema(hello="world")] 1'] = {
    "args": [("hello", "world")],
    "type": "Schema",
}

snapshots["test_simple[Schema(world=true,Property(hello=true))] 1"] = {
    "args": [("world", "true"), {"args": [("hello", "true")], "type": "Property"}],
    "type": "Schema",
}
