from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

class TestView(APIView):
    def get(self,request,*args,**kwargs):
        data = {
            'name':'deen',
            'age':'ds',
            'hack':'works',
            'this':'works'
        }
        return Response(data)