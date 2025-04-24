from django.contrib import admin
from .models import TbResults, TbCard, TbTransact, TbUsed
# Register your models here.
admin.site.register(TbResults)
admin.site.register(TbCard)
admin.site.register(TbTransact)
admin.site.register(TbUsed)
