import collections


class SectionHolder():

    def __init__(self):
        self.items = {}

    def __getitem__(self, item):
        # TODO: implement item access and storage
        new_item = self.items.get(item)
        return new_item

    def __setitem__(self, key, value):
        # TODO: implement proper storage
        self.items[key] = value


# TODO: make more sophisticated, create class?
def to_internal_position(position):
    """Convert positions to the internal list representation."""
    if not isinstance(position, (list, str, collections.deque)):
        position = [position]
    position = collections.deque(position)
    return position
