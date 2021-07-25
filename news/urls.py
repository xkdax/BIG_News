from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    # path('', HomeView.as_view()),
    # path('news/create/', CreateView.as_view()),
    # path('news/<slug:article_id>/', ArticleView.as_view()),
    # re_path("news/(?P<link>[^/]*)/?/", news.views.PageView.as_view()),
    # НАХУЯ ТУТ ЭТО ВСЁ БЫЛО??????

]
