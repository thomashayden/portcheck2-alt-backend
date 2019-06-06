class Database:
    # Implement as much of dir(dict()) as is needed

    def __init__(self, db_dir):
        self._db_dir = db_dir

    def __getitem__(self, arg):
        # Traverse to a sub-folder or the data stored in a ~data file
        pass
