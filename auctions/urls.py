from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path('listing/<int:pk>', views.detailListing, name='detail'),
    path('remove/<int:pk>', views.removeWatch, name='remove'),
    path('add/<int:pk>', views.addWatch, name='add'),
    path('watchlist', views.watchList, name="watchlist"),
    path('add_comment/<int:pk>', views.addComment, name="addComment"),
]
