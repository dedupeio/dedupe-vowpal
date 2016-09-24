import numpy
import random
import socket
import subprocess
import shlex
import time
from dedupe.labeler import ActiveLearner


class VowpalLearner(ActiveLearner):
    def __init__(self, data_model, candidates):
        self.data_model = data_model
        self.candidates = candidates

        self.distances = self.transform(candidates)
        self.importance = {}

        command = 'vw --active --loss_function logistic --port 26542 --mellowness 0.01 --quiet'
        self.vw = subprocess.Popen(shlex.split(command))
        time.sleep(1)

        self.sock = socket.create_connection(('127.0.0.1', 26542))


    def transform(self, pairs):
        distances = self.data_model.distances(pairs)
        vw_x = []
        for x in distances:
            inner = ' '.join('{}:{}'.format(j, value)
                             for j, value
                             in enumerate(x))
            vw_x.append('| {}\n'.format(inner))

        return vw_x


    def get(self):
        while True:
            i = random.randint(0, len(self.distances))
            x = self.distances[i]
            self.sock.sendall(x.encode())
            response = self.sock.recv(4096).decode()
            response = [float(each) for each in response.strip().split()]
            if len(response) > 1:
                self.importance[x] = response[1]
                self.distances.pop(i)

                uncertain_pair = self.candidates.pop(i)
                return [uncertain_pair]

    def mark(self, pairs, ys):
        X = self.transform(pairs)
        ys = [1 if y else -1 for y in ys]
        for x, y in zip(X, ys):
            importance = self.importance.pop(x, 1)
            example = '{} {} {}'.format(y, importance, x).encode()
            self.sock.sendall(example)

    def __len__(self):
         return len(self.candidates)
