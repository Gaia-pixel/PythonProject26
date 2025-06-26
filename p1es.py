# query restituisce:
# (cliente A, cliente B, numero di prodotti in comune) se ≥ min inserito da utente

# gli archi collegano due clienti se hanno fatto almeno min ordini in comune
# i nodi sono i clienti qui

@staticmethod
def getClientiConProdottiInComune(min_comune, idMap):   # sarebbe la getAllArchi
    conn = DBConnect.get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """SELECT 
                   c1.customer_id AS id1,
                   c2.customer_id AS id2,
                   COUNT(DISTINCT oi1.product_id) AS peso
               FROM 
                   order_items oi1
                   JOIN orders o1 ON oi1.order_id = o1.order_id
                   JOIN customers c1 ON o1.customer_id = c1.customer_id
                   JOIN order_items oi2 ON oi1.product_id = oi2.product_id
                   JOIN orders o2 ON oi2.order_id = o2.order_id
                   JOIN customers c2 ON o2.customer_id = c2.customer_id
               WHERE 
                   c1.customer_id < c2.customer_id
               GROUP BY id1, id2
               HAVING COUNT(DISTINCT oi1.product_id) >= %s"""

    cursor.execute(query, (min_comune,))
    results = []
    for row in cursor:
        results.append((idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

    cursor.close()
    conn.close()
    return results

# e nel model

def buildGraph(self):
    self._graph.clear()

    clienti = DAO.getAllClients()  # recupera i vertici
    self._graph.add_nodes_from(clienti)

    archi = DAO.getClientiConProdottiInComune(min_comune=3, idMap=self._idMap)
    for c1, c2, peso in archi:
        self._graph.add_edge(c1, c2, weight=peso)
