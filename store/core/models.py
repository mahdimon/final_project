from django.db import models
from django.utils.timezone import now
from safedelete.models import SafeDeleteModel , HARD_DELETE


class BaseModel(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At') 
    class Meta:
        abstract = True




