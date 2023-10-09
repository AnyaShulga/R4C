from django.core import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render

from orders.models import Order
from robots.models import Robot


# Create your views here.
def new_order(request):
    if request.method == "POST":
        robot = request.POST("serial")
        email = request.POST("email")
        order = Order(customer=email, robot_serial=robot)
        order.save()
        if not Robot.objects.get(serial=robot).exists():
            num_order = cache.get('waiting list')
            if num_order is not None:
                num_order.append(order.pk)
                cache.set('waiting list', num_order)
            else:
                cache.set('waiting list', [order.pk])


@receiver(signal=post_save, sender=Robot)
def send_email(instance: Robot):
    waiting_list = cache.get('waiting list')
    mail_order = Order.objects.filter(pk__in=waiting_list).filter(robot_serial__exact=instance.serial)
    if mail_order.exists():
        send_email(
            'Робот в наличии',
            f'Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n'
            'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
            example@example.com,
            [customer.email for customer in mail_order]
        )
