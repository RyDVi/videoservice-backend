from django.urls import path, include
from rest_framework_nested import routers

from users.views import CustomersViewSet

def get_leads_router(base_router):
    leads_router = routers.NestedDefaultRouter(
        base_router, r"leads", lookup="leads"
    )
    leads_router.register(r"customer", CustomersViewSet)
    return leads_router

def leads_url_patterns(base_router, lpath):
    return [
        path(lpath, include(get_leads_router(base_router).urls)),
    ]