from django.shortcuts import render
# Create your views here.
import csv,os,json
from rest_framework import status
from psycopg2 import IntegrityError
from .models import response,fileName
from  rest_framework.views import APIView
from django.shortcuts import render, redirect
from  rest_framework.response import Response
from .serialiaers import serialiaersfileName,sResponse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

# Алгоритм для нахождения 5 клиентов, совершивших больше сделок за весь период
def algoritm(file):
    global result_username_money,gems_copy
    workPath = os.path.dirname(os.path.abspath(__file__))#путь к файлу
    with open(os.path.join(workPath, f"csv/{file}"), encoding='utf-8') as deals_csv:#читаем файл
        list_allObject_dealsCsv = [objects.replace(" ", "-").replace(",", "\n").split() for objects in deals_csv.readlines()]
        list_allObject_dealsCsv.remove(list_allObject_dealsCsv[0])  # Список из каждой строки csv файла--[['bellwether', 'Цаворит', '612', '6', '2018-12-14-08:29:52.506166'],.............]
        username = list(set([login[0] for login in list_allObject_dealsCsv]))  # Список логинов--['concoction', 'wallflower', 'viperliamk0125', 'nibblethew19', 'resplendent', 'snookered', 'fartkontrol', 'kismetkings213', 'braggadocio', 'buckaroo', 'bloviate', 'bellwether', 'nambypamby', 'turophile', 'monkeyydux', 'uvulaperfly117', 'majordomo', 'zygote4id3n']
        dictFrom_username_spentMoney_gems = {}  # {'braggadocio': (108957, ['Изумруд', 'Лунный-камень']),.......}
        sum_money = 0;list_allGems = []  # [['Цаворит', 'Спессартин', 'Аквамарин'],.....] список камней в конце получается NONE
        for login in username:
            for listObject_all in list_allObject_dealsCsv:
                if login in listObject_all:
                    sum_money += int(listObject_all[2])
                    list_allGems.append(listObject_all[1])
            dictFrom_username_spentMoney_gems[login] = sum_money, list(set(list_allGems))
            sum_money = 0;list_allGems = []
        dictFrom_username_spentMoney_gems = list(dictFrom_username_spentMoney_gems.items())  # [('concoction', (83562, ['Танзанит', 'Аметист', 'Топаз', 'Циркон', 'Аквамарин', 'Марганит'])),.....]
        dictFrom_username_spentMoney_gems.sort(key=lambda i: i[1][0])  # сортировка
        dictFrom_username_spentMoney_gems = [tuple for tuple in reversed(dictFrom_username_spentMoney_gems)]  # перевачивем список, чтобы получить сортировку по убыванию
        dictFrom_username_spentMoney_gems = [dictFrom_username_spentMoney_gems[i] for i in range(5)]  # получаем список из 5 клиентов с наибольшей сделок за весь период,но с не сортироваными камнями
        sum = 0;i = 0
        list_gems = []  # сортированые камни для 5 клиентов---->
        for dict in dictFrom_username_spentMoney_gems:
            list_gems.append([])
            for gems in dict[1][1]:
                for repeat in dictFrom_username_spentMoney_gems:
                    if gems in repeat[1][1]:
                        sum += 1
                if sum >= 2:
                    list_gems[i].append(gems)
                    sum = 0
                sum = 0
            i += 1
        result_username_money = dictFrom_username_spentMoney_gems #создаём экземпляр и объявляем глобальным
        gems_copy = list_gems


class SerializerfileName(APIView):
    def post(self, request):#отправим название файла csv,считываем и добавляем данные в базу данных
        serializer = serialiaersfileName(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            json_serealizarData = json.dumps(serializer.data["name_file"]).replace('"', "") #получаем название файла
            print(json_serealizarData)
            try:
                algoritm(json_serealizarData)  # отправляем в функцию название файла
            except:
                fileName.objects.get(name_file=json_serealizarData).delete()
                return Response("status:Файл не существует")
            for num in range(len(result_username_money)):#добавляем данные в базу данных
                response.objects.create(username=result_username_money[num][0],spent_money=int(result_username_money[num][1][0]), gems=gems_copy[num]).save()
            return Response("status:Ok")

        try:#если файл вызывается повторно, после какких-то измений,то выполним следующий код
            json_serealizarData = json.dumps(serializer.data["name_file"]).replace('"', "")#получаем название файла
            algoritm(json_serealizarData)
            for num in range(len(result_username_money)):
                for response_object in response.objects.all():#добавляем данные в базу данных
                    #данные которые есть в базе данных не добавляем
                    if response_object.username.__str__() == result_username_money[num][0] and response_object.spent_money.__int__() == int(result_username_money[num][1][0]) and response_object.gems.__str__() == gems_copy[num]:
                        pass

                    if response_object.username.__str__() == result_username_money[num][0]:#данные которые изменены добавим в базу данных
                        if response_object.spent_money.__int__() != int(result_username_money[num][1][0]) or response_object.gems.__str__() != gems_copy[num]:
                            response.objects.get(pk=response_object.id.__int__()).delete()
                            response.objects.create(username=result_username_money[num][0],spent_money=int(result_username_money[num][1][0]),gems=gems_copy[num]).save()
            return Response("status:Ok")
        except:
            return Response("status:Error")