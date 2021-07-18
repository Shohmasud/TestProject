from django.db import models

# Create your models here.
class response(models.Model):
    username = models.CharField(verbose_name='Логин клиента', db_index=True,max_length=400)
    spent_money = models.BigIntegerField(verbose_name='Сумма потраченных средств за весь период')
    gems = models.CharField(verbose_name='Список из названии камней,которые купили как минимум двое из списка клиентов', db_index=True,max_length=400)
    class Meta:
        verbose_name = '5 клиентов,потратившиx наибольшую сумму за весь период'
        ordering = ['spent_money']



class fileName(models.Model):
    name_file = models.CharField(verbose_name='Название файлов', db_index=True,unique=True,max_length=400)
    reletedFile = models.ManyToManyField(response,blank=True)
    class Meta:
        verbose_name = 'Файлы'
        ordering = ['id']