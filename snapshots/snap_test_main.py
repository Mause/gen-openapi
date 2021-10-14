# snapshottest: v1 - https://goo.gl/zC4yUc

from snapshottest import GenericRepr, Snapshot

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

snapshots["test_tokeneyes[Schema(Property(hello=true))] 1"] = [
    GenericRepr("LexToken(NAME,'Schema',1,0)"),
    GenericRepr("LexToken(LBRACE,'(',1,6)"),
    GenericRepr("LexToken(NAME,'Property',1,7)"),
    GenericRepr("LexToken(LBRACE,'(',1,15)"),
    GenericRepr("LexToken(NAME,'hello',1,16)"),
    GenericRepr("LexToken(EQ,'=',1,21)"),
    GenericRepr("LexToken(BOOL,'true',1,22)"),
    GenericRepr("LexToken(RBRACE,')',1,26)"),
    GenericRepr("LexToken(RBRACE,')',1,27)"),
]

snapshots['test_tokeneyes[Schema(hello="world")] 1'] = [
    GenericRepr("LexToken(NAME,'Schema',1,0)"),
    GenericRepr("LexToken(LBRACE,'(',1,6)"),
    GenericRepr("LexToken(NAME,'hello',1,7)"),
    GenericRepr("LexToken(EQ,'=',1,12)"),
    GenericRepr("LexToken(STRING,'\"world\"',1,13)"),
    GenericRepr("LexToken(RBRACE,')',1,20)"),
]

snapshots["test_tokeneyes[Schema(world=true,Property(hello=true))] 1"] = [
    GenericRepr("LexToken(NAME,'Schema',1,0)"),
    GenericRepr("LexToken(LBRACE,'(',1,6)"),
    GenericRepr("LexToken(NAME,'world',1,7)"),
    GenericRepr("LexToken(EQ,'=',1,12)"),
    GenericRepr("LexToken(BOOL,'true',1,13)"),
    GenericRepr("LexToken(COMMA,',',1,17)"),
    GenericRepr("LexToken(NAME,'Property',1,18)"),
    GenericRepr("LexToken(LBRACE,'(',1,26)"),
    GenericRepr("LexToken(NAME,'hello',1,27)"),
    GenericRepr("LexToken(EQ,'=',1,32)"),
    GenericRepr("LexToken(BOOL,'true',1,33)"),
    GenericRepr("LexToken(RBRACE,')',1,37)"),
    GenericRepr("LexToken(RBRACE,')',1,38)"),
]
