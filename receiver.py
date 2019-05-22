import re
import json

# Set the 'database' to the intial schema
_db = { "Building" : [
        { "Name" : "WIL",
          "Room" : [
            { "Number" : "103" },
            { "Number" : "104" },
            { "Number" : "105" }
          ]
        },
        { "Name" : "PAN",
          "Room" : [
            { "Number" : "733" },
            { "Number" : "831" },
            { "Number" : "1006" }
          ]
        },
        { "Name" : "337",
          "Room" : [
            { "Number" : "301" },
            { "Number" : "309" },
            { "Number" : "108" }
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
            return err('Invalid number of keys at base level. Expected exactly 1 key.')
        # Determine which type of request it is
        if j_cmd.keys()[0] == '*query':
            return query(j_cmd['*query'])
        elif j_cmd.keys()[0] == '*chg':
            return change(j_cmd['*chg'])
        elif j_cmd.keys()[0] == '*del':
            return delete(j_cmd['*del'])
        elif j_cmd.keys()[0] == '*add':
            return add(j_cmd['*add'])
        else:
            return err('Unrecognized base key. Expected "*query", "*chg", "*del", or "*add".')
    except ValueError:
        return err('Unable to parse json.')


def query(cmd, db=dict(_db)):
    if len(cmd) > 1:
        return err("Query contains more than one key at a level.")
    if len(cmd) == 0:
        return db
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
    return query(cmd, db)



def change(cmd):
    pass


def delete(cmd):
    pass


def add(cmd):
    pass


def err(msg):
    return '{ "~err" : { "~msg" : "%s" } }' % msg

print(handle_cmd('{ "*query" : { "Building" : { "*[1]" : {} } } }'))
