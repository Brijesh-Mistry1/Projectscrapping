# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	cust_name = models.CharField('Customer Name', max_length=160)
	cust_status = models.BooleanField('Status', default=True)


class Sites(models.Model):
	site_name = models.CharField('Site Name', max_length=160)
	site_status = models.BooleanField('Status', default=True)
	select_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	# cust_id = models.ManyToManyField(Customer, related_name="customer_id", blank=True)


class Routers(models.Model):
	router_name = models.CharField('Router Name', max_length=180)
	router_status = models.BooleanField('Status', default=True)
	select_site = models.ForeignKey(Sites, on_delete=models.CASCADE)
	# site_id = models.ManyToManyField(Sites, related_name="site_id", blank=True)
	access_id = models.CharField('Access ID', max_length=200)
	access_pwd = models.CharField('Access Password', max_length=180)
	access_url = models.URLField('Access URL', max_length=200)
	brand = models.CharField('Brand', max_length=160)
	firmware = models.CharField('Firmware', max_length=160)


class RouterOverviewLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ip_add = models.CharField('IP Address', max_length=100)
	curr_datetime = models.DateTimeField('Current Datetime')
	firmware = models.CharField('Firmware Version', max_length=160)
	router_uptime = models.CharField('Router Uptime', max_length=200)
	local_device_time = models.CharField('Local Device Time', max_length=200)
	memoryusage_RAM = models.CharField('RAM Memory Usage', max_length=160)
	memoryusage_Flash = models.CharField('Flash Memory Usage', max_length=160)