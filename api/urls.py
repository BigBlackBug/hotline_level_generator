from django.conf.urls import url

from api.views import EmailVerifiedView, GetLevelsView, GetUserDetailView, GetPreviewImage

urlpatterns = [
    url(r'^email-verified/', EmailVerifiedView.as_view(),
        name=EmailVerifiedView.view_name),
    url(r'^levels/(?P<level_id>[0-9]+)/preview_image/', GetPreviewImage.as_view(),
        name=GetPreviewImage.view_name),
    url(r'^levels/', GetLevelsView.as_view(), name=GetLevelsView.view_name),
    url(r'^users/(?P<pk>[0-9]+)/$', GetUserDetailView.as_view(),
        name=GetUserDetailView.view_name)
]
