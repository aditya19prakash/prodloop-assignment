
from django.urls import path
from prodloop_assignment.views import Tasks,Tasks_id

urlpatterns = [
    path('tasks/',Tasks.as_view()),
    path('tasks/<int:id>/',Tasks_id.as_view()),
]
