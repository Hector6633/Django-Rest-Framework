from django.urls import path, include
from home.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', Mobilebrands, basename='employee')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index, name='index'),
    path('employee/', employee, name='employee'),
    path('EmployeeClass/', EmployeeClass.as_view(), name='EmployeeClass'),
    path('registerapi/', RegisterApi.as_view(), name='registerapi'),
    path('loginapi/', LoginApi.as_view(), name='loginapi'),
]