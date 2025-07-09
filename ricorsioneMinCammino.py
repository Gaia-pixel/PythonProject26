# cammino minimo num archi
# ES: Trova il cammino più corto (in numero di tappe)
# tra due ordini di uno store (bike_store_full)

def getCamminoMinimoNodi(self, start_id, end_id):
    self._bestPath = []
    start = self._idMap[int(start_id)]
    end = self._idMap[int(end_id)]
    self._ricorsioneMinimoNodi([start], end)
    return self._bestPath

def _ricorsioneMinimoNodi(self, parziale, end):
    ultimo = parziale[-1]
    if ultimo == end:
        if not self._bestPath or len(parziale) < len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
        return

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            parziale.append(vicino)
            self._ricorsioneMinimoNodi(parziale, end)
            parziale.pop()

# cammino peso minimo
def getCamminoPesoMinimo(self, start_id, end_id):
    self._bestPath = []
    self._bestScore = None
    start = self._idMap[int(start_id)]
    end = self._idMap[int(end_id)]
    self._ricorsionePesoMinimo([start], end, 0)
    return self._bestPath, self._bestScore

def _ricorsionePesoMinimo(self, parziale, end, pesoAttuale):
    ultimo = parziale[-1]
    if ultimo == end:
        if pesoAttuale < self._bestScore:
            self._bestScore = pesoAttuale
            self._bestPath = copy.deepcopy(parziale)
        return

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            peso = self._graph[ultimo][vicino]["weight"]
            if pesoAttuale + peso < self._bestScore:  # pruning
                parziale.append(vicino)
                self._ricorsionePesoMinimo(parziale, end, pesoAttuale + peso)
                parziale.pop()

# Cammino con peso minimo e massimo numero di tappe T
def getCamminoPesoMinimoMaxTappe(self, start_id, end_id, T):
    self._bestPath = []
    self._bestScore = float('inf')
    start = self._idMap[int(start_id)]
    end = self._idMap[int(end_id)]
    self._ricorsioneConTappe([start], end, 0, T)
    return self._bestPath, self._bestScore

def _ricorsioneConTappe(self, parziale, end, pesoAttuale, maxTappe):
    if len(parziale) > maxTappe + 1:
        return

    ultimo = parziale[-1]
    if ultimo == end:
        if pesoAttuale < self._bestScore:
            self._bestScore = pesoAttuale
            self._bestPath = copy.deepcopy(parziale)
        return

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            peso = self._graph[ultimo][vicino]["weight"]
            parziale.append(vicino)
            self._ricorsioneConTappe(parziale, end, pesoAttuale + peso, maxTappe)
            parziale.pop()

# peso minimo passando per un nodo obbligatorio
def getCamminoConNodoObbligatorio(self, start_id, obbligatorio_id, end_id):
    self._bestPath = []
    self._bestScore = float('inf')

    start = self._idMap[int(start_id)]
    obbligatorio = self._idMap[int(obbligatorio_id)]
    end = self._idMap[int(end_id)]

    # Cammino 1: start → obbligatorio
    self._tempPath = []
    self._tempScore = float('inf')
    self._ricorsionePesoMinimo([start], obbligatorio, 0)
    path1 = self._tempPath
    score1 = self._tempScore

    # Cammino 2: obbligatorio → end
    self._tempPath = []
    self._tempScore = float('inf')
    self._ricorsionePesoMinimo([obbligatorio], end, 0)
    path2 = self._tempPath
    score2 = self._tempScore

    if path1 and path2:
        self._bestPath = path1[:-1] + path2  # evita doppio nodo centrale
        self._bestScore = score1 + score2

    return self._bestPath, self._bestScore

def _ricorsionePesoMinimo(self, parziale, end, pesoAttuale):
    ultimo = parziale[-1]
    if ultimo == end:
        if pesoAttuale < self._tempScore:
            self._tempScore = pesoAttuale
            self._tempPath = copy.deepcopy(parziale)
        return

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            peso = self._graph[ultimo][vicino]["weight"]
            if pesoAttuale + peso < self._tempScore:  # pruning
                parziale.append(vicino)
                self._ricorsionePesoMinimo(parziale, end, pesoAttuale + peso)
                parziale.pop()

# esempio uso nel controller :
path, score = model.getCamminoConNodoObbligatorio(5, 10, 20)



