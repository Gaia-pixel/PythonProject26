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


    # cammino più corto
    def getShortestPath(self, u, v):
        return nx.single_source_dijkstra(self.graph, u, v)

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

