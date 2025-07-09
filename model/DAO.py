@staticmethod
    def get_colors():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp.Product_color as c
                        FROM go_products gp 
                        ORDER BY gp.Product_color
                                   """
            cursor.execute(query)

            for row in cursor:
                result.append(row['c'])

            cursor.close()
            cnx.close()

        return result

@staticmethod
    def getAllNodes(colore):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp.*
                        FROM go_products gp 
                        WHERE gp.Product_color = %s
                                       """
            cursor.execute(query, (colore,))

            for row in cursor:
                result.append(Product(**row))

            cursor.close()
            cnx.close()

        return result

@staticmethod
    def getAllArchi(colore, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t.p1 as p1, t.p2 as p2, COUNT(*) as peso
                        FROM (SELECT DISTINCT t1.p1, t2.p2, t1.d1 
                                FROM (SELECT DISTINCT gp.Product_number as p1, gds.Retailer_code as r1, gds.`Date` as d1
                                        FROM go_products gp, go_daily_sales gds  
                                        WHERE gp.Product_color = "White"
                                                and gds.Product_number = gp.Product_number
                                                and year(gds.Date) = 2018) t1, 
                                        (SELECT DISTINCT gp.Product_number as p2, gds.Retailer_code as r2, gds.`Date` as d2
                                        FROM go_products gp, go_daily_sales gds 
                                        WHERE gp.Product_color = "White"
                                                and gds.Product_number = gp.Product_number
                                                and year(gds.Date) = 2018) t2
                                WHERE t1.r1 = t2.r2
                                and t1.d1 = t2.d2
                                and t1.p1 > t2.p2) t
                        GROUP BY t.p1, t.p2

                                           """
            cursor.execute(query, (colore, anno, colore, anno))

            for row in cursor:
                result.append((row['p1'], row['p2'], row['peso']))

            cursor.close()
            cnx.close()

        return result


@staticmethod
    def getSalaryOfTeam(year, idMap):  # per il peso
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.teamCode, t.ID, sum(s.salary) as totSalary
                    from salaries s, teams t, appearances a
                    where s.`year` = t.`year` and t.`year` = a.`year` 
                    and a.`year` = %s
                    and t.ID = a.teamID 
                    and s.playerID = a.playerID 
                    group by t.teamCode"""

        cursor.execute(query, (year,))

        results = {}
        for row in cursor:
            #results.append(idMap[row["ID"]], row["totSalary"])
            results[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return results

