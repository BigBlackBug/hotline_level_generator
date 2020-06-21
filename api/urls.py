from django.conf.urls import url

from api.views import EmailVerifiedView

urlpatterns = [
    # url(r'^do/', DoStuffView.as_view(), name=DoStuffView.view_name),
    url(r'^email-verified/', EmailVerifiedView.as_view(),
        name=EmailVerifiedView.view_name),
]
