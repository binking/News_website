# Be Careful: tools.py shouldn't use flask app context, it's for test


class NewsUrlCache(list):
    """
    A Queue whose length is fixed by size parameter.
    The instance saves some urls that was processed, and keep elements unique.
    """
    def __init__(self, size=100):
        list.__init__(self)
        self.size = size

    #def __getitem__(self, key):
    #    return list.__getitem__(self, key - 1)

    def is_contained(self, ele):
        """
        Adjust whether ele in list
        :param ele: the element to adjust
        :return: True / False
        """
        is_contained = True
        if self.__len__() == 0:  # Emtpy stack
            is_contained = False
        if ele not in self.__iter__():
            is_contained = False
        return is_contained

    def is_empty(self):
        if self.__len__():
            return False
        return True

    def is_full(self):
        if self.__len__() == self.size:
            return True
        return False

    def get_all(self):
        if self.__len__():
            return [ele for ele in self.__iter__()]
        else:
            return []

    def push(self, ele):
        if self.is_full():  # Full stack, pop the oldest and insert newest one
            if not self.is_contained(ele):
                self.pop(0)
                self.append(ele)
        else:  # able to insert
            if not self.is_contained(ele):
                self.append(ele)

    def __repr__(self):
        return "The Queue's length is {size}, used {usage}: {elements}".format(
            size=self.size,
            usage=self.__len__(),
            elements=[ele for ele in self.__iter__()]
        )