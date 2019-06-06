import re
import json

# Set the 'database' to the initial schema
# This will obviously be replaced by a more efficient system (maybe an actual database), but it gets the idea across.

_db = {"Building": [
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


def handle_cmd(cmd):
    try:
        # Convert to an actual json structure
        j_cmd = json.loads(cmd)
        # Check that there is the correct number of base keys (can only perform one operation per request)
        if len(j_cmd) != 1:
            return _err('Invalid number of keys at base level. Expected exactly 1 key.')
        # Determine which type of request it is
        if j_cmd.keys()[0] == '*query':
            return json.dumps(_query(j_cmd['*query']))
        elif j_cmd.keys()[0] == '*chg':
            return json.dumps(_change(j_cmd['*chg']))
        elif j_cmd.keys()[0] == '*del':
            return json.dumps(_delete(j_cmd['*del']))
        elif j_cmd.keys()[0] == '*add':
            return json.dumps(_add(j_cmd['*add']))
        else:
            return _err('Unrecognized base key. Expected "*query", "*chg", "*del", or "*add".')
    except ValueError:
        return _err('Unable to parse json.')


def _query(cmd, db=dict(_db)):
    if len(cmd) > 1:
        return _err("Query contains more than one key at a level.")
    if len(cmd) == 0:
        if isinstance(db, list):
            return _arr(db)
        else:
            return _clean(db)
    key = cmd.keys()[0]
    re_mt = re.match(r'\*\[(\d+)\]', key)
    if re_mt:
        # An element in a list
        db = db[int(re_mt.group(1))]
    else:
        # A json key
        db = db[key]
    # Progress through the query
    cmd = cmd[key]
    return _query(cmd, db)


def _change(cmd, db=dict(_db)):
    pass


def _delete(cmd):
    pass


def _add(cmd):
    pass


def _err(msg):
    return {"~err": {"~msg": msg}}


def _arr(arr):
    return {"~arr": {"~len": len(arr)}}


def _clean(msg):
    if isinstance(msg, list):
        return _arr(msg)
    elif isinstance(msg, dict):
        n_dict = {}
        for key in msg.keys():
            n_dict[key] = _clean(msg[key])
        return n_dict
    else:
        return msg


if __name__ == "__main__":
    print(handle_cmd('{ "*query" : { "Building" : { "*[1]" : {} } } }'))
