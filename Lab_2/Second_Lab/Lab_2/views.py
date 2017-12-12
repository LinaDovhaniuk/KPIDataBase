import json
import ast

from django.http import JsonResponse
from django.views import generic


from .models import MyDataBase
from django.shortcuts import render

class IndexView(generic.ListView):
    template_name = 'Lab_2/index.html'

    def get_queryset(self):
        pass


def load_files(request):
        mydb = MyDataBase()
        mydb.load_files()
        mydb.close_connection()

        res = get_entities_names_ids()
        return JsonResponse(res)

def get_entities_names_ids():
        mydb = MyDataBase()
        projects = mydb.get_all_id_and_name("Projects")
        customers = mydb.get_all_id_and_name("Customers")
        teams = mydb.get_all_id_and_name("Teams")
        mydb.close_connection()
        return dict({
            'data': {
                'projects': projects,
                'customers': customers,
                'teams': teams
            }
        })
def all_facts(request):

    if request.method == 'GET':
        return get_all_changes(request)
    elif request.method == 'POST':
        return create_changes(request)
    elif request.method == 'DELETE':
        return delete_changes(request)

def get_all_changes(request):
    mydb = MyDataBase()
    facts = mydb.get_dicts_of_facts()
    mydb.close_connection()
    res = dict({
        'facts': facts
    })
    return JsonResponse(res)

def create_changes(request):
    dataStr = request.body.decode('utf-8')
    fact = ast.literal_eval(dataStr)
    mydb = MyDataBase()
    newFact = mydb.add_fact(fact)
    mydb.close_connection()
    return JsonResponse(newFact)

def delete_changes(request):
    mydb = MyDataBase()
    mydb.truncate_facts()
    mydb.close_connection()
    res = dict({
        'status' : True
    })
    return JsonResponse(res)

def fact(request, id):
    if request.method == 'GET':
        return get_fact(request, id)
    elif request.method == 'PUT':
        return put_fact(request, id)
    elif request.method == 'DELETE':
        return delete_fact(request, id)

def get_fact(request, id):
    pass

def put_fact(request, id):
    dataSTR = request.body.decode('utf-8')
    fact = ast.literal_eval(dataSTR)
    mydb = MyDataBase()

    newfact = mydb.edit_fact(id,fact)
    mydb.close_connection()

    res = dict({
        'fact': newfact
    })
    return JsonResponse(res)

def delete_fact(request, id):
     mydb = MyDataBase()
     mydb.delete_fact(id)
     mydb.close_connection()
     res = dict({
         'status':'OK'
     })
     return JsonResponse(res)

def get_entities_name(request):
    if request.method == 'GET':
        res = get_entities_names_ids()
        print(res)
    return JsonResponse(res)

def finish_search(request):
    if request.method == 'GET':
        finish_status = request.GET.get('finish_status')

        mydb = MyDataBase()
        projects = mydb.search_finished_project(finish_status)
        mydb.close_connection()

        res = dict({
            'projects':projects
        })
        return JsonResponse(res)
def date_search(request):
    if request.method == 'GET':
        start = request.GET.get('start')
        finish = request.GET.get('finish')

        mydb = MyDataBase()
        mydb.close_connection()

        res = dict({

        })
        return JsonResponse(res)

def word_text_search(request):
    if request.method == 'GET':
        searchType = request.GET.get('type')
        search = request.GET.get('search')
        if searchType == 'word':
            search = '+' + search.replace(' ', '+')
        else:
            search = ''.join(('"', search, '"'))
        mydb = MyDataBase()
        projects = mydb.search_project_word_text(search)
        mydb.close_connection()
        res = dict({
            'projects':projects
        })
        return JsonResponse(res)