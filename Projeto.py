from PySimpleGUI import PySimpleGUI as sg
import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph()
g1 = nx.DiGraph()
g2 = nx.DiGraph()


class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = []
        self.antecessor = [[] for i in range(1, self.vertices + 1)]

    def adiciona_aresta(self, u, v, w):
        self.grafo.append([u, v, w])
        G.add_edge(u, v)
        self.antecessor[v].append([-1])

    def bellman_ford(self, origem, destino):

        infinito = float("Inf")
        custo = [infinito] * self.vertices
        custo[origem] = 0

        for c in range(self.vertices - 1):
            for u, v, w in self.grafo:
                if custo[u] != infinito and custo[v] > custo[u] + w:
                    self.antecessor[v] = u
                    custo[v] = custo[u] + w

        for u, v, w in self.grafo:
            if custo[u] != infinito and custo[u] + w < custo[v]:
                print("Ciclo negativo encontrado!")
                return False

        caminho = []

        j = destino
        while j != origem:
            caminho.append(j)
            j = self.antecessor[j]
        caminho.append(origem)
        lista_caminho = caminho[::-1]

        caminho_resul = []
        respostacaminho = "| "

        for c in range(len(lista_caminho)-1):
            for u, v, w in self.grafo:
                if u == lista_caminho[c] and v == lista_caminho[c+1]:
                    caminho_resul.append([u, v, w])
                    respostacaminho += f"{u} --> {v}: {w} | " + " "

        resposta = f"Origem: {origem} \nDestino: {destino} \nCusto do percurso: {custo[destino]}"
        return resposta, caminho_resul, respostacaminho


def adiciona_aresta_resul(u, v):
    g2.add_edge(u, v)


teste = 0
while teste == 0:
    sg.theme('DarkTeal12')
    layout = [
        [sg.Text("Ponto de Saída:"), sg.Input(key="vertice_inicio")],
        [sg.Text("Ponto de Chegada:"), sg.Input(key="vertice_destino")],
        [sg.Button("Calcular melhor rota")],
        [sg.Button("Mostrar Grafo")],
    ]

    janela = sg.Window("Escolha os pontos", layout)
    resposta = "Dados não fornecidos"

    while True:
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            teste = 1
            break
        if eventos == "Calcular melhor rota":

            Qtd_vertices = 94
            graph = Grafo(Qtd_vertices)

            arq = open("base_dados.txt")
            linhas = arq.readlines()

            for linha in linhas:
                resul = linha.split(" ")

                graph.adiciona_aresta(int(resul[0]), int(resul[1]), int(resul[2]))

            if int(valores["vertice_inicio"]) > Qtd_vertices or 0 > int(valores["vertice_inicio"]):
                print('Vértice fora do intervalo.')
            elif int(valores["vertice_destino"]) > Qtd_vertices or 0 > int(valores["vertice_destino"]):
                print('Vértice fora do intervalo.')
            else:
                vertice_inicio = int(valores["vertice_inicio"])
                vertice_destino = int(valores["vertice_destino"])
                resposta, caminho_resul, resposta_caminho = graph.bellman_ford(vertice_inicio, vertice_destino)

            break

        if eventos == 'Mostrar Grafo':
            Qtd_vertices = 94
            graph = Grafo(Qtd_vertices)

            arq = open("base_dados.txt")
            linhas = arq.readlines()

            for linha in linhas:
                resul = linha.split(" ")

                graph.adiciona_aresta(int(resul[0]), int(resul[1]), int(resul[2]))

            # Visualizar grafo
            for i in G.nodes:
                G.nodes[i]['smoking'] = False

            lista_metro = [0, 53, 51, 63, 68, 74, 77, 62]
            for c in lista_metro:
                G.nodes[c]['smoking'] = True
            color_map = []
            for i in G.nodes:
                if G.nodes[i]['smoking']:
                    color_map.append('magenta')
                else:
                    color_map.append('cyan')

            nx.draw(G, node_color=color_map, with_labels=True, node_size=300)
            plt.show()

    sg.theme('DarkTeal12')
    layout2 = [
        [sg.Text("Aresta: Peso")],
        [sg.Text(resposta_caminho)],
        [sg.Text(resposta)],
        [sg.Button("Fechar")],
        [sg.Button("Mostrar Grafo Somente do Caminho")],
        [sg.Button("Mostrar Caminho Dentro do Grafo Geral")],
        [sg.Button("Voltar")]
    ]

    janela2 = sg.Window("Escolha os pontos", layout2)

    while True:
        eventos, valores = janela2.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == "Fechar":
            teste = 1
            break
        if eventos == "Mostrar Grafo Somente do Caminho":
            for u,v,w in caminho_resul:
                g1.add_edge(u, v)

            nx.draw(g1,  with_labels=True, node_size=300)
            plt.show()

        if eventos == "Mostrar Caminho Dentro do Grafo Geral":

            lista_vertice = []
            for u, v, w in caminho_resul:
                if u not in lista_vertice:
                    lista_vertice.append(u)
                if v not in lista_vertice:
                    lista_vertice.append(v)

            arq = open("base_dados.txt")
            linhas = arq.readlines()

            for linha in linhas:
                resul = linha.split(" ")

                adiciona_aresta_resul(int(resul[0]), int(resul[1]))

            for i in g2.nodes:
                g2.nodes[i]['smoking'] = False

            for c in lista_vertice:
                g2.nodes[c]['smoking'] = True
            color_map = []
            for i in g2.nodes:
                if g2.nodes[i]['smoking']:
                    color_map.append('green')
                else:
                    color_map.append('cyan')

            nx.draw(g2, node_color=color_map, with_labels=True, node_size=300)
            plt.show()

        if eventos == "Voltar":
            break