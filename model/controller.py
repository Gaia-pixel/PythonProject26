


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self.lSelezionata = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # se riempo DD con stringhe
    def fillDD(self):
        loc = self._model.get_loc()
        for l in loc:
            self._view.dd_localization.options.append(ft.dropdown.Option(l))
        self._view.update_page()

    def handle_graph(self, e):
        self._view._txt_result.controls.clear()
        self.lSelezionata = self._view.dd_localization.value
        # se è un intero in un txt faccio il controllo try except
        if self.lSelezionata is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare una localizzazione"))
            self._view.update_page()
            return
        self._model.buildGraph(self.lSelezionata)
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"grafo creato con {n} nodi e {a} archi"))
        self._view.update_page()

    # se lo riempio con oggetti o comunque ho bisogno che faccia qualcosa quando clicco sulla scelta
    # key è quello che vede l'utente, data è ciò che ci metto dentro
    def fillDD(self):
        anni = self._model.get_years()
        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(key = a, data = a, on_click = self.handleDDSelection))
        self._view.update_page()

    def handleDDSelection(self, e):
        self.annoSelezionato = e.control.data # in questo caso non necessario il controllo sul None ne qui ne nell' handlegrafo
        forme = self._model.get_shapes(self.annoSelezionato)
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))
        self._view.update_page()

    # punto c
    def handlePrintDetails(self, e):
        nodiComponente = self._model.getMaxComponente()
        self._view._txtGraphDetails.controls.append(ft.Text("Di seguito i nodi della massima componente connessa: "))
        for n,p in nodiComponente:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{n} -- {p}"))
        self._view.update_page()




