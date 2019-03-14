from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('add', views.add_question, name='add_question'),
    path('edit', views.view_edit, name='view_edit'),
    path('delete', views.delete_question, name='delete_question'),
    path('save_edit', views.edit_question, name='edit_question'),

    path('rsp', views.responsive_show, name='rsp'),

    path('<int:question_id>/add', views.add_choice, name='add_choice'),
    path('<int:question_id>/edit', views.edit_delete_choice, name='edit_choice'),
    path('<int:question_id>/delete', views.edit_delete_choice, name='delete_choice'),
    path('<int:question_id>/save', views.save_choice, name='save_choice'),

    path('table_question/', views.show_table_question, name='show_table_question'),
    path('table_question/<int:question_id>/table_choice/', views.show_table_choice, name='show_table_choice'),
]