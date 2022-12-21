from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'bid')
    list_filter = ("listing", 'user')

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid, BidAdmin)
