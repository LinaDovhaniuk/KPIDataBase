from django.conf.urls import url, include

from . import views

app_name = 'Lab_2'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/facts/', include([
        url(r'^$', views.all_facts, name='facts'),
        url(r'^(?P<id>[0-9]+)/$', views.fact, name='fact')
    ])),
    url(r'^api/entities_names/', views.get_entities_name, name='entities_names'),
    url(r'^api/load_files/$', views.load_files, name='load_files'),
    url(r'^api/search/', include([
        url(r'^projects/$', views.finish_search, name='finish_search'),
        url(r'^customers/$', views.date_search, name='date_search'),
        url(r'^projects_text/$', views.word_text_search, name='word_text_search')
    ]))
]