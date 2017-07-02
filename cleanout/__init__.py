from django.apps import AppConfig


import os

default_app_config = 'cleanout.CleanOutConfig'

VERBOSE_APP_NAME = "清洗管理"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class CleanOutConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME
