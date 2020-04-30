import os
from multiprocessing import Process, Pipe
from typing import Type


class Volatility_calculation(Process):
    pathDir: Type[str] = '/'
    maximumNumberOfProcesses: Type[int] = 3

    def __init__(self, file_name, conn, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.file = file_name
        self.conn = conn
    def run(self):
        self.conn.send([self.file, self.name])
        self.conn.close()



if __name__ == '__main__':
    volatility_file, pipes = [], []
    files = os.listdir('trades')
    for name in files:
        parent_conn, child_conn = Pipe()
        new_file = Volatility_calculation(file_name=name, conn=child_conn)
        volatility_file.append(new_file)
        pipes.append(parent_conn)
    for i in volatility_file:
        i.start()
    for conn in pipes:
        name, num = conn.recv()
        print(f'Файл - {name} читаем в процессе - {num}')
