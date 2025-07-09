import networkx as nx
import copy

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0

    def buildGraph(self, parametro=None):
        self._graph.clear()
        self._idMap.clear()
        nodi = DAO.getAllNodi(parametro)
        for n in nodi:
            self._idMap[n.id] = n
        self._graph.add_nodes_from(nodi)
        archi = DAO.getAllArchi(parametro, self._idMap)
        for sorgente, destinazione, peso in archi:
            self._graph.add_edge(sorgente, destinazione, weight=peso)

    def getPathScore(self, cammino):
        score = 0
        for i in range(len(cammino) - 1):
            if self._graph.has_edge(cammino[i], cammino[i + 1]):
                score += self._graph[cammino[i]][cammino[i + 1]].get("weight", 0)
        return score

    # PER GRAFI NON ORIENTATI
    # componente connessa di un nodo
    def getComponenteConnessaDFS(self, nodo_id):
        nodo = self._idMap[int(nodo_id)]
        visitati = set()
        self._dfs(nodo, visitati)
        return list(visitati)

    def _dfs(self, nodo, visitati):
        visitati.add(nodo)
        for vicino in self.graph.neighbors(nodo):
            if vicino not in visitati:
                self._dfs(vicino, visitati)

    def getSizeComponenteDFS(self, nodo_id):
        return len(self.getComponenteConnessaDFS(nodo_id))

    # componente massima
    def getComponenteMassima(self):
        visitati_globali = set()
        max_componente = []
        for nodo in self.graph.nodes:
            if nodo not in visitati_globali:
                visitati_corrente = set()
                self._dfsComponente(nodo, visitati_corrente)
                if len(visitati_corrente) > len(max_componente):
                    max_componente = list(visitati_corrente)
                visitati_globali.update(visitati_corrente)
        return max_componente

    def _dfsComponente(self, nodo, visitati):
        visitati.add(nodo)
        for vicino in self.graph.neighbors(nodo):
            if vicino not in visitati:
                self._dfsComponente(vicino, visitati)

    # peso totale componente
    def getPesoComponente(self, nodo_id):
        component = set(self.getComponenteConnessaDFS(nodo_id))
        peso = 0
        for u, v, d in self.graph.edges(data=True):
            if u in component and v in component:
                peso += d.get("weight", 0)
        return peso

# PER GRAFI ORIENTATI
import networkx as nx
import copy

class Model:
    def __init__(self):
        self._graph = None
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0
        self._allPaths = []
        self._pathCount = 0

    def buildGraph(self, parametro=None, orientato=True):
        self.graph = nx.DiGraph() if orientato else nx.Graph()
        self._idMap.clear()
        nodi = DAO.getAllNodi(parametro)
        for n in nodi:
            self._idMap[n.id] = n
        self.graph.add_nodes_from(nodi)
        archi = DAO.getAllArchi(parametro, self._idMap)
        for sorgente, destinazione, peso in archi:
            self.graph.add_edge(sorgente, destinazione, weight=peso)

    def getPathScore(self, cammino):
        score = 0
        for i in range(len(cammino) - 1):
            score += self.graph[cammino[i]][cammino[i + 1]]["weight"]
        return score

    # Ricorsione per componente connessa (trattando il grafo orientato come non orientato)
    def getComponenteConnessaDFS(self, nodo_id):
        nodo = self._idMap[int(nodo_id)]
        visitati = set()
        grafo_non_orientato = self.graph.to_undirected()
        self._dfsComponente(nodo, visitati, grafo_non_orientato)
        return list(visitati)

    def getSizeComponenteDFS(self, nodo_id):
        return len(self.getComponenteConnessaDFS(nodo_id))

    # per la componente massima
    def getComponenteMassima(self):
        grafo_non_orientato = self.graph.to_undirected()
        visitati_globali = set()
        max_componente = []

        for nodo in grafo_non_orientato.nodes:
            if nodo not in visitati_globali:
                visitati_corrente = set()
                self._dfsComponente(nodo, visitati_corrente, grafo_non_orientato)
                if len(visitati_corrente) > len(max_componente):
                    max_componente = list(visitati_corrente)
                visitati_globali.update(visitati_corrente)

        return max_componente

    def _dfsComponente(self, nodo, visitati, grafo):
        visitati.add(nodo)
        for vicino in grafo.neighbors(nodo):
            if vicino not in visitati:
                self._dfsComponente(vicino, visitati, grafo)

    # peso tot componente
    def getPesoComponente(self, nodo_id):
        component = set(self.getComponenteConnessaDFS(nodo_id))
        peso = 0
        for u, v, d in self.graph.edges(data=True):
            if u in component and v in component:
                peso += d.get("weight", 0)
        return peso