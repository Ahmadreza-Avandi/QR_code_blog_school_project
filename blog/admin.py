# blog/admin.py

from django.contrib import admin
from .models import Post

# ثبت مدل Post در پنل مدیریت
admin.site.register(Post)
