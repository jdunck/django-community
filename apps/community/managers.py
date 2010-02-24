from django.db import models

class ActiveManager(models.Manager):
    def get_query_set(self):
        qs = super(ActiveManager, self).get_query_set()
        qs.filter(active=True)
        return qs
