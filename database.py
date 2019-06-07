import os


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
            self.val_from_file(self._db_dir + "/~data")

    def val_from_file(self, path):
        # Read the data file and return if it is in it or error otherwise
        pass
