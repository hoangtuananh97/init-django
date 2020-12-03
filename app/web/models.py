from django.db import models

# Create your models here.
from app.users.models import User


class Consumer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=False, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'tb_consumer'
        verbose_name = 'Consumers'


class Good(models.Model):
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=3)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'tb_goods'
        verbose_name = 'Goods'


class Bill(models.Model):
    status_delivery = models.BooleanField(null=True, blank=True, default=False)
    total_money = models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=3)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'tb_bill'
        verbose_name = 'Bill'


class BillDetail(models.Model):
    consumer = models.ForeignKey(Consumer, null=True, blank=True,
                                 on_delete=models.DO_NOTHING,
                                 related_name='bd_relate_consumer')
    good = models.ForeignKey(Good, null=True, blank=True,
                             on_delete=models.DO_NOTHING,
                             related_name='bd_relate_good')
    bill = models.ForeignKey(Bill, null=True, blank=True,
                             on_delete=models.DO_NOTHING,
                             related_name='bd_relate_bill')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'tb_bill_detail'
        verbose_name = 'Bill Detail'


class StaffPerformBill(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING,
                             related_name='staff_relate_user')
    bill = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.DO_NOTHING,
                             related_name='staff_relate_bill')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'tb_staff_perform_bill'
        verbose_name = 'Staff Perform Bill'
