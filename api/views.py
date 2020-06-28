import http

from rest_framework import views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.models import Level, HotlineUser
from api.serializers import LevelSerializer, UserSerializer
from api.tasks import generate_level_preview
from hotline.utils import extra_permissions


class EmailVerifiedView(views.APIView):
    renderer_classes = (JSONRenderer,)
    view_name = 'email-verified'

    def get(self, request, *args, **kwargs):
        return Response(status=http.HTTPStatus.OK, data={
            "status": "verified"
        })


class GetUserDetailView(generics.RetrieveAPIView):
    view_name = 'get-user-detail'
    lookup_field = 'pk'
    serializer_class = UserSerializer
    queryset = HotlineUser.objects.all()


class GetLevelsView(generics.ListCreateAPIView):
    view_name = 'get-all-levels'
    queryset = Level.objects.filter(is_public=True)
    serializer_class = LevelSerializer

    def get(self, request, *args, **kwargs):
        """
        Returns all publicly available levels

        Response:

        200 OK
        """
        return super().get(request, *args, **kwargs)

    @extra_permissions(IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        # running the image preview generator
        generate_level_preview.delay(instance.id,
                                     instance.level_config)
