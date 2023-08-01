from django.db import models


class Consignment(models.Model):
    key_id = models.CharField(max_length=16, unique=True) # Ключ партии товара в Альта-СВХ. 
    contact = models.IntegerField(blank=True, null=True) # Код клиента 
    contact_name = models.CharField(max_length=150, blank=True, default='') # Наименование клиента
    contact_broker = models.IntegerField(blank=True, null=True) # Код брокера оформляющего товар
    broker_name = models.CharField(max_length=150, blank=True,  default='') # Наименование брокера
    nttn = models.CharField(max_length=100, blank=True, default='') # Номер транспортного документа
    nttn_date = models.DateField(blank=True, null=True) # Дата транспортного документа
    goods = models.CharField(max_length=100, blank=True, default='') # Номер документа доставки
    weight = models.FloatField(default=0) # Вес партии товара
    dater = models.DateTimeField(blank=True, null=True) # Дата регистрации партии товара
    dateo = models.DateTimeField(blank=True, null=True) # Дата выдачи партии товара со склада
    id_enter = models.CharField(max_length=8, blank=True, default='') # Id пропуска въезда транпортного средства на терминал
    car =  models.CharField(max_length=30, blank=True, default='') # Номер транспортного средства 
    d_in = models.DateTimeField(blank=True, null=True) # Дата въезда транспортного средства на терминал
    d_out = models.DateTimeField(blank=True, null=True) # Дата выезда транспортного средства с терминала 

    guid_user = models.CharField(max_length=36, blank=True, default='') # GUID пользователя который создал эту запись
    datep = models.DateTimeField(auto_now_add=True) # Дата создания записи
    posted = models.BooleanField(default=False) # флаг проводки
    post_date = models.DateTimeField(blank=True, null=True) # дата проводки
    post_user_id = models.CharField(max_length=36, blank=True, default='') # идентификатор пользователя  который провел запись
    was_posted = models.BooleanField(default=False) # флаг первичной проводки

    class Meta:
        managed = False
        db_table = 'svh_service_consignment'
        ordering = ['-id']


class Contact(models.Model):
    contact = models.IntegerField(unique=True) # Код клиента из программы Альта-СВХ
    type = models.CharField(max_length=1, blank=True, default='') # Тип пользователя
    name = models.CharField(max_length=150, blank=True, default='') # Наименование организации
    inn = models.CharField(max_length=12, blank=True, default='') # ИНН организации
    fio = models.CharField(max_length=100, blank=True, default='') # ФИО физлица организации. ФИО оператора СВХ
    email0 = models.CharField(max_length=100, blank=True, default='') # Почта для смены пароля и контактов по работе портала
    email1 = models.CharField(max_length=100, blank=True, default='') # Почта отсылки сообщений
    email2 = models.CharField(max_length=100, blank=True, default='') # Почта для передачи документов партии товара
    idtelegram = models.CharField(max_length=36, blank=True, default='') # Идентификатор ID messenger Telegram
    tags = models.CharField(max_length=100, blank=True, default='') # Список хэштегов
    login = models.CharField(max_length=30, blank=True, default='') # Логин клиента (организации)
    pwd = models.CharField(max_length=20, blank=True, default='') # Пароль входа в портал. Должен быть зашифрован

    f_stop = models.BooleanField(default=False) # Флаг приостановки пользования порталом
    guid_user = models.CharField(max_length=36, blank=True, default='') # GUID пользователя который создал эту запись
    datep = models.DateTimeField(auto_now_add=True) # Дата создания записи
    posted = models.BooleanField(default=False) # флаг проводки
    post_date = models.DateTimeField(blank=True, null=True) # дата проводки
    post_user_id = models.CharField(max_length=36, blank=True, default='') # идентификатор пользователя  который провел запись 


    class Meta:
        managed = False
        db_table = 'svh_service_contact'
        ordering = ['-id']
        

class Document(models.Model):
    docnum = models.CharField(max_length=36) # Номер документа
    docdate = models.DateTimeField(blank=True, null=True) # Дата документа
    docname = models.CharField(max_length=100, blank=True, default='') # Наименование документа
    file = models.FileField(upload_to='documents/', blank=True, null=True)

    docbody = models.BinaryField(blank=True, null=True) # Содержимое документа. Может быть zip
    f_zip = models.BooleanField(blank=True, default=False) # файл архивирован/неархивирован
    nfile = models.CharField(max_length=100, blank=True, default='') # Наименование файла
    guid_partia = models.CharField(max_length=100) # Ссылка на партию товара (key_id)
    guid_mail = models.CharField(max_length=36, blank=True, default='') # Uemail.guid. guid письма которое отослал этот документ 
    dates = models.DateTimeField(blank=True, null=True) # Дата отправки письма c документом

    guid_user = models.CharField(max_length=36, blank=True, default='') # GUID пользователя который создал эту запись
    datep = models.DateTimeField(auto_now_add=True) # Дата создания записи

    class Meta:
        managed = False
        db_table = 'svh_service_document'
        ordering = ['-id']


class Message(models.Model):
    guid_partia = models.CharField(max_length=36) # id Партии товара
    contact = models.IntegerField() # Код клиента 
    txt = models.CharField(max_length=200) # Сообщение
    datep = models.DateTimeField(auto_now_add=True) # Дата создания записи
    dater = models.DateTimeField() # Дата прочтения сообщения    

    class Meta:
        managed = False
        db_table = 'svh_service_message'
        ordering = ['-id']