#  cammino massimo con vincolo su peso decrescente
def getBestPath(self, start):
    self._bestPath = []
    self._bestScore = 0
    partenza = self._idMap[int(start)]
    parziale = [partenza]

    for vicino in self._graph.neighbors(partenza):
        parziale.append(vicino)
        self._ricorsione(parziale)
        parziale.pop()

    return self._bestPath, self._bestScore


def _ricorsione(self, parziale):
    score = self.getPathScore(parziale)
    if score > self._bestScore:
        self._bestScore = score
        self._bestPath = copy.deepcopy(parziale)

    ultimo = parziale[-1]
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            peso_corrente = self._graph[parziale[-2]][parziale[-1]]["weight"]
            peso_nuovo = self._graph[ultimo][vicino]["weight"]

            # ESEMPIO1: vincolo su peso decrescente
            if peso_nuovo < peso_corrente:
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()

def getPathScore(self, cammino):  # xes cammino max con pesi decrescenti
    # sarebbe _getPeso
    """
    Calcola il punteggio (peso) totale di un cammino, sommando i pesi degli archi
    """
    score = 0
    for i in range(len(cammino) - 1):
        score += self._graph[cammino[i]][cammino[i + 1]]["weight"]
    return score

def getTeamScore(self, team): # per valutare il punteggio complessivo di un gruppo di nodi
    # Cerco un gruppo ottimo di nodi
    """
    Calcola la somma dei pesi dagli archi in ingresso al team da nodi esterni
    """
    score = 0
    for u, v, data in self._graph.edges(data=True):
        if u not in team and v in team:
            score += data["weight"]
    return score


# cammino massimo ma con peso sotto una soglia max_peso
def getBestPath(self, start, max_peso):
    self._bestPath = []
    self._bestScore = 0
    partenza = self._idMap[int(start)]
    parziale = [partenza]

    for vicino in self._graph.neighbors(partenza):
        peso = self._graph[partenza][vicino]["weight"]
        if peso <= max_peso:
            parziale.append(vicino)
            self._ricorsione(parziale, peso, max_peso)
            parziale.pop()

    return self._bestPath, self._bestScore

def _ricorsione(self, parziale, peso_attuale, max_peso):
    if peso_attuale > max_peso:
        return

    score = self.getPathScore(parziale)
    if score > self._bestScore:
        self._bestScore = score
        self._bestPath = copy.deepcopy(parziale)

    ultimo = parziale[-1]
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            peso_nuovo = self._graph[ultimo][vicino]["weight"]
            if peso_attuale + peso_nuovo <= max_peso:
                parziale.append(vicino)
                self._ricorsione(parziale, peso_attuale + peso_nuovo, max_peso)
                parziale.pop()

# cammino massimo ma con esattamente N archi (ciclo chiuso)
def getBestPath(self, start, N):
    self._bestPath = []
    self._bestScore = 0
    partenza = self._idMap[int(start)]
    parziale = [partenza]
    self._ricorsione(parziale, N)
    return self._bestPath, self._bestScore

def _ricorsione(self, parziale, N):
    if len(parziale) == N + 1:
        ultimo = parziale[-1]
        if parziale[0] in self._graph.neighbors(ultimo):
            parziale.append(parziale[0])  # chiudo il ciclo
            score = self.getPathScore(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            parziale.pop()
        return

    ultimo = parziale[-1]
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            parziale.append(vicino)
            self._ricorsione(parziale, N)
            parziale.pop()


# cammino massimo ma con al massimo T tappe (archi) DA UN NODO
def getBestPath(self, start, T):
    self._bestPath = []
    self._bestScore = 0
    partenza = self._idMap[int(start)]
    parziale = [partenza]
    self._ricorsione(parziale, T)
    return self._bestPath, self._bestScore

def _ricorsione(self, parziale, T):
    if len(parziale) > T + 1:
        return

    score = self.getPathScore(parziale)
    if score > self._bestScore:
        self._bestScore = score
        self._bestPath = copy.deepcopy(parziale)

    ultimo = parziale[-1]
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            parziale.append(vicino)
            self._ricorsione(parziale, T)
            parziale.pop()

# Cammino massimo con al più T tappe (archi = nodi+1) TRA DUE NODI
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
            if punteggio > self._bestScore and len(parziale) < tappe_rimaste:
                self._bestScore = punteggio
                self._bestPath = copy.deepcopy(parziale)
            return

        if len(parziale) > tappe_rimaste:
            return

        for vicino, peso in self._graph[ultimo]:
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione_con_tappe(parziale, destinazione, tappe_rimaste - 1)
                parziale.pop()

    def _calcolaPeso(self, path):  # somma i pesi degli archi della lista di nodi path
        peso = 0
        for i in range(0, len(path)-1):
            peso += self._graph[path[i]][path[i+1]]["weight"]
        return peso

        """
            for vicino, w in self._graph[path[i]]:
                if vicino == path[i+1]:
                    peso += w
        return peso
        
        """


# cammino massimo che passa per richiesto_id
def getBestPath(self, start, richiesto_id):
    self._bestPath = []
    self._bestScore = 0
    partenza = self._idMap[int(start)]
    richiesto = self._idMap[int(richiesto_id)]
    parziale = [partenza]
    self._ricorsione(parziale, richiesto)
    return self._bestPath, self._bestScore

def _ricorsione(self, parziale, richiesto):
    score = self.getPathScore(parziale)
    if richiesto in parziale and score > self._bestScore:
        self._bestScore = score
        self._bestPath = copy.deepcopy(parziale)

    ultimo = parziale[-1]
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            parziale.append(vicino)
            self._ricorsione(parziale, richiesto)
            parziale.pop()


# cammino massimo senza passare per vietato_id
def getBestPath(self, start, vietato_id):
    self._bestPath = []
    self._bestScore = 0
    partenza = self._idMap[int(start)]
    vietato = self._idMap[int(vietato_id)]
    parziale = [partenza]

    # Se il nodo di partenza è vietato, non ha senso iniziare
    if partenza == vietato:
        return [], 0

    self._ricorsione(parziale, vietato)
    return self._bestPath, self._bestScore

def _ricorsione(self, parziale, vietato):
    # Se ho visitato il nodo vietato, blocco subito
    if vietato in parziale:
        return

    score = self.getPathScore(parziale)
    if score > self._bestScore:
        self._bestScore = score
        self._bestPath = copy.deepcopy(parziale)

    ultimo = parziale[-1]
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale and vicino != vietato:
            parziale.append(vicino)
            self._ricorsione(parziale, vietato)
            parziale.pop()

# Cammino più lungo in archi (non peso)
    def getLongestPath(self, start_id):
        self._bestPath = []
        partenza = self._idMap[int(start_id)]
        self._ricorsioneLunga([partenza])
        return self._bestPath

    def _ricorsioneLunga(self, parziale):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
        ultimo = parziale[-1]
        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsioneLunga(parziale)
                parziale.pop()

# Cammino con durata totale ≤ MAX e valore massimo caso specifico LAB14
# SE "Seleziona il miglior sottoinsieme di nodi con durata (peso) totale ≤ D,
# numero massimo K e valore massimo"

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








