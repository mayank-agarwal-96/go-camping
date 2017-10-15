# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from watson import search as watson


class CampConfig(AppConfig):
    name = 'camp'
    def ready(self):
        Camp = self.get_model("Camp")
        watson.register(Camp)