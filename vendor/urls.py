from django.urls import path
from vendor.views import *

urlpatterns = [
    path('dtl/', view_home),
    path('vendors/', StudentView.as_view()),
    path('vendors/<int:pk>/', StudentView.as_view(), name='student-detail'),
]
