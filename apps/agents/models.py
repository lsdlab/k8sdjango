import time
import uuid
from django.db import models
from apps.core.models import TimestampedModel
import shortuuid


class Broker(TimestampedModel):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False, default='')
    mobile = models.CharField(max_length=11, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '采购人'
        verbose_name_plural = verbose_name


class Customer(TimestampedModel):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False, default='')
    mobile = models.CharField(max_length=11, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '买家'
        verbose_name_plural = verbose_name


class CustomerOrder(TimestampedModel):
    SUCCESS = '1'
    MANUAL_CLOSE = '2'
    WIP = '3'
    DEALED = '4'
    STATUS_CHOICE = (
        (SUCCESS, '创建成功'),
        (MANUAL_CLOSE, '手动关闭'),
        (WIP, '接单中'),
        (DEALED, '接单完成'),
    )
    name = models.CharField(max_length=255,
                            blank=False,
                            help_text='用户名+时间戳字符串')
    sn = models.CharField(max_length=255, blank=False)
    status = models.TextField(max_length=1,
                              choices=STATUS_CHOICE,
                              default=SUCCESS,
                              blank=False)
    buyer_note = models.TextField(blank=True, default='')

    def __str__(self):
        return self.sn

    def save(self, *args, **kwargs):
        if not self.sn:
            self.sn = str(time.time()).replace('.', '') + shortuuid.ShortUUID(
                alphabet="0123456789").random(length=9)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '需求订单'
        verbose_name_plural = verbose_name


class BrokerOrder(TimestampedModel):
    STOCK = '1'
    WAITTING = '2'
    PURCHASED = '3'
    STATUS_CHOICE = (
        (STOCK, '现货'),
        (WAITTING, '待采购'),
        (PURCHASED, '采购完成'),
    )
    name = models.CharField(max_length=255,
                            blank=False,
                            help_text='用户名+时间戳字符串')
    sn = models.CharField(max_length=255, blank=False)
    status = models.TextField(max_length=1,
                              choices=STATUS_CHOICE,
                              default=STOCK,
                              blank=False)
    seller_note = models.TextField(blank=True, default='')
    broker = models.ForeignKey('Broker',
                               on_delete=models.CASCADE,
                               related_name='broker_broker_orders',
                               blank=False,
                               null=False)

    def __str__(self):
        return self.sn

    def save(self, *args, **kwargs):
        if not self.sn:
            self.sn = str(time.time()).replace('.', '') + shortuuid.ShortUUID(
                alphabet="0123456789").random(length=9)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '采购订单'
        verbose_name_plural = verbose_name


class ShippingOrder(TimestampedModel):
    SUCCESS = '1'
    TIMEOUT_CLOSE = '2'
    MANUAL_CLOSE = '3'
    PAID = '4'
    SELLER_PACKAGED = '5'
    RECEIVE = '6'
    REVIEW = '7'
    STATUS_CHOICE = (
        (SUCCESS, '创建成功-待支付'),
        (TIMEOUT_CLOSE, '支付超时-订单关闭'),
        (MANUAL_CLOSE, '手动关闭订单'),
        (PAID, '支付完成-待发货'),
        (SELLER_PACKAGED, '已发货-待收货'),
        (RECEIVE, '已收货-待评价'),
        (REVIEW, '已评价-交易完成'),
    )
    EXPRESS = '1'
    COLLECT = '2'
    EXPRESS_TYPE_CHOICE = ((EXPRESS, '快递'), (COLLECT, '自提'))
    name = models.CharField(max_length=255,
                            blank=False,
                            help_text='用户名+时间戳字符串')
    sn = models.CharField(max_length=255, blank=False)
    status = models.TextField(max_length=1,
                              choices=STATUS_CHOICE,
                              default=SUCCESS,
                              blank=False)
    total_amount = models.DecimalField(max_digits=8,
                                       decimal_places=2,
                                       blank=False)
    note = models.TextField(blank=True, default='')
    express_type = models.TextField(max_length=1,
                                    choices=EXPRESS_TYPE_CHOICE,
                                    default=EXPRESS,
                                    blank=False)
    closed_datetime = models.DateTimeField(blank=True, null=True)
    seller_packaged_datetime = models.DateTimeField(blank=True, null=True)
    received_datetime = models.DateTimeField(blank=True, null=True)
    paid = models.DecimalField(max_digits=8,
                               decimal_places=2,
                               blank=True,
                               default=0.00)
    payment_sn = models.CharField(max_length=255, blank=True, default='')
    payment_datetime = models.DateTimeField(blank=True, null=True)
    customer_order = models.OneToOneField(
        'CustomerOrder',
        on_delete=models.SET_NULL,
        related_name='customer_order_shipping_order',
        blank=True,
        null=True)

    def __str__(self):
        return self.sn

    def save(self, *args, **kwargs):
        if not self.sn:
            self.sn = str(time.time()).replace('.', '') + shortuuid.ShortUUID(
                alphabet="0123456789").random(length=9)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '出货订单'
        verbose_name_plural = verbose_name


class OrderProduct(TimestampedModel):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False, default='')
    customer_order = models.ForeignKey(
        'CustomerOrder',
        blank=False,
        on_delete=models.CASCADE,
        related_name='customer_order_order_products')
    standard_product = models.ForeignKey(
        'StandardProduct',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='standard_product_order_products')
    broker_order = models.OneToOneField(
        'BrokerOrder',
        on_delete=models.SET_NULL,
        related_name='broker_order_order_product',
        blank=True,
        null=True)
    nums = models.IntegerField(default=1)
    except_price = models.DecimalField(max_digits=8,
                                       decimal_places=2,
                                       blank=False,
                                       help_text='期待价格')
    total_amount = models.DecimalField(max_digits=8,
                                       decimal_places=2,
                                       blank=False,
                                       help_text='总金额')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name


class StandardProduct(TimestampedModel):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False, default='')
    available_in = models.CharField(max_length=255, blank=False)
    price_range = models.CharField(max_length=255, blank=False)
    purchase_price = models.CharField(max_length=255, blank=False)
    header_image = models.URLField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '标准商品'
        verbose_name_plural = verbose_name
