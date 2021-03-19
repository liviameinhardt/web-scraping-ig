# -*- coding: utf-8 -*-
"""
Created on Sex Jan 22 2021

@author: livia
"""

#tratamento dos dados do instagram

import re
from datetime import date
from datetime import datetime


def trata_data(data):
    data = data.split("T")[0]
    return datetime.strptime(data, '%Y-%m-%d').date().strftime('%d-%m-%Y')


def trata_curtidas(texto):
    return float(re.sub(r"( curtidas| visualizações)","",texto))
    


"""
def trata_data(data):
    
    mes_conv = {"JANEIRO":"01","FEVEREIRO":"02", "MARÇO":"03","ABRIL":"04","MAIO":"05",
                "JUNHO":"06","JULHO":"07","AGOSTO":"08","SETEMBRO":"09","OUTUBRO":"10","NOVEMBRO":"11","DEZEMBRO":"12"}
                
    if "HORA" in data:
        data = date.today().strftime('%d-%m-%y')
    elif "DIA" in data:
        d = re.compile(r'(HÁ | DIAS| DIA)')
        data = d.sub("",data)
        today = date.today()
        data = f"{today.day - int(data)}-{today.month}-{today.year}"
    else:
        data = re.sub(r" DE "," ",data)
        for mes,valor in mes_conv.items():
            if mes in data:
                m = re.compile(rf" {mes} ")
                data = m.sub(rf"-{valor}-",data)
        
    return data
"""



