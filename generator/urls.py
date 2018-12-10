from django.urls import path , re_path

from . import views

urlpatterns = [
    path(''					, views.index			, name='index'),
    path('createquestion'	, views.createquestion	, name='createquestion'),
    path('checkanswer'		, views.checkanswer		, name='checkanswer'),
    path('createtemplate' , views.createtemplate ,name='createtemplate'),
    path('createque',views.createque,name='createque')
]

