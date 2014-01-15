from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question', 'pub_date', 'was_published_recently']
    list_filter = ['pub_date']
    search_fields = ['question']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'poll', 'votes']
    list_filter = ['poll']
    search_fields = ['choice_text']

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)

