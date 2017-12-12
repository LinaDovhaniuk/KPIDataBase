from django.db import models

# Create your models here.
import MySQLdb as myDB
import json
import datetime


class MyDataBase :

    config_json = "D:/KPI/DataBase/lab_2/Second_Lab/config.json"
    projects_xml = "D:\KPI\DataBase\lab_2\Second_Lab\Lab_2\Entities\Project.xml"
    teams_xml = "D:\KPI\DataBase\lab_2\Second_Lab\Lab_2\Entities\Team.xml"
    customers_xml = "D:\KPI\DataBase\lab_2\Second_Lab\Lab_2\Entities\Customer.xml"

    db_connection = None
    files = False

    def __init__(self):
        with open(MyDataBase.config_json, 'r') as f:
            data = json.load(f)
        self.db_connection = myDB.connect(data['host'], data['user'], data['password'],
                               data['name'], port=data['port'])
        print("Open!")

    def export_xml_to_db(self):
        current = self.db_connection.cursor()
        current.execute("LOAD XML LOCAL INFILE %s INTO TABLE projects ROWS IDENTIFIED BY '<Project>';",
                    (self.projects_xml,))
        current.execute("LOAD XML LOCAL INFILE %s INTO TABLE teams ROWS IDENTIFIED BY '<Team>';",
                    (self.teams_xml,))
        current.execute("LOAD XML LOCAL INFILE %s INTO TABLE customers ROWS IDENTIFIED BY '<Customer>';",
                    (self.customers_xml,))
        current.close()
        self.db_connection.commit()


    def delete_all_data_on_table(self):
        current = self.db_connection.cursor()

        current.execute('SET FOREIGN_KEY_CHECKS = 0;')
        current.execute('TRUNCATE Projects;')
        current.execute('TRUNCATE Customers;')
        current.execute('TRUNCATE Teams;')
        current.execute('SET FOREIGN_KEY_CHECKS = 1;')

        current.close()
        self.db_connection.commit()

    def load_files(self):
        self.delete_all_data_on_table()
        self.export_xml_to_db()

    def make_list_of_entities(self, table_name, tuple_list):
        entities = []
        if table_name is "Projects":
            fields = ['id_project', 'project_name', 'project_description','finish_status']
        elif table_name is "Teams":
            fields = ['id_team', 'team_name', 'team_department', 'manager_name','developers']
        elif table_name is "Customers":
            fields = ['id_customer', 'customer_name', 'customer_email', 'customer_phone']
        else:
            return []

        for tuple in tuple_list:
            entities.append(dict(zip(fields, tuple)))
        return entities

    def get_entities(self, table_name):
        current = self.db_connection.cursor()

        if table_name is "Projects" or table_name is "Teams" or table_name is "Customers":
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

        fact['changing_date'] = str(datetime.date.today())
        сurrent.execute("INSERT INTO Changes_project_status(id_project, id_customer, id_team, changing_date) "
                    "VALUES(%s, %s, %s, %s);", (fact['id_project'], fact['id_customer'], fact['id_team'], fact['changing_date']))

        sql = "SELECT Changes_project_status.id_changing, Projects.project_name, Customers.customer_name, Teams.team_name, Changes_project_status.changing_date " \
              "FROM (((Changes_project_status " \
              "INNER JOIN Projects ON Changes_project_status.id_project = Projects.id_project) " \
              "INNER JOIN Customers ON Changes_project_status.id_customer = Customers.id_customer) " \
              "INNER JOIN Teams ON Changes_project_status.id_team = Teams.id_team) " \
              "ORDER BY Changes_project_status.id_changing DESC LIMIT 0,1;"

        сurrent.execute(sql)

        newFact = сurrent.fetchone()
        self.db_connection.commit()
        сurrent.close()
        return self.fact_to_dict(newFact)

    def fact_to_dict(self, fact):
        fields = ['id_changing', 'id_project', 'id_customer', 'id_team', 'changing_date']

        factDict = dict(zip(fields, fact))

        factDict['changing_date'] = str(factDict['changing_date'])

        return factDict

    def get_dicts_of_facts(self):

        current = self.db_connection.cursor()

        sql = "SELECT Changes_project_status.id_changing, Projects.project_name, Customers.customer_name, Teams.team_name, Changes_project_status.changing_date " \
              "FROM (((Changes_project_status " \
              "INNER JOIN Projects ON Changes_project_status.id_project = Projects.id_project) " \
              "INNER JOIN Customers ON Changes_project_status.id_customer = Customers.id_customer) " \
              "INNER JOIN Teams ON Changes_project_status.id_team = Teams.id_team) ;"
        current.execute(sql)

        data = []

        for i in range(current.rowcount):
            data.append(self.fact_to_dict(current.fetchone()))

        current.close()

        return data

    def get_all_id_and_name(self, table_name):
        current = self.db_connection.cursor()

        if table_name is "Projects" :
            sql = "SELECT id_project, project_name FROM %s;" % (table_name)
            current.execute(sql)
        if table_name is "Customers":
            sql = "SELECT id_customer, customer_name FROM %s;" % (table_name)
            current.execute(sql)
        if table_name is "Teams":
            sql = "SELECT id_team, team_name FROM %s;" % (table_name)
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

        sql = "DELETE FROM Changes_project_status WHERE id_changing = %s;" % id

        current.execute(sql)
        self.db_connection.commit()
        current.close()

    def edit_fact(self, id, fact):

        current = self.db_connection.cursor()


        sql = "UPDATE Changes_project_status SET id_project = %s, id_customer = %s, " \
              "id_team = %s WHERE id_changing = %s;" % (fact['id_project'], fact['id_customer'],
                                               fact['id_team'], id)

        sqlGet = "SELECT Changes_project_status.id_changing, Projects.project_name, Customers.customer_name, Teams.team_name, Changes_project_status.changing_date " \
              "FROM (((Changes_project_status " \
              "INNER JOIN Projects ON Changes_project_status.id_project = Projects.id_project) " \
              "INNER JOIN Customers ON Changes_project_status.id_customer = Customers.id_customer) " \
              "INNER JOIN Teams ON Changes_project_status.id_team = Teams.id_team) " \
              "WHERE Changes_project_status.id_changing = %s ;" % id

        current.execute(sql)
        current.execute(sqlGet)
        data = current.fetchone()
        self.db_connection.commit()
        current.close()

        return self.fact_to_dict(data)

    def truncate_facts(self):

        current = self.db_connection.cursor()

        sql = "TRUNCATE Changes_project_status;"

        current.execute(sql)
        self.db_connection.commit()
        current.close()

    def search_finished_project(self, finish):
         current = self.db_connection.cursor()

         sql = sql = 'SELECT * FROM Projects WHERE finish_status = %s;' % finish

         current.execute(sql)

         data = []

         for i in range(current.rowcount):
             data.append(current.fetchone())

         current.close()

         return self.make_list_of_entities('Changes_project_status', data)

    def search_changing_date(self, first, second):

        current = self.db_connection.cursor()
        sql =  "SELECT Changes_project_status.id_changing, Projects.project_name, Customers.customer_name, Teams.team_name, Changes_project_status.changing_date " \
              "FROM (((Changes_project_status " \
              "INNER JOIN Projects ON Changes_project_status.id_project = Projects.id_project) " \
              "INNER JOIN Customers ON Changes_project_status.id_customer = Customers.id_customer) " \
              "INNER JOIN Teams ON Changes_project_status.id_team = Teams.id_team) " \
              "WHERE Changes_project_status.changing_date BETWEEN %s AND %s; " % (first, second)
        current.execute(sql)

        data = []
        for i in range(current.rowcount):
            data.append(current.fetchone())

        current.close()

        return self.make_list_of_entities('Changes_project_status', data)

    def search_project_word_text(self, word):
        current = self.db_connection.cursor()

        sql = "SELECT * FROM Projects WHERE MATCH (project_description) " \
              "against ('%s' in boolean mode);" % word

        current.execute(sql)

        data = []
        for i in range(current.rowcount):
            data.append(current.fetchone())
            current.close()
        return self.make_list_of_entities('Projects', data)

    def close_connection(self):
        self.db_connection.close()
        print("Close!")



