from django import forms
from .models import Consignment, Carpass, Contact, Document
from django.contrib.admin.widgets import AdminDateWidget


class ConsignmentForm(forms.ModelForm):
    class Meta:
        model = Consignment
        fields = ['key_id', 'contact', 'contact_name', 'contact_broker', 'broker_name', 'nttn', 'nttn_date',
                  'dkd', 'dkd_date', 'goods', 'weight', 'dater', 'dateo', 'id_enter', 'car', 'd_in', 'd_out']
        # fields = '__all__'

        widgets = {
            'key_id': forms.HiddenInput(),
            'nttn_date': forms.DateInput(attrs=dict(type='date')),
            'dkd_date': forms.DateInput(attrs=dict(type='date')),
        }

        labels = {
            'key_id': 'ID партии товара', 
            'contact': 'Код клиента', 
            'contact_name': 'Наименование клиента', 
            'contact_broker': 'Код брокера', 
            'broker_name': 'Наименование брокера', 
            'nttn': '№ транспортного документа', 
            'nttn_date': 'Дата транспортного документа',
            'dkd': '№ документа доставки',
            'dkd_date': 'Дата документа доставки',
            'goods': 'Описание товаров', 
            'weight': 'Вес партии товара', 
            'dater': 'Дата регистрации партии товара', 
            'dateo': 'Дата выдачи партии товара со склада', 
            'id_enter': 'ID пропуска въезда ТС на терминал', 
            'car': 'Номер ТС', 
            'd_in': 'Дата въезда ТС на терминал', 
            'd_out': 'Дата выезда ТС с терминала',
        }

        # help_texts = {
        #     'dater': 'format: yyyy-mm-dd hh:mm:ss',
        #     'dateo': 'format: yyyy-mm-dd hh:mm:ss',
        #     'd_in': 'format: yyyy-mm-dd hh:mm:ss',
        #     'd_out': 'format: yyyy-mm-dd hh:mm:ss',
        # }
        # labels = {
        # }

class ConsignmentFiltersForm(forms.Form):
    key_id = forms.CharField(label='ID партии', max_length=16, required=False)
    contact_name = forms.CharField(label='Клиент', max_length=150, required=False)
    broker_name = forms.CharField(label='Брокер', max_length=150, required=False)
    dater_from = forms.DateField(label='Дата регистрации, c', widget=forms.DateInput(attrs=dict(type='date')), required=False)
    dater_to = forms.DateField(label='по', widget=forms.DateInput(attrs=dict(type='date')), required=False)
    nttn =  forms.CharField(label='№ транспортного документа', max_length=100, required=False)
    dateo_from = forms.DateField(label='Дата выдачи, с', widget=forms.DateInput(attrs=dict(type='date')), required=False)
    dateo_to = forms.DateField(label='по', widget=forms.DateInput(attrs=dict(type='date')), required=False)
    dkd = forms.CharField(label='№ документа доставки', max_length=100, required=False)
    car = forms.CharField(label='ТС', max_length=30, required=False)
    on_terminal = forms.BooleanField(label='На складе', widget=forms.CheckboxInput(), initial=True, required=False)


class CarpassFiltersForm(forms.Form):
    id_enter = forms.CharField(label='ID пропуска', max_length=8, required=False)
    dateen_from = forms.DateField(label='Дата въезда, с', widget=forms.DateInput(attrs=dict(type='date')), required=False)
    dateen_to = forms.DateField(label='Дата въезда, по', widget=forms.DateInput(attrs=dict(type='date')), required=False)
    ncar = forms.CharField(label='ТС', max_length=255, required=False)
    ntir = forms.CharField(label='№ документа доставки', max_length=50, required=False)
    nkont = forms.CharField(label='№ контейнера', max_length=50, required=False)

    
class CarpassForm(forms.ModelForm):
    class Meta:
        model = Carpass
        fields = ['guid', 'id_enter', 'ncar', 'dateen', 'timeen', 'ntir', 'nkont',
                  'driver', 'drv_man', 'dev_phone', 'contact', 'contact_name', 'contact_broker', 'broker_name', 'place_n', 'dateex', 'timeex']
        # fields = '__all__'

        widgets = {
            'guid': forms.HiddenInput(),
            'id_enter': forms.HiddenInput(),
            'dateen': forms.DateInput(attrs=dict(type='date')),
            'dateex': forms.DateInput(attrs=dict(type='date')),
        }

        labels = {
            # 'guid': 'Уникальный идентификатор записи', 
            # 'id_enter': 'ID пропуска въезда ТС на терминал', 
            'ncar': 'Номер ТС', 
            'dateen': 'Дата въезда', 
            'timeen': 'Время въезда', 
            'ntir': 'Номер документа доставки', 
            'nkont': 'Номер контейнера', 
            'driver': 'Наименование перевозчика', 
            'drv_man': 'ФИО водителя', 
            'dev_phone': 'Телефон водителя для связи', 
            'contact': 'Код клиента', 
            'contact_name': 'Наименование клиента', 
            'contact_broker': 'Код брокера', 
            'broker_name': 'Наименование брокера', 
            'place_n': 'Номер стоянки', 
            'dateex': 'Дата выезда',
            'timeex': 'Время выезда', 
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        # fields = '__all__'
        fields = ['guid_partia', 'id_enter', 'docnum', 'docdate', 'docname', 'file']

        widgets = {
            'guid_partia': forms.HiddenInput(),
            'id_enter': forms.HiddenInput(),
        }

        labels = {
            'docnum': 'Номер документа', 
            'docdate': 'Дата документа', 
            'docname': 'Наименование документа', 
            'file': 'Файл', 
        }
