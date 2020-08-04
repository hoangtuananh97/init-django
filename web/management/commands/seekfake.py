from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, UNUSABLE_PASSWORD_SUFFIX_LENGTH, get_hasher
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker
import random as rd

from faker.generator import random

from users.models import User
from web.models import Good, Consumer, BillDetail, Bill, StaffPerformBill

fake = Faker('en_US')
choices = [0, 1]


class Command(BaseCommand):
    help = 'Fake data'

    def add_arguments(self, parser):
        parser.add_argument('record', type=int, help='ABC')

    def handle(self, *args, **options):
        records = options['record']

        for _ in range(records):
            Good.objects.create(
                code=fake.pystr(),
                name=fake.name(),
                status=1,
                price=random.randint(1, 7),
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                is_deleted=rd.choice(choices)
            )

        for _ in range(records):
            email = fake.email()
            User.objects.create(
                password=make_password(fake.password(length=12)),
                username=email,
                email=email,
                last_name=fake.last_name(),
                first_name=fake.first_name(),
                is_staff=rd.choice(choices),
                is_active=rd.choice(choices),
                date_joined=fake.date_time_this_year()
            )

        for _ in range(records):
            Consumer.objects.create(
                name=fake.name(),
                email=fake.email(),
                password=make_password(fake.password(length=12)),
                phone=fake.phone_number(),
                address=fake.address(),
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                is_deleted=rd.choice(choices)
            )
        for _ in range(records):
            Bill.objects.create(
                status_delivery=rd.choice(choices),
                total_money=random.randint(1, 10),
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                is_deleted=rd.choice(choices)
            )

        for _ in range(records):
            StaffPerformBill.objects.create(
                user=rd.choice(User.objects.all()),
                bill=rd.choice(Bill.objects.all()),
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                is_deleted=rd.choice(choices)
            )

        # for _ in range(records):
        #     BillDetail.objects.create(
        #         consumer=Consumer.objects.all(),
        #         bill=Bill.objects.all(),
        #         good=Good.objects.all(),
        #         created_at=fake.date_time(),
        #         updated_at=fake.date_time(),
        #         is_deleted=rd.choice(choices)
        #     )


def make_password(password, salt=None, hasher='default'):
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH)
    hasher = get_hasher(hasher)
    salt = salt or hasher.salt()
    return hasher.encode(password, salt)
