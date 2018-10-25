from django.conf.urls import url
from answers.views import AnswerCreate
from answers.views import AnswerEdit
from answers.views import AnswerDetails

urlpatterns = [
    url(r'^(?P<answer_id>\d+)/$', AnswerDetails.as_view(pk_url_kwarg='answer_id'), name='answer_details'),
    url(r'^(?P<answer_id>\d+)/edit/$', AnswerEdit.as_view(pk_url_kwarg='answer_id'), name='answer_edit'),
    url(r'^create/$', AnswerCreate.as_view(), name='answer_create')
]
