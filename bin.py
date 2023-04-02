import gc


class Data:
    def __init__(self, id, location):
        self.id = id
        self.location = location


list_of_instance = []


def get_all_instance():

    for obj in gc.get_objects():
        if isinstance(obj, Data):
            list_of_instance.append(obj)
