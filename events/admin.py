from django.contrib import admin

from events.models import Events, Category


# Register your models here.
@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'meeting_time', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
