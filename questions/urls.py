from django.conf.urls import url
from questions.views import QuestionEdit, QuestionCreate, QuestionViews, QuestionDetails

urlpatterns = [
    url(r'^$', QuestionViews.as_view(), name='questions'),
    url(r'^(?P<question_id>\d+)/$', QuestionDetails.as_view(pk_url_kwarg='question_id'), name='question_details'),
    url(r'^(?P<question_id>\d+)/edit/$', QuestionEdit.as_view(pk_url_kwarg='question_id'), name='question_edit'),
    url(r'^create/$', QuestionCreate.as_view(), name='question_create'),
]