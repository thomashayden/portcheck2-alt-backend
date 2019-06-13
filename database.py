import os
import json


def val_from_file(path, arg):
    # Read the data file and return if it is in it or error otherwise
    try:
        with open(path) as f:
            try:
                js_data = json.load(f)
                try:
                    return js_data[arg]
                except KeyError:
                    raise IndexError("Data point %s not found in file %s" % (arg, path))
            except ValueError:
                raise IndexError("No valid data file found for %s" % arg)
    except IOError:
        raise IndexError("No value found for key %s" % arg)


class Database:
    # Implement as much of dir(dict()) as is needed

    def __init__(self, db_dir):
        self._db_dir = db_dir

    def __getitem__(self, arg):
        # Traverse to a sub-folder or the data stored in a ~data file
        # Raise IndexError if not exist
        if not isinstance(arg, str) and not isinstance(arg, int):
            raise TypeError("Invalid key type. Must be str or int")
        contents = os.listdir(self._db_dir)
        if arg in contents:
            return Database(self._db_dir + "/" + arg)
        else:
            val_from_file(self._db_dir + "/~data", arg)

    def __setitem__(self, key, value):
        # Set the given key to the value. Value can't be an atomic value
        if not isinstance(key, str):
            raise TypeError("Invalid key type. Must be str!")
        # TODO: Complete the method
