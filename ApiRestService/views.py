from django.shortcuts import render
# Create your views here.
import csv,os,json
from rest_framework import status
from psycopg2 import IntegrityError
from .models import response,fileName
from  rest_framework.views import APIView
from django.shortcuts import render, redirect
from  rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect