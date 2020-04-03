from tkinter import filedialog
from tkinter import *
import networkx as nx
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

class App:
    def __init__(self, root):
        self.data = None
        self.nodeAmount = None
        self.graphData = list()
        self.graphDict = defaultdict(list)
        self.processed = False
        self.maxTreePrimProcessed = False
        self.postmanProblemProcessed = False
        self.komivoyagerProblemProcessed = False
        self.graphLabelString = ''
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.errorMessage = ('Файл даних не вибрано!',
                             'Дані вже оброблено!',
                             'Дані не оброблено!',
                             'Алгоритм вже задіяно!')
        self.root = root
        self.root.title('Дискретні моделі в системному проектуванні. Лаб 4.')
        self.root.minsize(width=500, height=300)
        self.root.configure(background='white')

        self.bW, self.bFg, self.bBg, self.bAb, self.bF = 40, 'white', 'RoyalBlue', 'RoyalBlue4', ('Arial', 10)

        self.openFileAndProcessDataButton = Button(self.root, text='Відкрити файл та обробити дані', command=self.openFileAndProccessData,
                                                   width=self.bW, fg=self.bFg, bg=self.bBg, activebackground=self.bAb, font=self.bF)
        self.maxTreePrimButton = Button(self.root, text='Максимальне остове дерево (Прима)', command=lambda: self.treePrim('max'),
                                        width=self.bW, fg=self.bFg, bg=self.bBg, activebackground=self.bAb, font=self.bF)
        self.minTreePrimButton = Button(self.root, text='Мінімальне остове дерево (Прима)', command=lambda: self.treePrim('min'),
                                        width=self.bW, fg=self.bFg, bg=self.bBg, activebackground=self.bAb, font=self.bF)
        self.postmanProblemButton = Button(self.root, text='Задача листоноші', command=self.postmanProblem,
                                           width=self.bW, fg=self.bFg, bg=self.bBg, activebackground=self.bAb, font=self.bF)
        self.komivoyagerProblem = Button(self.root, text='Задача комівояжера', command=self.komivoyagerProblem,
                                         width=self.bW, fg=self.bFg, bg=self.bBg, activebackground=self.bAb, font=self.bF)
        self.exitButton = Button(self.root, text='Вийти', command=self.root.quit,
                                 width=self.bW, fg=self.bFg, bg=self.bBg, activebackground=self.bAb, font=self.bF)
        self.logLabel = Label(self.root, bg='white')
        self.graphLabel = Label(self.root, bg='white', font=('Arial', 12))
        self.canvas = FigureCanvasTkAgg(figure(figsize=(5, 5)), master=self.root)

        self.openFileAndProcessDataButton.pack()
        self.maxTreePrimButton.pack()
        self.minTreePrimButton.pack()
        self.postmanProblemButton.pack()
        self.komivoyagerProblem.pack()
        self.exitButton.pack()
        self.logLabel.pack()
        self.graphLabel.pack(side=LEFT)
        self.canvas.get_tk_widget().pack(side=LEFT)

    def openFile(self):
        filename = filedialog.askopenfilename(
            initialdir='C:\\Users\\vihnatenko001\\Documents\\PycharmProjects\\IhnatenkoKN416', title='Select file',
            filetypes=(('data files', '*.data'), ('all files', '*.*')))

        with open(filename) as file:
            self.data = file.read()

        if self.processed:
            self.canvas.get_tk_widget().pack_forget()
            self.canvas = FigureCanvasTkAgg(figure(figsize=(5, 5)), master=self.root)
            self.canvas.get_tk_widget().pack(side=LEFT)

        self.processed = False
        self.maxTreePrimProcessed = False
        self.postmanProblemProcessed = False
        self.komivoyagerProblemProcessed = False
        self.graphData = list()
        self.graphDict = defaultdict(list)
        self.logLabel.config(text='Файл відкрито успішно.', fg='green')
        print('*** Зчитані данні:\n' + self.data)

    def processData(self):
        if self.data is not None:
            if not self.processed:
                self.data = [string.split(' ') for string in self.data.split('\n')]
                self.nodeAmount = len(self.data)
                print('*** Оброблені данні:\n#', self.nodeAmount, '\n', self.data)
                graph = nx.Graph()
                self.graphLabelString = ''
                counterY = 0

                for row in self.data:  # для кожної стрічки файлу
                    counterX = 0
                    counterLim = counterY  # щоб обробити лише верхню діагональ
                    for index in row:  # кожен елемент стрічки
                        if int(index) != 0:
                            if counterX >= counterLim:  # щоб побудувати граф лише по верхній діагоналі
                                graph.add_edge(self.alphabet[counterY], self.alphabet[counterX], weight=index)
                                self.graphLabelString += self.alphabet[counterY] + ' ↔ ' + self.alphabet[counterX] + '\t(' + str(index) + ')\n'
                                self.graphData.append([counterY, counterX, int(index)])
                            self.graphDict[counterY].append(counterX)
                        counterX += 1
                    counterY += 1

                print('*** Граф:\n' + self.graphLabelString)
                print('*** Дані графу:\n', self.graphData)
                nx.draw_networkx(graph, with_labels=True)
                self.canvas.draw()
                self.processed = True
                self.graphLabel.config(text=self.graphLabelString)
                self.logLabel.config(text='Граф побудовано успішно.', fg='green')
            else:
                self.logLabel.config(text=self.errorMessage[1], fg='red')
        else:
            self.logLabel.config(text=self.errorMessage[0], fg='red')

    def openFileAndProccessData(self):
        self.openFile()
        self.processData()

    def treePrim(self, operator):
        if self.data is not None:
            if self.processed is True:
                if not self.maxTreePrimProcessed:
                    graph = nx.Graph()
                    graphData = list()
                    tempGraphData = self.graphData.copy()
                    self.graphLabelString = ''
                    counter, index = 0, 0

                    if operator == 'max':
                        operatorValue = 0
                        while counter < len(tempGraphData) and tempGraphData[counter][0] == 0:
                            if tempGraphData[counter][2] > operatorValue:
                                operatorValue, index = tempGraphData[counter][2], counter
                            counter += 1
                    if operator == 'min':
                        operatorValue = 999
                        while counter < len(tempGraphData) and tempGraphData[counter][0] == 0:
                            if tempGraphData[counter][2] < operatorValue:
                                operatorValue, index = tempGraphData[counter][2], counter
                            counter += 1

                    graph.add_edge(self.alphabet[tempGraphData[index][0]], self.alphabet[tempGraphData[index][1]])
                    self.graphLabelString += self.alphabet[tempGraphData[index][0]] + ' ↔ ' + self.alphabet[tempGraphData[index][1]] + '\t(' + str(tempGraphData[index][2]) + ')\n'
                    graphData.append(tempGraphData[index])
                    del tempGraphData[index]

                    while tempGraphData:
                        counter, index, makeLoop = 0, 0, False
                        if operator == 'max':
                            operatorValue = 0
                            for node in tempGraphData:
                                if node [2] > operatorValue:
                                    operatorValue, index = tempGraphData[counter][2], counter
                                counter += 1
                        if operator == 'min':
                            operatorValue = 999
                            for node in tempGraphData:
                                if node [2] < operatorValue:
                                    operatorValue, index = tempGraphData[counter][2], counter
                                counter += 1

                        graph.add_edge(self.alphabet[tempGraphData[index][0]], self.alphabet[tempGraphData[index][1]])
                        try:
                            nx.find_cycle(graph)
                            graph.remove_edge(self.alphabet[tempGraphData[index][0]], self.alphabet[tempGraphData[index][1]])
                            makeLoop = True
                        except:
                            pass
                        if not makeLoop:
                            graphData.append(tempGraphData[index])
                            self.graphLabelString += self.alphabet[tempGraphData[index][0]] + ' ↔ ' + self.alphabet[tempGraphData[index][1]] + '\t(' + str(tempGraphData[index][2]) + ')\n'
                        del tempGraphData[index]
                        if len(graphData) == self.nodeAmount - 1:
                            break

                    self.canvas.get_tk_widget().pack_forget()
                    self.canvas = FigureCanvasTkAgg(figure(figsize=(5, 5)), master=self.root)
                    self.canvas.get_tk_widget().pack(side=LEFT)
                    nx.draw_networkx(graph, with_labels=True)
                    self.canvas.draw()
                    print('*** Дані утвореного графу:\n', graphData)
                    self.graphLabel.config(text=self.graphLabelString)
                    self.maxTreePrimProcessed = True
                    self.logLabel.config(text='Успішно.', fg='green')
                else:
                    self.logLabel.config(text=self.errorMessage[3], fg='red')
            else:
                self.logLabel.config(text=self.errorMessage[2], fg='red')
        else:
            self.logLabel.config(text=self.errorMessage[0], fg='red')

    def findEulerPath(self, node):
        for edge in self.graphDict[node]:
            self.graphDict[node].remove(edge)
            self.graphDict[edge].remove(node)
            self.findEulerPath(edge)
            self.graphLabelString += ' ' + str(node)

    def postmanProblem(self):
        if self.data is not None:
            if self.processed is True:
                if not self.postmanProblemProcessed:
                    self.graphLabelString = '0'
                    print(self.graphDict)
                    self.findEulerPath(0)
                    eulerPath = self.graphLabelString.split(' ')
                    graph = nx.Graph()

                    self.graphLabelString = ''
                    counter = 0
                    while counter < len(eulerPath)-1:
                        node1 = self.alphabet[int(eulerPath[counter])] + str(counter)
                        if counter+1 == len(eulerPath)-1:
                            node2 = self.alphabet[int(eulerPath[counter + 1])] + str(0)
                        else:
                            node2 = self.alphabet[int(eulerPath[counter+1])] + str(counter+1)
                        graph.add_edge(node1, node2)
                        self.graphLabelString += self.alphabet[int(eulerPath[counter])] + ' -> ' + self.alphabet[int(eulerPath[counter+1])] + '\n'
                        print(node1, node2)
                        counter += 1

                    print('*** Дані утвореного шляху:\n', eulerPath)
                    self.canvas.get_tk_widget().pack_forget()
                    self.canvas = FigureCanvasTkAgg(figure(figsize=(5, 5)), master=self.root)
                    self.canvas.get_tk_widget().pack(side=LEFT)
                    nx.draw_networkx(graph, with_labels=True)
                    self.canvas.draw()
                    self.graphLabel.config(text=self.graphLabelString)
                    self.postmanProblemProcessed = True
                    self.logLabel.config(text='Успішно.', fg='green')
                else:
                    self.logLabel.config(text=self.errorMessage[3], fg='red')
            else:
                self.logLabel.config(text=self.errorMessage[2], fg='red')
        else:
            self.logLabel.config(text=self.errorMessage[0], fg='red')

    def komivoyagerProblem(self):
        if self.data is not None:
            if self.processed is True:
                if not self.komivoyagerProblemProcessed:
                    intData = self.data.copy()
                    i = 0
                    while i < self.nodeAmount:
                        j = 0
                        while j < self.nodeAmount:
                            intData[i][j] = int(self.data[i][j])
                            j += 1
                        i += 1

                    Visited = [False] * self.nodeAmount
                    hamiltonPath = []

                    def hamilton(curr):
                        hamiltonPath.append(curr)
                        if len(hamiltonPath) == self.nodeAmount:
                            if intData[hamiltonPath[0]][hamiltonPath[-1]] != 0:
                                return True
                            else:
                                hamiltonPath.pop()
                                return False
                        Visited[curr] = True
                        for next in range(self.nodeAmount):
                            if intData[curr][next] != 0 and not Visited[next]:
                                if hamilton(next):
                                    return True
                        Visited[curr] = False
                        hamiltonPath.pop()
                        return False

                    komivoyagerPath = list()
                    pathWeight = 999
                    for node in range(self.nodeAmount):
                        hamiltonPath.clear()
                        Visited = [False] * self.nodeAmount
                        if hamilton(node):
                            weight = 0
                            i = 0
                            while i < self.nodeAmount - 1:
                                weight += intData[hamiltonPath[i]][hamiltonPath[i + 1]]
                                i += 1
                            print(weight, hamiltonPath)
                            if weight < pathWeight:
                                pathWeight = weight
                                komivoyagerPath = hamiltonPath.copy()

                    graph = nx.Graph()
                    self.graphLabelString = ''
                    counter = 0
                    while counter < self.nodeAmount - 1:
                        node1 = self.alphabet[komivoyagerPath[counter]]
                        node2 = self.alphabet[komivoyagerPath[counter + 1]]
                        graph.add_edge(node1, node2)
                        self.graphLabelString += node1 + ' -> ' + node2 + '\n'
                        counter += 1
                    self.graphLabelString += '(' + str(pathWeight) + ')'

                    print('*** Дані утвореного шляху:\n', komivoyagerPath)
                    self.canvas.get_tk_widget().pack_forget()
                    self.canvas = FigureCanvasTkAgg(figure(figsize=(5, 5)), master=self.root)
                    self.canvas.get_tk_widget().pack(side=LEFT)
                    nx.draw_networkx(graph, with_labels=True)
                    self.canvas.draw()
                    self.graphLabel.config(text=self.graphLabelString)
                    self.komivoyagerProblemProcessed = True
                    self.logLabel.config(text='Успішно.', fg='green')
                else:
                    self.logLabel.config(text=self.errorMessage[3], fg='red')
            else:
                self.logLabel.config(text=self.errorMessage[2], fg='red')
        else:
            self.logLabel.config(text=self.errorMessage[0], fg='red')

root = Tk()
app = App(root)
root.mainloop()
