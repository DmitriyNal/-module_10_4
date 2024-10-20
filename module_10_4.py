import time
from random import randint
from threading import Thread
from queue import Queue


#  Класс Table - стол, хранит информацию о находящемся за ним гостем (Guest).
class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


# Класс Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


# Класс Cafe - кафе, в котором есть определённое кол-во столов
# и происходит имитация прибытия гостей (guest_arrival) и их обслуживания (discuss_guests)
class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def check_table(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False

    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or self.check_table():
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    table.guest = None
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        print(f'{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                        table.guest = new_guest
                        new_guest.start()
                    break


if __name__ == '__main__':
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()
