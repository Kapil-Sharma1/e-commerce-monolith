from uuid import uuid4
from django.db import models


class NCAbstractBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True
