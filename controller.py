def __init__(self, view, model):
    # the view, with the graphical elements of the UI
    self._view = view
    # the model, which implements the logic of the program and holds the data
    self._model = model
    self.storeSelezionato = None
    self.nodeSelezionato = None




def read_node(self, e):
    if e.control.value is None:
        self.nodeSelezionato = None
    else:
        self.nodeSelezionato = e.control.value


def fillDD(self, allNodes): # populate
    self._view._ddNode.options.clear()
    for n in allNodes:
        self._view._ddNode.options.append(
            ft.dropdown.Option(key = n.order_id, data = n, on_click = self.read_dropDown))


def read_dropDown(self, e):  # leggi dal dd
    if e.control.value is None:
        self.storeSelezionato = None
    else:
        self.storeSelezionato = e.control.value
    print("read_dropDown called: ", self.storeSelezionato)


def fillDDStore(self):
    stores = self._model.get_stores()
    for s in stores:
        self._view._ddStore.options.append(ft.dropdown.Option(key=s.store_id, text=s.store_id, data=s))
    self._view.update_page()

def fillDDCircuits(self):
    circuits = self._model.getCircuits()
    circuitDD = []
    for c in circuits:
        circuitDD.append(ft.dropdown.Option(key = c.name, data = c, on_click=self.read_dropDown)) # quando l'utente seleziona dal dd mi salvo cos'ha scelto
    self._view.update_page()


def handleCreaGrafo(self, e):
    self._view._txt_result.controls.clear()  # cancello ciò che ho stampato con la chiamata precedente
    store = self._view._ddStore.value
    if store is None or store == "":
        self._view.create_alert("Store non selezionato!")
        return

    g = self._view._txtIntK.value
    try:
        numG = int(g)

    except ValueError:
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Inserire un valore numerico!", color="red"))
        self._view.update_page()
        return

    if numG < 0:
        self._view.create_alert("Inserire un valore positivo!")

    self._model.build_graph(store, numG)
    # abilito tutti i pulsanti ecc che devo abilitare dopo aver creato il grafo
    # (se mi dice che dal dd si seleziona qualcosa tra quelli presenti nel grafo)
    self._view.dd_AeroportoP.disabled = False
    self._view.btn_connessi.disabled = False
    self._view.dd_AeroportoD.disabled = False
    self._view.btn_cerca.disabled = False

    allNodes = self._model.getAllNodes()  # li prendo per metterli nel dropdown, da fare se dice di riempirlo con nodi grafo
    self.fillDD(allNodes)

    nNodes, nEdges = self._model.getGraphDetails()
    self._view._txt_result.controls.append(ft.Text(f"Grafo creato correttamente:"))
    self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
    self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))

    self._view.update_page()


def handleCerca(self, e):
    nodi = self._model.get_nodiMaxCammino(self._view._ddNode.value)
    self._view._txt_result.controls.append(ft.Text(f"nodo di partenza: {self._view._ddNode.value}"))
    for n in nodi:
        self._view._txt_result.controls.append(ft.Text(f"{n.order_id}"))
        # se dice contemporaneamente aggiungi al dd lo faccio qui
        self._view._ddNode.options.append(ft.dropdown.Option(data = n, key = n.id))
    self._view.update_page()


def handle_connessi(self, e):  # i nodi connessi a quello dato
    nodo = self._choiceDDAeroportoP
    if nodo is None:
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Attenzione, selezionare una voce dal menù."))
        return

    viciniTuple = self._model.getSortedNeighbors(nodo)  # tupla nodo - peso
    self._view._txt_result.controls.clear()
    self._view._txt_result.controls.append(ft.Text(f"nodo di partenza: {nodo}"))
    self._view._txt_result.controls.append(ft.Text(f"nodi connessi in ordine decr di num di voli:"))

    for n in viciniTuple:
        self._view._txt_result.controls.append(ft.Text(f"nodo: {n[0]} - peso: {n[1]}"))

    self._view.update_page()

def handlePercorso(self, e):  # devo trovare un percorso tra due nodi, nel model c'è getPath e quelli sotto in base a cosa mi serve
    nodo1  = self._choiceDDAeroportoP
    if nodo1 is None:
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Attenzione, selezionare una voce dal menù."))
        return
    nodo2 = self._choiceDDAeroportoP
    if nodo2 is None:
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Attenzione, selezionare una voce dal menù."))
        return
    path = self._model.getPath(nodo1, nodo2)
    if len(path) == 0:
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Cammino non trovato"))
    else:
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Cammino trovato, di seguito i nodi:"))
        for n in path:
            self._view._txt_result.controls.append(ft.Text(n))
    self._view.update_page()



def handleRicorsione(self, e):
    nodi = self._model.get_nodiCamminoRicorsione(self._view._ddNode.value)
    self._view._txt_result.controls.append(ft.Text(f"nodo di partenza (r): {self._view._ddNode.value}"))
    for n in nodi:
        self._view._txt_result.controls.append(ft.Text(f"{n.order_id}"))

    self._view.update_page()
