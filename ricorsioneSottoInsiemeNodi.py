# utile per casi come:
# Dream Team: selezionare K nodi con punteggio minimo/massimo
# Sottinsieme di album con durata totale ≤ X
# Massimo numero di nodi compatibili secondo un vincolo

# ES 1: Dream Team di K nodi con score minimo
def getDreamTeam(self, K):
    self._bestTeam = []
    self._bestScore = float('inf')

    nodi = list(self._graph.nodes)
    self._ricorsioneDream([], nodi, K)
    return self._bestTeam, self._bestScore

def _ricorsioneDream(self, parziale, nodi_possibili, K):
    if len(parziale) == K:
        score = self._scoreTeam(parziale)
        if score < self._bestScore:
            self._bestScore = score
            self._bestTeam = copy.deepcopy(parziale)
        return

    for n in nodi_possibili:
        if n not in parziale:
            parziale.append(n)
            self._ricorsioneDream(parziale, nodi_possibili, K)
            parziale.pop()

def _scoreTeam(self, team):
    score = 0
    for u, v, d in self._graph.edges(data=True):
        if u in team and v in team:
            score += d["weight"]
        elif u in team or v in team:
            score += d["weight"] / 2  # penalità minore per archi misti (opzionale)
    return score

# ES2: Massimo numero di album con durata ≤ MAX
def getMassimoSottinsiemeConDurata(self, nodi, durataMax):
    self._bestSubset = []
    self._ricorsioneDurata([], nodi, durataMax)
    return self._bestSubset

def _ricorsioneDurata(self, parziale, nodi_possibili, durataMax):
    durata_totale = sum(n.durata for n in parziale)
    if durata_totale > durataMax:
        return
    if len(parziale) > len(self._bestSubset):
        self._bestSubset = copy.deepcopy(parziale)

    for n in nodi_possibili:
        if n not in parziale:
            parziale.append(n)
            self._ricorsioneDurata(parziale, nodi_possibili, durataMax)
            parziale.pop()

# ES3: Dato uno store, seleziona il massimo numero di ordini (nodi)
# con una somma totale di item ordinati ≤ X,
# dove gli item sono il peso degli archi uscenti.

def getOrdiniSottoSoglia(self, ordini, sogliaMAX):
    self._bestSubset = []
    self._ricorsioneOrdini([], ordini, sogliaMAX)
    return self._bestSubset

def _ricorsioneOrdini(self, parziale, nodi_possibili, sogliaMAX):
    totale = sum(self._quantitaOrdine(n) for n in parziale)
    if totale > sogliaMAX:
        return
    if len(parziale) > len(self._bestSubset):
        self._bestSubset = copy.deepcopy(parziale)

    for o in nodi_possibili:
        if o not in parziale:
            parziale.append(o)
            self._ricorsioneOrdini(parziale, nodi_possibili, sogliaMAX)
            parziale.pop()

def _quantitaOrdine(self, nodo):
    """
    Somma delle quantità vendute (peso archi uscenti)
    """
    peso = 0
    for _, _, d in self._graph.out_edges(nodo, data=True):
        peso += d["weight"]
    return peso



