import itertools

import networkx as nx
import copy

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()  # o nx.Graph() se non orientato
        self._idMap = {}            # id → oggetto dominio (es. id → Airport)
        self._bestPath = []
        self._bestScore = 0
        #self._allNodes = [] mi serve se devo metterli in un dd ad esempio

    def buildGraph(self, parametro): # parametro opzionale
        self._graph.clear()

        # aggiungo i nodi
        nodi = DAO.getAllNodi(parametro)  # es. tutti i piloti / clienti / ordini
        for n in nodi:
            self._idMap[n.id] = n
        self._graph.add_nodes_from(nodi)

        # aggiungo gli archi
        allArchi = DAO.getAllArchi(parametro, self._idMap)
        for sorgente, destinazione, peso in allArchi:
            self._graph.add_edge(sorgente, destinazione, weight=peso)
        # oppure
        allArchi = DAO.getAllEdges(store, k)
        for a in allArchi:
            self._graph.add_edge(self._idMap[a.id1], self._idMap[a.id2], weight=a.peso)

        # se il grafo è completo ci sono tutti gli archi possibili
        # un arco collega ogni coppia di nodi distinti
        for u in nodi:
            for v in nodi:
                if u!=v:
                    self._graph.add_edge(u,v)
        # oppure se db grande
        allArchi = list(itertools.combinations(nodi, r=2))
        self._graph.add_edges_from(allArchi)
        # aggiungo poi il peso
        pesi = DAO.getPesi(parametro, self._idMap)
        for e in self._graph.edges:
            self._graph[e[0]][e[1]]["weight"] = pesi[e[0]]+pesi[e[1]]  # SE NEL DAO result = {} come in baseball

        """
        IL PESO è UGUALE AL NUMERO DI ARCHI CHE COLLEGANO I DUE NODI 
        
        allArchi = DAO.getAllEdges(self.idmapAirports)
        for e in allArchi:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                if self._graph.has_edge(e.aeroportoP, e.aeroportoD):
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)
        """

        def getAllArchi(self):  # da usare se ho un filtro sui nodi perchè se no mi ritrovo con nodi in più aggiunti
            allArchi = DAO.getAllEdges(self.idmapAirports)
            for e in allArchi:
                if e.aeroportoP in self._graph and e.aeroportoD in self._graph:  # mi chiedo se posso mettere l'arco ovvero se ho già i nodi
                    if self._graph.has_edge(e.aeroportoP, e.aeroportoD): # se c'è già aggiorno il peso
                        self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso
                    else:
                        self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        # nodes.sort(key=lambda x: x.IATA_CODE) oppure x.order_date, x.year, x.surname.lower()
        return nodes

    def getTeamsOfYear(self, year):  # e poi lo richiamo nel controller handleddyear selection
        self._allTeams = DAO.getTeamsOfYear(year)
        for t in self._allTeams:
            self._idMap[t.ID] = t
        return self._allTeams

    def getAllNodesByOutDegree(self):
        # Ritorna i nodi ordinati in base al grado uscente (numero archi uscenti)
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda n: self._graph.out_degree(n), reverse=True)
        return nodes

    def getAllNodesByScore(self):  # prestazione netta
        def calcola_score(nodo):
            score = 0
            for _, _, data in self._graph.out_edges(nodo, data=True):
                score += data["weight"]
            for _, _, data in self._graph.in_edges(nodo, data=True):
                score -= data["weight"]
            return score

        nodes = list(self._graph.nodes)
        nodes.sort(key=calcola_score, reverse=True)
        return nodes

    def getBestNodo(self):  # può essere bestDriver (quello con meno sconfitte)
        bestNodo = None
        bestScore = float('-inf')
        for n in self._graph.nodes:
            score = 0
            for e_out in self._graph.out_edges(n, data=True):
                score += e_out[2]["weight"]
            for e_in in self._graph.in_edges(n, data=True):
                score -= e_in[2]["weight"]
            if score > bestScore:
                bestScore = score
                bestNodo = n
        return bestNodo, bestScore

def getNeighborsSorted(self, source):  # vicini in ordine decr
    vicini = nx.neighbors(self._grafo, source)  # [v0 v1 v2 ...]
    # vicini = self._grafo.neighbors(source)

    viciniTuple = []

    for v in vicini:
        viciniTuple.append((v, self._grafo[source][v]["weight"]))  # [(v0, p0) (v1, p1) ()]

    viciniTuple.sort(key=lambda x: x[1], reverse=True)  # sorto per secondo elemento della tupla, ovvero peso, decr
    return viciniTuple

# componente connessa di un nodo (grafo non orientato)
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()  # o nx.DiGraph()
        self._idMap = {}  # id → oggetto (es. Product, Order...)

    def getConnectedComponent(self, id_selezionato):
        if id_selezionato not in self._idMap:
            return []

        nodo = self._idMap[id_selezionato]

        if nodo not in self._graph.nodes:
            return []

        component = nx.node_connected_component(self._graph, nodo)
        return sorted(component, key=lambda x: str(x))  # opzionale: ordinamento


    # dimensione della componente
    def getSizeComponente(self, nodo_id):
        componente = self.getConnectedComponent(nodo_id)
        return len(componente)

    # peso tot della componente
    def getPesoComponente(self, nodo_id):
        component = self.getConnectedComponent(nodo_id)
        peso = 0
        for u, v, d in self._graph.edges(data=True):
            if u in component and v in component:
                peso += d["weight"]
        return peso

    # componente connessa massima grafo non orientato
    def getMaxConnectedComponent(self):
        if self._graph.number_of_nodes() == 0:
            return []

        # Trova tutte le componenti connesse
        components = nx.connected_components(self._graph)

        # Prendi quella con più nodi
        max_component = max(components, key=len)

        return sorted(max_component, key=lambda x: str(x))  # opzionale: ordina

    # cammino qualsiasi tra due nodi
    def getPath(self, n1, n2):  # cammino ottimo che minimizza la somma dei pesi sugli archi
        path = nx.dijkstra_path(self._graph, n1, n2)
        # path = nx.shortest_path(self._graph, n1, n2)

        return path
    # cammino minimo in numero di archi
    def getPath(self, n1, n2):
        path = nx.dijkstra_path(self._graph, n1, n2, weight = None)
        # path = nx.shortest_path(self._graph, n1, n2, weight = None))

        return path

# cammino minimo in peso tra due nodi
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()  # o nx.DiGraph() se il grafo è orientato

    def getShortestWeightedPath(self, sorgente, destinazione):
        if sorgente not in self._graph.nodes or destinazione not in self._graph.nodes:
            return []

        try:
            # Trova il cammino minimo pesato
            path = nx.dijkstra_path(self._graph, source=sorgente, target=destinazione, weight='weight')
            total_weight = nx.dijkstra_path_length(self._graph, source=sorgente, target=destinazione, weight='weight')
            return path, total_weight

        except nx.NetworkXNoPath:
            return []

# cammino minimo in numero archi tra due nodi
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()

    def getShortestPath(self, sorgente, destinazione):
        if sorgente not in self._graph.nodes or destinazione not in self._graph.nodes:
            return []

        try:
            path = nx.shortest_path(self._graph, source=sorgente, target=destinazione)
            return path
        except nx.NetworkXNoPath:
            return []  # nessun cammino esistente









