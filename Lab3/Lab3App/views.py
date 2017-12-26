import datetime
import ast
from django.http import JsonResponse
from django.views import generic
from .models import *
from django.apps import apps


class IndexView(generic.ListView):
    template_name = 'Lab3App/index.html'

    def get_queryset(self):
        pass


class HistoryView(generic.ListView):
    template_name = 'Lab3App/history.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        return History.objects.order_by('-date')


def all_facts(request):

    if request.method == 'GET':
        return get_all_facts(request)
    elif request.method == 'POST':
        return post_fact(request)
    elif request.method == 'DELETE':
        return delete_facts(request)

def get_all_facts(request):
    facts_q = get_facts()

    res = dict({
        'facts': list(facts_q)
    })
    return JsonResponse(res)

def post_fact(request):
    dataStr = request.body.decode('utf-8')
    fact = ast.literal_eval(dataStr)
    instance = ChangesProjectStatus(
        id_project=Projects.objects.get(id_project=fact['id_project']),
        id_customer = Customers.objects.get(id_customer=fact['id_customer']),
        id_team = Teams.objects.get(id_team=fact['id_team']),
        changing_date=str(datetime.date.today())
    )
    ''''newFact = ChangesProjectStatus.objects.create(Projects.objects.filter(id_project = fact['id_project']),
                            Customers.objects.filter(id_customer = fact['id_customer']), Teams.objects.filter(id_team = fact['id_team']), changing_date = str(datetime.date.today()))

    newFact = get_facts(newFact.id_changing)
    print(newFact)
    '''''
    instance.save()
    res = dict({
        'fact': list(ChangesProjectStatus.objects.filter(id_changing=instance.id_changing).values('id_changing', 'id_project__project_name', 'id_team__team_name', 'id_customer__customer_name', 'changing_date').order_by('id_changing'))[0]
    })
    return JsonResponse(res)

def delete_facts(request):
    ChangesProjectStatus.objects.all().delete()
    res = dict({'status':True})
    return JsonResponse(res)

def fact(request, id):
    if request.method == 'PUT':
        return put_fact(request, id)
    elif request.method == 'DELETE':
        return delete_fact(request, id)

def put_fact(request, id):
    dataStr = request.body.decode('utf-8')
    fact = ast.literal_eval(dataStr)
    ChangesProjectStatus.objects\
        .filter(id_changing=int(id))\
        .update(
        id_project=Projects.objects.get(id_project=fact['id_project']),
        id_customer=Customers.objects.get(id_customer=fact['id_customer']),
        id_team=Teams.objects.get(id_team=fact['id_team']),
        changing_date=datetime.date.today()
    )

    newFact = get_facts(id)
    print(newFact)
    res = dict({'fact': list(newFact)[0]})
    return JsonResponse(res)

def delete_fact(request, id):
    ChangesProjectStatus.objects.filter(id_changing=int(id)).delete()
    res = dict({'status':'OK'})
    return JsonResponse(res)



def bool_search(request):
    if request.method == 'GET':
        finish_status = request.GET.get('finish_status')

        projects = Projects.objects.filter(finish_status=finish_status).values()

        res = dict({'projects':list(projects)})
        return JsonResponse(res)

def range_search(request):
    if request.method == 'GET':
        bottom = request.GET.get('bottom')
        top = request.GET.get('top')

        customers = Customers.objects.filter(invitins_date__range=[bottom,top]).values()

        res = dict({'customers':list(customers)})
        return JsonResponse(res)

def get_dim_names_ids(request):

    projects = get_all_id_name_dim("Projects")
    customers = get_all_id_name_dim("Customers")
    teams = get_all_id_name_dim("Teams")

    res = dict({
        'data': {
            'projects': projects,
            'customers': customers,
            'teams': teams
        }
    })

    return JsonResponse(res)

def get_all_id_name_dim(dim_name):
    Dimension = apps.get_model('Lab3App', dim_name)
    if(dim_name == 'Projects'):
        return list(Dimension.objects.values('id_project', 'project_name'))
    if(dim_name == 'Customers'):
        return list(Dimension.objects.values('id_customer', 'customer_name'))
    if(dim_name == 'Teams'):
        return list(Dimension.objects.values('id_team', 'team_name'))


def get_facts(id=None):
    if id is None:
        return ChangesProjectStatus.objects.values('id_changing', 'id_project__project_name', 'id_team__team_name', 'id_customer__customer_name', 'changing_date').order_by('id_changing')

    else:
        return ChangesProjectStatus.objects.filter(id_changing=int(id)).values('id_changing', 'id_project__project_name', 'id_team__team_name', 'id_customer__customer_name', 'changing_date')
