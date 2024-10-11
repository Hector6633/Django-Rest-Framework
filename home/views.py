from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from. models import *
from. serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
@api_view(["GET", 'POST']) 
def index(request):
    if request.method == 'GET':
        employee = {
            'name':'rajeev',
            'age':22,
            'city':'kerala',
            'job':'developer'
        }
        return Response(employee)
    elif request.method == 'POST':
        return Response('post request')
    else:
        return Response('error')
    
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def employee(request):
    if request.method == 'GET':
        emp = Employee.objects.all()
        emp_ser = EmployeeSerializer(emp, many=True)
        return Response(emp_ser.data)
    elif request.method == 'POST':
        data = request.data
        emp_ser = EmployeeSerializer(data=data)
        if emp_ser.is_valid():
            emp_ser.save()
            return Response('data saved')
        else:
            return Response('data not saved')
    elif request.method == 'PUT':
        data = request.data
        emp = Employee.objects.get(id=data.get('id'))
        emp_ser = EmployeeSerializer(emp, data=data, partial=False)
        if emp_ser.is_valid():
            emp_ser.save()
            return Response('data updated')
        else:
            return Response('data not updated')
    elif request.method == 'PATCH':
        data = request.data
        emp = Employee.objects.get(id=data.get('id'))
        emp_ser = EmployeeSerializer(emp, data=data, partial=True)
        if emp_ser.is_valid():
            emp_ser.save()
            return Response('data updated')
        else:
            return Response('data not updated')
    elif request.method == 'DELETE':
        data = request.data
        emp = Employee.objects.get(id=data.get('id'))
        emp.delete()
        return Response('data deleted')
    
class EmployeeClass(APIView):
      def get(self, request):
        emp = Employee.objects.all()
        emp_ser = EmployeeSerializer(emp, many=True)
        return Response(emp_ser.data)
      def post(self, request):
          return Response('This is post request')
      def put(self, request):
          return Response('This is put request') 
      
class Mobilebrands(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    
    def list(self, request):
        search = self.request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = EmployeeSerializer(queryset, many=True)
        return Response({'data': serializer.data})


class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data, many=False)
        if not serializer.is_valid():
            return Response({'message':serializer.errors})
        serializer.save()
        
        return Response('data saved')
    
    def get(self, request):
        user = User.objects.all()
        user_ser = RegisterSerializer(user, many=True)  # convert to json
        return Response(user_ser.data)
    
class LoginApi(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data = request.data, many=False)
        if not serializer.is_valid():
            return Response({'message':serializer.errors})
        user = authenticate(username = request.data['username'], password = request.data['password'])
        
        if not user:
            return Response('message:Login failed')
        else:
            token, _ = Token.objects.get_or_create(user = user) # boolean variable
            return Response({'message':'Login success'}, {'token':str(token)})
            
        
        return Response('Login success')
    
class AuthorizationApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        obj = Employee.objects.get(team__isnull = True)
        ser = EmployeeSerializer(obj, many=True)
        return Response(ser.data)
        