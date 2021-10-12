# snapshottest: v1 - https://goo.gl/zC4yUc

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_simple[Schema(Property(hello=true))] 1"] = {
    "args": [{"args": [("hello", "true")], "type": "Property"}],
    "type": "Schema",
}

snapshots['test_simple[Schema(hello="world")] 1'] = {
    "args": [("hello", '"world"')],
    "type": "Schema",
}

snapshots["test_simple[Schema(world=true,Property(hello=true))] 1"] = {
    "args": [("world", "true"), {"args": [("hello", "true")], "type": "Property"}],
    "type": "Schema",
}
