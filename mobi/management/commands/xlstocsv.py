import xlrd
import csv
from geopy.geocoders import Nominatim
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    loc = ("Places-Europe-TC.xls")

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    nom = Nominatim(user_agent="CSVToLatLong")

    u = open('new_universities', 'w')
    c = open('new_cities', 'w')
    co = open('new_countries', 'w')

    writer_u = csv.writer(u)
    writer_c = csv.writer(c)
    writer_co = csv.writer(co)

    writer_co.writerow(["name", "continent", "ECTSConversion", "id"])
    writer_c.writerow(["name", "country", "id"])
    writer_u.writerow(["name", "city", "univ_appartment", "latitude", "longitude", "id"])

    countrytemp = None
    citytemp = None
    idCo = 2
    idC = 2

    for i in range(1, sheet.nrows):
        country = sheet.cell_value(i, 0)
        city = sheet.cell_value(i, 1)
        if country == "":
            break
        if country != countrytemp:
            writer_co.writerow([country, "Europe", "1"])
            idCo += 1
        if city == "":
            break
        if city != citytemp:
            writer_c.writerow([sheet.cell_value(i, 1), idCo])
            idC += 1

        countrytemp = country
        citytemp = city

        try:
            print(sheet.cell_value(i, 3))
            n = nom.geocode(sheet.cell_value(i, 3))
            lat = n.latitude
            lon = n.longitude
            writer_u.writerow([sheet.cell_value(i, 3), idC, "False", lat, lon])
        except AttributeError:
            writer_u.writerow([sheet.cell_value(i, 3), idC, "False"])

    u.close()
    c.close()
    co.close()


