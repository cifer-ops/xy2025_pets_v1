from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path("index", index, name="index"),
    path("pets", pets, name="pets"),
    path("detail", detail, name="detail"),
    path("my_colloect", my_colloect, name="my_colloect"),
    path("delete_collect", delete_collect, name="delete_collect"),
    path("add_collect", add_collect, name="add_collect"),

    path("my_adoption", my_adoption, name="my_zan"),
    path("delete_adoption", delete_adoption, name="delete_zan"),
    path("add_adoption", add_adoption, name="add_zan"),

    re_path(r"^my_info$", my_info, name="my_info"),

    path("", index, name="index"),
]
