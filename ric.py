# ESEMPIO 1: Cammino con peso massimo e archi decrescenti
import copy

class Model:

    def __init__(self, grafo):
        self._graph = grafo
        self._bestPath = []
        self._bestScore = 0

    def getCamminoDecrescente(self, partenza):
        self._bestPath = []
        self._bestScore = 0
        parziale = [partenza]
        self._ricorsione_decrescente(parziale, float('inf'))
        return self._bestPath, self._bestScore

    def _ricorsione_decrescente(self, parziale, peso_precedente):
        ultimo = parziale[-1]

        for vicino, peso in self._graph[ultimo]:
            if vicino not in parziale and peso < peso_precedente:
                parziale.append(vicino)
                self._ricorsione_decrescente(parziale, peso)
                parziale.pop()

        # aggiorno soluzione migliore se necessario
        punteggio = self._calcolaPeso(parziale)
        if punteggio > self._bestScore:
            self._bestScore = punteggio
            self._bestPath = copy.deepcopy(parziale)

    def _calcolaPeso(self, path):
        peso = 0
        for i in range(len(path)-1):
            for vicino, w in self._graph[path[i]]:
                if vicino == path[i+1]:
                    peso += w
        return peso



# ESEMPIO 15 : Cammino massimo con al più T tappe tra due nodi
# peso massimo entro T spostamenti
import copy

class Model:

    def __init__(self, grafo):
        self._graph = grafo
        self._bestPath = []
        self._bestScore = 0

    def getCamminoConTappe(self, partenza, destinazione, T):
        self._bestPath = []
        self._bestScore = 0
        parziale = [partenza]
        self._ricorsione_con_tappe(parziale, destinazione, T)
        return self._bestPath, self._bestScore

    def _ricorsione_con_tappe(self, parziale, destinazione, tappe_rimaste):
        ultimo = parziale[-1]

        if tappe_rimaste < 0:
            return

        if ultimo == destinazione:
            punteggio = self._calcolaPeso(parziale)
            if punteggio > self._bestScore:
                self._bestScore = punteggio
                self._bestPath = copy.deepcopy(parziale)
            return

        for vicino, peso in self._graph[ultimo]:
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione_con_tappe(parziale, destinazione, tappe_rimaste - 1)
                parziale.pop()

    def _calcolaPeso(self, path):
        peso = 0
        for i in range(len(path)-1):
            for vicino, w in self._graph[path[i]]:
                if vicino == path[i+1]:
                    peso += w
        return peso

