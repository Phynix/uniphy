import collections


class SectionHolder(collections.UserDict):

    def __init__(self):
        super().__init__()
        # self.data = {}

    def __getitem__(self, item):
        # TODO: implement item access and storage
        new_item = self.data.get(item)
        return new_item

    def __setitem__(self, key, value):
        # TODO: implement proper storage
        if key is None:
            key = self.next_section_nr()
        self.data[key] = value

    # def __next__(self):
    #     for item in self.data.values():
    #         yield item

    def next_section_nr(self):
        # do some stuff here

        # dummy implementation
        if self.data:
            next_sec = sorted(self.data.keys())[-1] + 1
        else:
            next_sec = 0
        return next_sec


# TODO: make more sophisticated, create class?
def to_internal_position(position):
    """Convert positions to the internal list representation."""
    if not isinstance(position, (list, str, collections.deque)):
        position = [position]

    position = collections.deque(position)
    return position


class SectionPosition():

    def __init__(self):
        pass
