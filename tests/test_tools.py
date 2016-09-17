from news_website.operations.tools import NewsUrlCache


class TestNewsUrlCache():

    def test_initialization(self):
        print("test_initialization")
        test_size = 10
        cache = NewsUrlCache(test_size)
        print(cache)
        assert '%s' % cache == "The Queue's length is 10, used 0: []"
        assert cache.get_all() == []
        assert cache.size == 10 and cache.is_empty() is True

    def test_push(self):
        print("test_push")
        test_size = 10
        cache = NewsUrlCache(test_size)
        for i in range(5):
            cache.push(i)
            assert cache.is_contained(i) is True
        assert cache.size == 10 and cache.get_all() == [0, 1, 2, 3, 4]
        assert cache.is_full() is False

    def test_add_existed_ele(self):
        print("test_add_existed_ele")
        test_size = 10
        cache = NewsUrlCache(test_size)
        for i in range(5):
            cache.push(i)
        cache.push(0)  # 0 is exited
        print(cache)
        assert cache.__len__() == 5 and cache.count(0) == 1  # unique

    def test_full(self):
        print("test_full")
        test_size = 10
        cache = NewsUrlCache(test_size)
        for i in range(10):
            cache.push(i)
        print(cache)
        assert cache.is_full() is True
        cache.push(10)
        assert cache[0] == 1 and cache[-1] == 10
        assert cache.size == 10 and cache.is_full() is True

    def test_practice(self):
        print("test_practice")
        test_size = 10
        cache = NewsUrlCache(test_size)
        for i in range(10):
            cache.push(i)

        cache.push(10)
        assert cache[-1] == 10 and cache[0] == 1 and cache.is_full() is True

        cache.push(9)
        assert cache[-1] == 10 and cache[0] == 1 and cache.is_full() is True

        cache.push(3)
        assert cache[-1] == 10 and cache[0] == 1 and cache.is_full() is True

        cache.push(20)
        assert cache[-1] == 20 and cache[0] == 2 and cache.is_full() is True

if __name__=='__main__':
    test_cache = TestNewsUrlCache()
    test_cache.test_initialization()
    test_cache.test_push()
    test_cache.test_add_existed_ele()
    test_cache.test_full()
    test_cache.test_practice()

