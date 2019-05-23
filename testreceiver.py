import receiver


def test_query_01():
    cmd = '{ "*query" : { "Building": { "*[1]": { "Name" : {} } } } }'
    assert receiver.handle_cmd(cmd) == '"PAN"'

def test_query_02():
    cmd = '{ "*query" : { "Building": { "*[1]": { "Room": {} } } } }'
    assert receiver.handle_cmd(cmd) == '{"~arr": {"~len": 3}}'

def test_query_03():
    cmd = '{ "*query" : { "Building" : { "*[2]": { "Room": { "*[0]": { "Number": {} } } } } } }'
    assert receiver.handle_cmd(cmd) == '301'

def test_query_04():
    cmd = '{ "*query" : { "Building" : {} } }'
    assert receiver.handle_cmd(cmd) == '{"~arr": {"~len": 3}}'

def test_query_05():
    cmd = '{ "*query" : { "Building" : { "*[1]" : {} } } }'
    assert receiver.handle_cmd(cmd) == '{"Name": "PAN", "Room": {"~arr": {"~len": 3}}}'