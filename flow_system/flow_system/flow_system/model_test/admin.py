from django.contrib import admin
from .models import TlsRes
from .models import FlowRes
from .models import ImageRes
from .models import HeartbeatRes

admin.site.register(TlsRes)
admin.site.register(FlowRes)
admin.site.register(ImageRes)
admin.site.register(HeartbeatRes)
# Register your models here.
