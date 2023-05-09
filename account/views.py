from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import response


class TestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return response.Response(status=200, data={'message': 'fine'})
