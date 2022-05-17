
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customer, Sites, Routers, RouterOverviewLog
import time
from datetime import datetime, timedelta
from django.utils import timezone
from .forms import CustomerAddForm, SiteAddForm, RouterAddForm, RouterOverviewForm, RevealPasswordForm
import scrapy
import requests
import sys, json, socket
from bs4 import BeautifulSoup


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


def display_customer(request):
    customers = Customer.objects.all()
    return render(request,'ui-customer.html',{'customers':customers})

def display_site(request):
    sites = Sites.objects.all()
    return render(request,'ui-site.html',{'sites':sites})

def display_router(request):
    routers = Routers.objects.all()
    return render(request,'ui-router.html',{'routers':routers})


# customer menu operations
def save_customer(request):
    if request.method == "POST":
        form = CustomerAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/customer")
        else:
            msg = 'Failed to save!'

def edit_customer(request, id):
    customers = Customer.objects.get(id=id)
    return render(request,'edit-customer.html', {'customers':customers})

def update_customer(request, id):
    customers = Customer.objects.get(id=id)
    form = CustomerAddForm(request.POST, instance = customers)
    if form.is_valid():
        form.save()
        return redirect("/customer")
    return render(request, 'edit-customer.html', {'customers':customers})

def delete_customer(request, id):
    # customers = Customer.objects.get(id=id)
    customers = Customer.objects.all()
    if Sites.objects.filter(select_customer=id):
        message = "Sorry.. you have to delete its associated site first!"  
        return render(request,'ui-customer.html',{'customers':customers, 'message':message})  
        # return redirect("/customer")
    else:
        customers = Customer.objects.get(id=id)
        customers.delete()  
        return redirect("/customer")


# site menu operations
def add_site(request):
    customers = Customer.objects.filter(cust_status=True)
    return render(request,'add-site.html',{'customers':customers})

def submit_site(request):
    if request.method == "POST":
        form = SiteAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/site")
        else:
            msg = 'Failed to save!'

def edit_site(request, id):
    site = Sites.objects.get(id=id)
    customers = Customer.objects.all()
    return render(request,'edit-site.html',{'site':site, 'customers':customers})

def update_site(request, id):
    sites = Sites.objects.get(id=id)
    import pdb;pdb.set_trace();
    form = SiteAddForm(request.POST or None, instance=sites)
    if form.is_valid():
        form.save()
        return redirect("/site")
    else:
        return render(request, 'edit-site.html', {'sites':sites})

def delete_site(request, id):
    sites = Sites.objects.all()
    if Routers.objects.filter(select_site=id):
        message = "Sorry.. you have to delete its associated router first!"  
        return render(request,'ui-site.html',{'sites':sites, 'message':message})  
    else:
        sites = Sites.objects.get(id=id)
        sites.delete()
        return redirect("/site")


# router menu operations
def add_router(request):
    sites = Sites.objects.filter(site_status=True)
    return render(request,'add-router.html',{'sites':sites})

def submit_router(request):
    if request.method == "POST":
        form = RouterAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/router")
        else:
            msg = 'Failed to save!'

def edit_router(request, id):
    router = Routers.objects.get(id=id)
    site = Sites.objects.all()
    return render(request,'edit-router.html',{'router':router, 'site':site})

def update_router(request, id):
    router = Routers.objects.get(id=id)
    form = RouterAddForm(request.POST, instance = router)
    if form.is_valid():
        form.save()
        return redirect("/router")
    else:
        return render(request, 'edit-router.html', {'router':router})

def delete_router(request, id):
    router = Routers.objects.get(id=id)
    router.delete()
    return redirect("/router")


# router overview
def router_overview(request):
    customers = Customer.objects.all()
    sites = Sites.objects.all()
    routers = Routers.objects.all()
    return render(request,'router-overview.html',{'customers':customers, 'sites':sites, 'routers':routers})

cookies_overview = {
                'sysauth': '9d033c71407dae0cbb4bbedd7eae2a6d',
            }
            
headers_overview = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://185.162.153.122:10001/cgi-bin/luci/;stok=97f7379234f26f3769423bcb806a3c97/admin/status',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def get_router_uptime(seconds):
    # change seconds to days, minutes, hours
    time = float(seconds)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    uptime = str(round(day)) + "d " + str(round(hour)) + "h " + str(round(minutes)) + "m " + str(round(time)) + "s"
    current_date = datetime.now()

    router_uptime = round_seconds(current_date) - timedelta(days = day) - timedelta(hours = hour) - timedelta(minutes = minutes) - timedelta(seconds = time)
    return uptime + "(since " + str(router_uptime) + ")"


def round_seconds(date_time_object):
    new_date_time = date_time_object

    if new_date_time.microsecond >= 500000:
        new_date_time =new_date_time + timedelta(seconds=1)

    return new_date_time.replace(microsecond=0)


def get_router_overview(request):
    routers = Routers.objects.all()
    if request.method == "POST":
        form = RouterOverviewForm(request.POST)
        a1 = request.POST.get('router_name')
        router_data = Routers.objects.filter(id=a1).get()
        start_urls = router_data.access_url
        params = (
                ('status', '1'),
                ('_', '0.3864759206224684'),
            )
        data = {
            'username': router_data.access_id,
            'password': router_data.access_pwd,
        }
       
        response = requests.post('https://185.162.153.122:10001/cgi-bin/luci/;stok=b3ded6f2270597150af49718c290575f/admin/status/overview', headers=headers_overview, params=params, cookies=cookies_overview,data=data, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        json_response = json.loads(str(soup))
        local_time = str(json_response['localtime'])
        firmware_version = json_response['fwver']
        ram_memory_total = json_response['memtotal']
        ram_memory_free = json_response['memfree']
        ram_memory_usage = str(round((ram_memory_total - ram_memory_free)/ram_memory_total * 100)) + "%"
        router_uptime = get_router_uptime(json_response['uptime'])
        flash_space = float(json_response['flashspace'])
        flash_free = float(json_response['flashfree'])
        flash_memory_usage = str(round((flash_space - flash_free)/flash_space * 100)) + "%"
        curr_datetime = datetime.now(tz=timezone.utc)
        local_ip_add = socket.gethostbyname(socket.gethostname())
        curr_user_id = request.user
        router_name = router_data.router_name
        site_name = router_data.select_site.site_name
        t1 = router_data.select_site.id
        customer_name = Sites.objects.filter(id=t1).get().select_customer.cust_name

        # saving details in db
        router_overview_log = RouterOverviewLog.objects.create(user=curr_user_id, ip_add=local_ip_add,
                                                                curr_datetime=curr_datetime, firmware=firmware_version,
                                                                router_uptime=router_uptime, local_device_time=local_time,
                                                                memoryusage_RAM=ram_memory_usage, memoryusage_Flash=flash_memory_usage)
        return render(request,'router-details.html',{'customer_name':customer_name, 'site_name':site_name, 'router_name':router_name, 'local_time':local_time, 'router_uptime':router_uptime, 
                                                    'ram_memory_usage':ram_memory_usage, 'flash_memory_usage':flash_memory_usage,
                                                    'firmware_version':firmware_version, 'curr_datetime':curr_datetime,
                                                    'local_ip_add':local_ip_add})

        # response = requests.post('https://185.162.153.122:10001/cgi-bin/luci/;stok=b3ded6f2270597150af49718c290575f/admin/status/sysinfo', data=data, verify=False)
        # soup = BeautifulSoup(response.text, 'lxml')
        # firmware_ver = soup.findAll('td')[7].text

def router_reveal_password(request):
    routers = Routers.objects.all()
    return render(request,'router-reveal-password.html',{'routers':routers})

def get_password_details(request):
    routers = Routers.objects.all()
    if request.method == "POST":
        form = RevealPasswordForm(request.POST)
        router_id = request.POST.get('router_name')
        router_data = Routers.objects.filter(id=router_id).get()
        router_name = router_data.router_name
        access_id = router_data.access_id
        access_pwd = router_data.access_pwd
        return render(request, 'reveal-pwd.html',{'router_name':router_name, 'access_id':access_id, 'access_pwd':access_pwd})


def router_overview_logs(request):
    router_overview_logs = RouterOverviewLog.objects.all()
    return render(request,'router-overview-logs.html',{'router_overview_logs':router_overview_logs})