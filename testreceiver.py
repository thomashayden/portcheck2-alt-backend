import receiver

import copy
import pytest


std_dict = {"Building": [
        {"Name": "WIL",
         "Room": [
             {"Number": 103},
             {"Number": 104},
             {"Number": 105}
          ]
        },
        {"Name": "PAN",
         "Room": [
             {"Number": 733},
             {"Number": 831},
             {"Number": 1006}
          ]
        },
        {"Name": 337,
         "Room": [
             {"Number": 301},
             {"Number": 309},
             {"Number": 108}
          ]
        }
      ]
    }

@pytest.fixture()
def resource():
    receiver._db = copy.copy(std_dict)
    yield "resource"

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

def test_change_01():
    cmd = '{ "*query" : { "Building" : { "*[1]" : {} } } }'
    assert receiver.handle_cmd(cmd) == '{"Name": "PAN", "Room": {"~arr": {"~len": 3}}}'
    cmd = '{ "*chg" : { "Building" : { "*[1]" : { "Name" : "YMC" } } } }'
    receiver.handle_cmd(cmd)
    cmd = '{ "*query" : { "Building" : { "*[1]" : {} } } }'
    assert receiver.handle_cmd(cmd) == '{"Name": "YMC", "Room": {"~arr": {"~len": 3}}}'
    cmd = '{ "*chg" : { "Building" : { "*[1]" : { "Room" : { "*[0]" : { "Number" : 302 } } } } } }'
    assert receiver.handle_cmd(cmd) == '302'
