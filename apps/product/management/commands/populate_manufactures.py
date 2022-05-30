from random import  random, randrange
from django.core.management.base import BaseCommand
from faker import Faker
import logging
from apps.groups.models import Groups

from apps.product.models import Manufactures



logging.getLogger('faker').setLevel(logging.ERROR)
class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker()

        manufacture_datas = set(["Epson","Nikon","Panasonic","Pentax","Pioneer","Planex","Ricoh","Sharp","SII,Sony","Denon,Toshiba,Acer","Asus","BenQ","ECS,Gigabyte","MSI","Soyo","TSMC","VIA Technologies","SURYA","Aigo","Haier","TCL","BBK Electronics","Huawei","Lenovo","OnePlus","Oppo","Vivo","Xiaomi","Voltas","Behringer","Beyerdynamic","Blaupunkt","EnOcean","Epcos","Grundig","Hama Photo","Loewe","Sennheiser","Siemens","Ultrasone	","Wortmann","LG","Electronics","Samsung ","Electronics","Hynix","Cowon","Humax","Philips","Epyon","Funke Digital TV","Teleplan","TomTom","Trust","Abercrombie & Fitch Co","Adidas Group","Arcadia Group","BCBG Max Azria Group Inc","Buckle Inc","C&J Clark International","Cato Corporation","Columbia Sportswear Company","Gerber Technology","Gildan Activewear Inc","Global Brands Group","Hanesbrands Inc","Iconix Brand Group Inc","JC Penney Company Inc","Levi Strauss & Co","Marks & Spencer Group Plc","Primark","Puma AG","PVH Corporation","Rocky Brands Inc","Sears Holdings Corporation","Steven Madden","Timberland Company","Under Armour Inc","Uniqlo","VF Corporation","Victoria's Secret","Wal-Mart Stores Inc","Zumiez Inc","KI","Vitra","Kinnarps","Teknion","Flexsteel Furniture","Poltrona Frau","NowyStyl Group","Ahrend","OFS","VS","USM","Sedus","Virco","Senator","Bene","AIS","Flokk","Dauphine Group"])

        print('======================== Stard Manufactures DB Seed process =======================')
        Manufactures.objects.all().delete()
        for data in manufacture_datas:
            rand_group = Groups.objects.order_by('?').first()
            manufactur = Manufactures()
            manufactur.name           = data.strip()
            manufactur.description    = fake.paragraph(nb_sentences=15) #optional
            manufactur.website        = fake.uri()
            manufactur.is_active      = 1
            manufactur.group_id       = rand_group.id
            manufactur.owner_id       = 1
            manufactur.save()

        print('======================== End Manufactures DB Seed process =======================')