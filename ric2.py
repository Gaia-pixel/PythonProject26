# 1 – Cammino con peso massimo e archi strettamente decrescenti
import networkx as nx
import copy

class Model:

    def __init__(self, grafo: nx.DiGraph):
        self._graph = grafo
        self._bestPath = []
        self._bestScore = 0

    def getCamminoPesoMassimoDecrescente(self, partenza):
        self._bestPath = []
        self._bestScore = 0
        parziale = [partenza]
        self._ricorsione_decrescente(parziale, float('inf'))
        return self._bestPath, self._bestScore

    def _ricorsione_decrescente(self, parziale, peso_precedente):
        ultimo = parziale[-1]
        for vicino in self._graph.successors(ultimo):
            peso = self._graph[ultimo][vicino]['weight']
            if vicino not in parziale and peso < peso_precedente:
                parziale.append(vicino)
                self._ricorsione_decrescente(parziale, peso)
                parziale.pop()

        punteggio = self._calcolaPeso(parziale)
        if punteggio > self._bestScore:
            self._bestScore = punteggio
            self._bestPath = copy.deepcopy(parziale)

    def _calcolaPeso(self, path):
        peso = 0
        for i in range(len(path)-1):
            peso += self._graph[path[i]][path[i+1]]['weight']
        return peso

# 2 - Cammino più lungo (massimo numero di archi, senza ripetizioni e senza cicli)
import networkx as nx
import copy

class Model:

    def __init__(self, grafo: nx.DiGraph):
        self._graph = grafo
        self._bestPath = []

    def getCamminoPiuLungo(self, partenza):
        self._bestPath = []
        parziale = [partenza]
        self._ricorsione_piu_lungo(parziale)
        return self._bestPath

    def _ricorsione_piu_lungo(self, parziale):
        # Aggiorno se il cammino corrente è più lungo di quello salvato
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        ultimo = parziale[-1]
        for vicino in self._graph.successors(ultimo):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione_piu_lungo(parziale)
                parziale.pop()


# 6B - con ricorsione
# raggiungibili da un nodo, stesso gruppo
import networkx as nx

class Model:

    def __init__(self, grafo: nx.Graph):
        self._graph = grafo
        self._visitati = set()

    def getComponenteConnessaDiNodo(self, nodo):
        self._visitati = set()
        self._dfs(nodo)
        return self._visitati

    def _dfs(self, nodo):
        self._visitati.add(nodo)
        for vicino in self._graph.neighbors(nodo):
            if vicino not in self._visitati:
                self._dfs(vicino)


# 7 - Componente connessa massima
import networkx as nx

class Model:

    def __init__(self, grafo: nx.Graph):
        # ⚠️ Deve essere un grafo NON orientato
        self._graph = grafo

    def getComponenteConnessaMassima(self):
        # Ritorna l'insieme di nodi della componente più grande
        componenti = nx.connected_components(self._graph)
        return max(componenti, key=len)
# 7B - con ricorsione
import networkx as nx

class Model:

    def __init__(self, grafo: nx.Graph):
        self._graph = grafo

    def getComponenteConnessaMassima(self):
        best = set()
        visitati_globale = set()

        for nodo in self._graph.nodes:
            if nodo not in visitati_globale:
                self._visitati = set()
                self._dfs(nodo)
                visitati_globale.update(self._visitati)
                if len(self._visitati) > len(best):
                    best = self._visitati.copy()

        return best

    def _dfs(self, nodo):
        self._visitati.add(nodo)
        for vicino in self._graph.neighbors(nodo):
            if vicino not in self._visitati:
                self._dfs(vicino)

# 8 -Sottinsieme massimo sotto soglia (di peso)
# valore massimo sotto peso limite, zaino
import copy

class Model:

    def __init__(self):
        self._bestVal = 0
        self._bestSubset = []

    def getSottinsiemeMassimo(self, nodi, soglia):
        """
        nodi: lista di tuple (nome, peso, valore)
        soglia: peso massimo ammissibile
        """
        self._bestVal = 0
        self._bestSubset = []
        self._ricorsione(nodi, 0, soglia, 0, [])
        return self._bestSubset, self._bestVal

    def _ricorsione(self, nodi, i, soglia_rimasta, valore_attuale, parziale):
        if i == len(nodi):
            if valore_attuale > self._bestVal:
                self._bestVal = valore_attuale
                self._bestSubset = copy.deepcopy(parziale)
            return

        nome, peso, valore = nodi[i]

        # Escludi nodo corrente
        self._ricorsione(nodi, i + 1, soglia_rimasta, valore_attuale, parziale)

        # Includi nodo se rientra nella soglia
        if peso <= soglia_rimasta:
            parziale.append(nome)
            self._ricorsione(nodi, i + 1, soglia_rimasta - peso, valore_attuale + valore, parziale)
            parziale.pop()

# 9 - componente connessa, poi ciclo con N archi con peso tot massimo come LAB 12
import copy

class Model:

    def __init__(self, grafo):
        self._graph = grafo
        self._bestCycle = []
        self._bestWeight = 0

    def getCicloDiLunghezzaN(self, partenza, N):
        self._bestCycle = []
        self._bestWeight = 0
        self._ricorsione([partenza], N)
        return self._bestCycle, self._bestWeight

    def _ricorsione(self, parziale, archi_rimasti):
        if archi_rimasti == 0:
            if parziale[-1] in self._graph[parziale[0]]:
                peso = self._calcolaPeso(parziale + [parziale[0]])
                if peso > self._bestWeight:
                    self._bestWeight = peso
                    self._bestCycle = copy.deepcopy(parziale)
            return

        ultimo = parziale[-1]
        for vicino in self._graph[ultimo]:
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione(parziale, archi_rimasti - 1)
                parziale.pop()

    def _calcolaPeso(self, path):
        peso = 0
        for i in range(len(path) - 1):
            peso += self._graph[path[i]][path[i+1]]['weight']
        return peso


# 10 ALTERNATIVA 3B- Cammino con durata totale ≤ MAX e valore massimo
import copy

class Model:

    def __init__(self, grafo):
        self._graph = grafo
        self._bestPath = []
        self._bestValue = 0

    def getCamminoConDurataMassima(self, partenza, durata_max):
        self._bestPath = []
        self._bestValue = 0
        self._ricorsione([partenza], 0, 0, durata_max)
        return self._bestPath, self._bestValue

    def _ricorsione(self, parziale, durata_attuale, valore_attuale, durata_max):
        if valore_attuale > self._bestValue:
            self._bestValue = valore_attuale
            self._bestPath = copy.deepcopy(parziale)

        ultimo = parziale[-1]
        for vicino in self._graph[ultimo]:
            if vicino not in parziale:
                durata = self._graph[ultimo][vicino]['duration']
                valore = self._graph[ultimo][vicino]['value']
                if durata_attuale + durata <= durata_max:
                    parziale.append(vicino)
                    self._ricorsione(parziale, durata_attuale + durata, valore_attuale + valore, durata_max)
                    parziale.pop()

# 11 - Cammino minimo (in peso) tra due nodi (dijkstra)
# cammino più breve, peso minimo
# vale anche per Digraph
import networkx as nx

class Model:

    def __init__(self, grafo: nx.Graph):
        self._graph = grafo

    def getCamminoMinimo(self, sorgente, destinazione):
        try:
            # Trova cammino minimo in peso tra sorgente e destinazione
            path = nx.dijkstra_path(self._graph, source=sorgente, target=destinazione, weight='weight')
            peso = nx.dijkstra_path_length(self._graph, source=sorgente, target=destinazione, weight='weight')
            return path, peso
        except nx.NetworkXNoPath:
            return None, float('inf')


# 11B - trova cammino minimo ma ricorsiva (no dijkstra)
import copy
class Model:

    def __init__(self, grafo):
        self._graph = grafo
        self._bestPath = []
        self._bestPeso = float('inf')

    def getCamminoMinimoRicorsivo(self, sorgente, destinazione):
        self._bestPath = []
        self._bestPeso = float('inf')
        self._ricorsione([sorgente], destinazione, 0)
        if self._bestPath:
            return self._bestPath, self._bestPeso
        else:
            return None, float('inf')

    def _ricorsione(self, parziale, destinazione, peso_attuale):
        # Taglio i rami troppo costosi
        if peso_attuale >= self._bestPeso:
            return

        ultimo = parziale[-1]

        if ultimo == destinazione:
            self._bestPeso = peso_attuale
            self._bestPath = copy.deepcopy(parziale)
            return

        for vicino in self._graph[ultimo]:
            if vicino not in parziale:
                peso = self._graph[ultimo][vicino]['weight']
                parziale.append(vicino)
                self._ricorsione(parziale, destinazione, peso_attuale + peso)
                parziale.pop()


# 12 - Cammino minimo con vincoli aggiuntivi (ricorsiva)
# peso minimo con max tappe o soglia
# Ad esempio: trova il cammino minimo in peso tra due nodi, ma solo se:
# Il cammino non supera un certo numero di nodi
# Il peso totale ≤ soglia

import copy

class Model:

    def __init__(self, grafo: nx.Graph):
        self._graph = grafo
        self._bestPath = []
        self._bestPeso = float('inf')

    def getCamminoVincolato(self, sorgente, destinazione, max_nodi, max_peso):
        self._bestPath = []
        self._bestPeso = float('inf')
        self._ricorsione([sorgente], destinazione, 0, max_nodi, max_peso)
        return self._bestPath, self._bestPeso

    def _ricorsione(self, parziale, destinazione, peso_attuale, max_nodi, max_peso):
        if len(parziale) > max_nodi or peso_attuale > max_peso:
            return

        if parziale[-1] == destinazione:
            if peso_attuale < self._bestPeso:
                self._bestPeso = peso_attuale
                self._bestPath = copy.deepcopy(parziale)
            return

        ultimo = parziale[-1]
        for vicino in self._graph[ultimo]:
            if vicino not in parziale:
                peso = self._graph[ultimo][vicino]['weight']
                parziale.append(vicino)
                self._ricorsione(parziale, destinazione, peso_attuale + peso, max_nodi, max_peso)
                parziale.pop()







