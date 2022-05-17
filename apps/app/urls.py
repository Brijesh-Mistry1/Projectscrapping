
from django.urls import path, re_path
from apps.app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # ----- SETUP -----
    path(r'customer', views.display_customer, name='customer'),
    path(r'site', views.display_site, name='site'),
    path(r'router', views.display_router, name='router'),

    # customer
    path(r'addcustomer', views.save_customer, name='addcustomer'),
    path(r'edit_customer/<int:id>', views.edit_customer, name='edit_customer'),
    path(r'update_customer/<int:id>', views.update_customer, name='update_customer'),
    path(r'delete_customer/<int:id>', views.delete_customer, name='delete_customer'),

    # site
    path(r'addsite', views.add_site, name='addsite'),
    path(r'submitsite', views.submit_site, name='submitsite'),
    path(r'edit_site/<int:id>', views.edit_site, name='edit_site'),
    path(r'update_site/<int:id>', views.update_site, name='update_site'),
    path(r'delete_site/<int:id>', views.delete_site, name='delete_site'),

    # router
    path(r'addrouter', views.add_router, name='addrouter'),
    path(r'submitrouter', views.submit_router, name='submitrouter'),
    path(r'edit_router/<int:id>', views.edit_router, name='edit_router'),
    path(r'update_router/<int:id>', views.update_router, name='update_router'),
    path(r'delete_router/<int:id>', views.delete_router, name='delete_router'),



    # ------ Action ------
    # router overview
    path(r'router_overview', views.router_overview, name='router_overview'),
    path(r'get_router_overview', views.get_router_overview, name='get_router_overview'),

    # reveal Password
    path(r'router_reveal_password', views.router_reveal_password, name='router_reveal_password'),
    path(r'get_password_details', views.get_password_details, name='get_password_details'),


    # ------ Activity Logs ------
    path(r'router_overview_logs', views.router_overview_logs, name='router_overview_logs'),

    # Router activity logs
    re_path(r'^.*\.*', views.pages, name='pages'),
]
