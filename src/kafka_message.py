import time


class IntervalQueue:
    """
    创建一个“时间”队列，指定这个队列只包含固定时长（interval）的数据.
    每次调用get方法时获取这个队列
    """
    def __init__(self, interval=10) -> None:
        self.interval = interval
        self.item_lst = []

    def put(self, item) -> None:
        if self.size() > 0:
            self.first_put_time = self.item_lst[0][1]
        self.item_lst.append((item, int(time.time())))

    def get(self) -> list:
        last_item = list(filter(self.__filter_f, self.item_lst))[-1][0]
        self.item_lst = []
        return last_item

    def __filter_f(self, item_tuple: tuple) -> bool:
        item_time = item_tuple[1]
        return item_time < self.first_put_time + self.interval

    def size(self) -> int:
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
