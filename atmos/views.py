from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
def translate_months_genitive(rus_months):
        # Ruscha (genitive) -> Inglizcha oy nomlari tarjimasi
        months_translation = {
            "января": "January",
            "февраля": "February",
            "марта": "March",
            "апреля": "April",
            "мая": "May",
            "июня": "June",
            "июля": "July",
            "августа": "August",
            "сентября": "September",
            "октября": "October",
            "ноября": "November",
            "декабря": "December"
        }

        # Tarjima va 3 harfli qisqartmalar ro'yxatini qaytarish
        eng_abbr = [months_translation[month][:3] for month in rus_months if month in months_translation]
        return eng_abbr
def get_children_second_classes(soup, parent_class):
        """
        Berilgan class_name ga ega barcha elementlarning
        birinchi bolaning ikkinchi classini ro'yxat sifatida qaytaradi.
        """
        results = []
        parents = soup.find_all(class_=parent_class)

        for parent in parents:
            child = parent.find()
            if child:
                class_list = child.get('class', [])
                if len(class_list) > 1:
                    results.append(class_list)
                elif class_list:
                    results.append("Faqat bitta class mavjud.")
                else:
                    results.append("Class mavjud emas.")
            else:
                results.append("Bola topilmadi.")
        
        return results
def get_dates(region):
    url = f"https://sinoptik.ua/ru/pohoda/{region}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Xatolik yuz berdi: {response.status_code}")
        soup = None

    def get_text_by_class(class_name):
            if not soup:
                print("Soup obyekt mavjud emas.")
                return []

            elements = soup.find_all(class_=class_name)
            texts = [el.get_text(strip=True) for el in elements]

            return texts
    
    def raqam_atrofini_ol(matnlar):
        natija = []
        for matn in matnlar:
            for i in range(len(matn)):
                if matn[i] in '+-' and i + 1 < len(matn) and matn[i+1].isdigit():
                    # Raqamning boshlanishi topildi
                    start = i
                    end = i + 1
                    while end < len(matn) and matn[end].isdigit():
                        end += 1

                    # Oldidagi 1 ta belgi
                    old_belgi = matn[start - 1] if start - 1 >= 0 else ''
                    # Raqamning o'zi
                    raqam = matn[start:end]
                    # Keyingi 1 ta belgi
                    keyingi_belgi = matn[end] if end < len(matn) else ''

                    # Barcha uch qismni birlashtirish
                    natija.append(old_belgi + raqam + keyingi_belgi)
                    break  # bitta raqam topilishi kifoya
        return natija

    def get_second_classes_from_soup(target_class):
        elements = soup.find_all(class_=target_class)
        second_classes = []

        for element in elements:
            class_list = element.get('class')
            if class_list and len(class_list) >= 2:
                second_classes.append(class_list[1])
        print(second_classes,1)
        return second_classes


    fullData=raqam_atrofini_ol(get_text_by_class("+Ncy59Ya"))
    minTemps=[]
    maxTemps=[]
    for i in range(len(fullData)):
        if (i+1)%2==0: maxTemps.append(fullData[i])
        else:
            minTemps.append(fullData[i])








    dates=get_text_by_class("RSWdP9mW")
    months=get_text_by_class("yQxWb1P4")
    iconClass=get_second_classes_from_soup("bSOXy2ra")
    hours=get_text_by_class("lgo8NaQM")[4:12]
    hourlyIcons=get_children_second_classes(soup,"WxisTPVu")
    hourlyTemps=get_text_by_class("lgo8NaQM")[20:28]
    months=translate_months_genitive(months)

    return dates,months,iconClass,hours,hourlyIcons,hourlyTemps,months,minTemps,maxTemps
def get_week_weather(regio):
    def get_text_by_class(class_name):
        if not soup:
            print("Soup obyekt mavjud emas.")
            return []

        elements = soup.find_all(class_=class_name)
        texts = [el.get_text(strip=True) for el in elements]

        return texts
    url = f"https://sinoptik.ua/ru/pohoda/{regio}"
    response = requests.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Xatolik yuz berdi: {response.status_code}")
        soup = None
    elements = soup.find_all('a', class_='tkK415TH')
    links = [el['href'] for el in elements[1:] if 'href' in el.attrs]
    datesML=get_text_by_class("RSWdP9mW")
    monthsML=get_text_by_class("yQxWb1P4")
    hourlyIconsML=[]
    hoursML=[]
    hourlyTempsML=[]
    elements = soup.find_all(class_="lgo8NaQM")
    texts = [el.get_text(strip=True) for el in elements]
    hoursML.append(texts[4:12])
    hourlyIconsML.append(get_children_second_classes(soup,"WxisTPVu"))
    elements = soup.find_all(class_="lgo8NaQM")
    teksts = [el.get_text(strip=True) for el in elements]
    hourlyTempsML.append(teksts[20:28])
    for e, i in enumerate(links):
            url = f"https://sinoptik.ua{i}"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Xatolik yuz berdi: {response.status_code}")
                soup = None
            if soup!=None:
                elements = soup.find_all(class_="lgo8NaQM")
                texts = [el.get_text(strip=True) for el in elements]
                if e==0 : 
                    hoursML.append(texts[4:12])
                    print(True)
                else: 
                    hoursML.append(texts[4:8])
                    print(i)
                hourlyIconsML.append(get_children_second_classes(soup,"WxisTPVu"))
                elements = soup.find_all(class_="lgo8NaQM")
                teksts = [el.get_text(strip=True) for el in elements]
                if e==0: hourlyTempsML.append(teksts[20:28])
                else: hourlyTempsML.append(texts[12:16])
    return hoursML, hourlyIconsML, hourlyTempsML,datesML,monthsML
                





    

class CustomGetApiView(APIView):
    def get(self, request):
        # API chaqirilganda ma'lumot olib kel
        region=request.GET.get("region","beruni")
        datesData = get_dates(region)
        dates, months, iconClass, hours, hourlyIcons, hourlyTemps, months, minTemps, maxTemps = datesData

        data = {
            "iconDays": iconClass,
            "minTempDays": minTemps,
            "maxTempDays": maxTemps,
            "dateDays": dates,
            "hours": hours,
            "tempHours": hourlyTemps,
            "months": months,
            "hourlyIcons":hourlyIcons
        }
        return Response(data)
class Asus(APIView):
    def get(self, request):
        region=request.GET.get("region","beruni")
        hoursML, hourlyIconsML, hourlyTempsML,datesML,monthsML= get_week_weather(region)

        data = {
            "hours": hoursML,
            "hourlyIcons": hourlyIconsML,
            "hourlyTemps": hourlyTempsML,
            "dates":datesML,
            "months":translate_months_genitive(monthsML)
        }
        return Response(data)