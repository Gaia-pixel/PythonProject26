import copy


class Model:
    def __init__(self):
        self.graph = None
        self.idmap = {}

    def get_qualcosa(self):
        return DAO.get_qualcosa()

    def buildGraph(self, parametro1, parametro2):
        # creo il grafo come mi serve
        self.graph = nx.DiGraph()
        # prendo i nodi dal db e li aggiungo al grafo
        allNodes = DAO.getAllNodes(parametro1, parametro2)
        self.graph.add_nodes_from(allNodes)
        # riempio la mappa
        for n in allNodes:
            self.idmap[n.id] = n
        # prendo gli archi con i rispettivi pesi dal db e li aggiungo al grafo
        allArchi = DAO.getAllArchi(parametro1, parametro2)
        self.graph.add_edges_from(allArchi)

        # oppure
        lista = DAO.getAllArchi(parametro1, parametro2)
        for n1, n2, p in lista:
            self.graph.add_edge(self.idmap[n1], self.idmap[n2], weight=p)


    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()
    def getNodes(self):
        return self.graph.nodes()

    # punto c
    def getMaxComponente(self):
        componenti = list(nx.connected_components(self.graph))
        componenteCorretta = []
        for c in componenti:
            if len(list(c)) > len(componenteCorretta):
                componenteCorretta = c
        self.cc = componenteCorretta  # mi serviva per la ricorsione dopo
        nodiConPesi = []
        for n in componenteCorretta:  # restituisco lista con i nodi della componente in ordine decr di peso
            pesoMin = None
            for vicino in nx.neighbors(self.graph, n):
                if pesoMin is None or self.graph[vicino][n]['weight'] < pesoMin:
                    pesoMin = self.graph[vicino][n]['weight']
            nodiConPesi.append((n, pesoMin))
        nodiConPesi.sort(key=lambda x: x[1], reverse=True)
        return nodiConPesi

    # cammino peso minimo
    def getShortestPath(self, u, v):
        path = nx.dijkstra_path(self.graph, source=u, target=v, weight='weight')
        total_weight = nx.dijkstra_path_length(self._graph, source=sorgente, target=destinazione, weight='weight')
        return path, total_weight


    # cammino minimo in numero di archi (non ha senso perchè sarebbe 0 (?))
    def getShortestPath(self, sorgente, destinazione):
        path = nx.shortest_path(self.graph, source=sorgente, target=destinazione)
        return path
    def getPath(self, n1, n2):
        path = nx.dijkstra_path(self.graph, n1, n2, weight=None)
        # path = nx.shortest_path(self._graph, n1, n2, weight = None))
        return path

    # cammino qualsiasi tra due nodi
    def getPath(self, n1, n2):  # cammino ottimo che minimizza la somma dei pesi sugli archi
        path = nx.dijkstra_path(self.graph, n1, n2)
        # path = nx.shortest_path(self._graph, n1, n2)

    # ordino i nodi per numero di archi uscenti decrescente
    def getAllNodesByOutDegree(self):
        # Ritorna i nodi ordinati in base al grado uscente (numero archi uscenti)
        nodes = list(self.graph.nodes)
        nodes.sort(key=lambda n: self.graph.out_degree(n), reverse=True)
        return nodes

    # cammino piu lungo senza tenere conto del peso
    def getCammino(self, nodo):
        cammino = nx.dfs_tree(self.graph, nodo)  # cammino più lungo
        n = list(cammino.nodes()) # tree : grafo connesso, non diretto
        return n

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self.graph, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]  # non tengo conto del primo elemento

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self.graph, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:] # non tengo conto del primo elemento

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self.graph, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self.graph, source)
        res = []
        for u, v in archi:
            res.append(v)
        return res

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self.graph, source)
        res = []
        for u, v in archi:
            res.append(v)
        return res



    def sort_list(lista):
        return lista.sort(key=lambda x: x[1], reverse=True)  # decrescente


    # ricorsione
    # utili lab11 e lab12

    def calcolaPeso(self, parziale):
        pesoTot = 0
        for i in range(len(parziale)-1):
            nodo1 = parziale[i]
            nodo2 = parziale[i+1]
            pesoTot += self.graph[nodo1][nodo2]['weight']
        return pesoTot

