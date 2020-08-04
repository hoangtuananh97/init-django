import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

import random as rd
from web.models import Consumer, Good, Bill, BillDetail, StaffPerformBill
from faker import Faker

fake_gen = Faker()
choices = [0, 1]



def gene_consumer(n=5):
    for entry in range(n):
        fake_name = fake_gen.name()
        fake_email = fake_gen.email()
        fake_pass = fake_gen.msisdn()
        fake_phone = fake_gen.phone_number()
        fake_address = fake_gen.address()
        fake_created_at = fake_gen.date()
        fake_updated_at = fake_gen.date()
        consumer = Consumer.objects.get_or_create(name=fake_name, email=fake_email,
                                                  password=fake_pass,
                                                  phone=fake_phone,
                                                  address=fake_address, created_at=fake_created_at,
                                                  updated_at=fake_updated_at, is_deleted=rd.choice(choices))


def gen_good(n=5):
    name_good_choices = ['sponge cake', 'cornflour',
                         'grape', 'grapefruit', 'bread rolls',
                         'yoghurt', 'salami', 'liver',
                         'cheese', 'chicken', 'cottage cheese']
    for i in range(n):
        fake_code = fake_gen.bothify()
        fake_price =



if __name__ == '__main__':
    gene_consumer(5)





