import time


class IntervalQueue:
    def __init__(self, interval=10):
        self.first_put_time = None
        self.interval = interval
        self.item_lst = []

    def put(self, item):
        if self.size() > 0:
            self.first_put_time = self.item_lst[0][1]
        self.item_lst.append((item, int(time.time())))

    def get(self):
        last_item = list(filter(self.filter_f, self.item_lst))[-1][0]
        self.item_lst = []
        return last_item

    def filter_f(self, item_tuple: tuple):
        item_time = item_tuple[1]
        return item_time < self.first_put_time + self.interval

    def size(self):
        return len(self.item_lst)


if __name__ == '__main__':
    a = IntervalQueue(10)
    for i in range(12):
        a.put(i + 20)
        time.sleep(1)

    print(a.item_lst)
    print(a.get())
    print(a.item_lst)

    for i in range(12):
        a.put(i + 40)
        time.sleep(1)

    print(a.item_lst)
    print(a.get())
