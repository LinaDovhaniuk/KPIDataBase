from django.db import models

# Create your models here.
import _mysql as myDB
import json
import datetime

class MyDataBase :

    projects_xml = "Lab_2/Entities/Project.xml"
    teams_xml = "Lab_2/Entities/Team.xml"
    customers_xml = "Lab_2/Entities/Customer.xml"

    db_connection = None
    files = False

    def __init__(self):
        with open(MyDataBase.config_json, 'r') as f:
            data = json.load(f)
        self.db_connection = myDB.connect(data['host'], data['user'], data['password'],
                               data['database'], port=data['port'])
        print("Open!")

    def export_xml_to_db(self):
        current = self.db_connection.cursor()
        current.execute("LOAD XML LOCAL INFILE %s INTO TABLE Projects ROWS IDENTIFIED BY '<Project>';",
                    (self.projects_xml,))
        current.execute("LOAD XML LOCAL INFILE %s INTO TABLE Teams ROWS IDENTIFIED BY '<Team>';",
                    (self.teams_xml,))
        current.execute("LOAD XML LOCAL INFILE %s INTO TABLE Customers ROWS IDENTIFIED BY '<Customer>';",
                    (self.customers_xml,))
        current.close()
        self.db_connection.commit()



    def delete_all_data_on_table(self):
        current = self.db_connection.cursor()

        current.execute('SET FOREIGN_KEY_CHECKS = 0;')
        current.execute('TRUNCATE Project;')
        current.execute('TRUNCATE Cusromer;')
        current.execute('TRUNCATE Team;')
        current.execute('SET FOREIGN_KEY_CHECKS = 1;')

        current.close()
        self.db_connection.commit()

    def load_files(self):
        self.delete_all_data_on_table()
        self.export_xml_to_db()

    def make_list_of_entities(self, table_name, tuple_list):
        entities = []
        if table_name is "Project":
            fields = ['id_project', 'project_name', 'project_description',"id_customer", "id_team"]
        elif table_name is "Team":
            fields = ['id_team', 'team_name', 'number_of_developers', 'team_department', 'manager_name']
        elif table_name is "Customer":
            fields = ['id_customer', 'customer_name', 'customer_email', 'customer_phone']
        else:
            return []

        for tuple in tuple_list:
            entities.append(dict(zip(fields, tuple)))
        return entities

    def get_entities(self, table_name):
        current = self.db_connection.cursor()

        if table_name is "Project" or table_name is "Team" or table_name is "Customer":
            sql = "SELECT * FROM %s ;" % (table_name)
            current.execute(sql)
        else:
            current.close()
            return dict()

        data = []

        for i in range(current.rowcount):
            data.append(current.fetchone())

        current.close()
        self.db_connection.commit()
        return self.make_list_of_entities(table_name, data)

    def add_fact(self, fact):

        сurrent = self.db_connection.cursor()

        fact['date'] = str(datetime.date.today())
        сurrent.execute("INSERT INTO Changing_project_status(Project_id, Status, Date) "
                    "VALUES(%s, %s, %s);", (fact['id_project'], fact['status'], fact['date']))

        sql = "SELECT Changing_project_status.Id, Project.Name, Team.Name, Customer.Name, Changing_project_status.Status, Changing_project_status.Date " \
              "FROM (((Changing_project_status " \
              "JOIN Project ON Changing_project_status.id_project = Project.id_project) " \
              "JOIN Team ON Project.id_team = Team.id_team) " \
              "JOIN Customer ON Project.id_customer = Customer.id_customer) " \
              "ORDER BY Changing_project_status.Id DESC LIMIT 0,1;"
        сurrent.execute(sql)

        newFact = сurrent.fetchone()
        self.db_connection.commit()
        сurrent.close()
        return self.fact_to_dict(newFact)

    def fact_to_dict(self, fact):
        fields = ['id_changing', 'id_project', 'status', 'date']

        factDict = dict(zip(fields, fact))

        factDict['date'] = str(factDict['date'])

        return factDict

    def get_dicts_of_facts(self):

        current = self.db_connection.cursor()

        sql =  "SELECT Changing_project_status.Id, Project.Name, Team.Name, Customer.Name, Changing_project_status.Status, Changing_project_status.Date " \
              "FROM (((Changing_project_status " \
              "JOIN Project ON Changing_project_status.id_project = Project.id_project) " \
              "JOIN Team ON Project.id_team = Team.id_team) " \
              "JOIN Customer ON Project.id_customer = Customer.id_customer); "
        current.execute(sql)

        data = []

        for i in range(current.rowcount):
            data.append(self.fact_to_dict(current.fetchone()))

        current.close()

        return data

    def get_all_id_and_name(self, table_name):
        current = self.con.cursor()

        if table_name is "Project" or table_name is "Customer" \
                or table_name is "Team":
            sql = "SELECT Id, Name FROM %s;" % (table_name)
            current.execute(sql)
        else:
            current.close()
            return dict()

        data = []

        for i in range(current.rowcount):
            data.append(current.fetchone())

        current.close()
        self.db_connection.commit()

        return self.make_list_of_entities(table_name, data)

    def delete_fact(self, id):

        current = self.db_connection.cursor()

        sql = "DELETE FROM Changing_project_status WHERE Id = %s;" % id

        current.execute(sql)
        self.db_connection.commit()
        current.close()

    def edit_fact(self, id, fact):

        current = self.db_connection.cursor()

        sql = "UPDATE Changing_project_status SET id_project = %s " \
              "WHERE id_changing = %s;"%(fact['id_project'], id)

        sqlGet =  "SELECT Changing_project_status.Id, Project.Name, Team.Name, Customer.Name, Changing_project_status.Status, Changing_project_status.Date " \
              "FROM (((Changing_project_status " \
              "JOIN Project ON Changing_project_status.id_project = Project.id_project) " \
              "JOIN Team ON Project.id_team = Team.id_team) " \
              "JOIN Customer ON Project.id_customer = Customer.id_customer)" \
              "WHERE Changing_project_status.id_changing = %s; " % id

        current.execute(sql)
        current.execute(sqlGet)
        data = current.fetchone()
        self.db_connection.commit()
        current.close()

        return self.fact_to_dict(data)

    def truncate_facts(self):

        current = self.db_connection.cursor()

        sql = "TRUNCATE Changing_project_status;"

        current.execute(sql)
        self.db_connection.commit()
        current.close()

    def search_finished_project(self, finish):
         current = self.db_connection.cursor()

         sql = "SELECT Changing_project_status.Id, Project.Name, Team.Name, Customer.Name, Changing_project_status.Status, Changing_project_status.Date " \
              "FROM (((Changing_project_status " \
              "JOIN Project ON Changing_project_status.id_project = Project.id_project) " \
              "JOIN Team ON Project.id_team = Team.id_team) " \
              "JOIN Customer ON Project.id_customer = Customer.id_customer)" \
              "WHERE Changing_project_status.status = %s; " % finish

         current.execute(sql)

         data = []

         for i in range(current.rowcount):
             data.append(current.fetchone())

         current.close()

         return self.make_list_of_entities('Changind_project_status', data)

    def search_changing_date(self, first, second):

        current = self.db_connection.cursor()
        sql =  "SELECT Changing_project_status.Id, Project.Name, Team.Name, Customer.Name, Changing_project_status.Status, Changing_project_status.Date " \
              "FROM (((Changing_project_status " \
              "JOIN Project ON Changing_project_status.id_project = Project.id_project) " \
              "JOIN Team ON Project.id_team = Team.id_team) " \
              "JOIN Customer ON Project.id_customer = Customer.id_customer)" \
              "WHERE Changing_project_status.date BETWEEN %s AND %s; " % (first, second)
        current.execute(sql)

        data = []
        for i in range(current.rowcount):
            data.append(current.fetchone())

        current.close()

        return self.make_list_of_entities('Changind_project_status', data)

    def search_project_word_text(self, word):
        current = self.db_connection.cursor()

        sql = "SELECT * FROM Project WHERE MATCH (project_description) " \
              "against ('%s' in boolean mode);" % word

        current.execute(sql)

        data = []
        for i in range(current.rowcount):
            data.append(current.fetchone())
            current.close()
        return self.make_list_of_dicts_dimensions('Project', data)

    def close_connection(self):
        self.con.close()
        print("Close!")



