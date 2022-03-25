import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class CheckResidual:
    def __init__(self):
        self.data = []
        with open('log.run', 'r', encoding='utf-8') as file:
            self.log = file.read().split('\n')

    def get_data(self):
        step = {}
        most_wanted = ['p_rgh', 'omega', 'k']
        for row in self.log:
            if row.__contains__('ExecutionTime'):
                self.data.append(step)
                step = {}
            elif row.startswith('Time ='):
                step.update({"time": float(row.split()[-1])})
            elif any(f'Solving for {x}' in row for x in most_wanted):
                step.update({
                    row.split(',')[0].split(' ')[-1]: float(row.split(',')[2].split(' ')[-1])
                })

    def render_graph(self):
        graph_data = {'time': [], 'p_rgh': [], 'omega': [], 'k': []}

        for step in self.data:
            for gd in graph_data:
                graph_data[gd].append(step[gd])

        x = np.array(graph_data['time'])
        plt.figure(figsize=(9, 3))

        plt.subplot(131)
        plt.yscale('log')
        plt.xlabel("time")
        plt.ylabel("p_rgh")
        plt.grid(True)
        plt.plot(x, np.array(graph_data['p_rgh']))

        plt.subplot(132)
        plt.yscale('log')
        plt.xlabel("time")
        plt.ylabel("omega", color='red')
        plt.grid(True)
        plt.plot(x, np.array(graph_data['omega']), color='red')

        plt.subplot(133)
        plt.yscale('log')
        plt.xlabel("time")
        plt.ylabel("k", color='green')
        plt.grid(True)
        plt.plot(x, np.array(graph_data['k']), color='green')

        plt.subplots_adjust(top=0.970, bottom=0.16, left=0.09, right=0.97, hspace=0.2,
                            wspace=0.38)

        plt.show()

    def save_result(self):
        dt = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        with open(f'res_result_{dt}.csv', 'w+') as r_file:
            headers = ['time', 'p_rgh', 'omega', 'k']
            w = csv.DictWriter(r_file, fieldnames=headers)
            w.writeheader()
            for row in self.data:
                w.writerow(row)


if __name__ == '__main__':
    run = CheckResidual()
    run.get_data()
    run.save_result()
    run.render_graph()
