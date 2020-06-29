import http

from celery.result import AsyncResult
from django.core.cache import cache
from rest_framework import views, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Level, HotlineUser
from api.serializers import LevelSerializer, UserSerializer
from api.tasks import generate_level_preview
from hotline import celery_app
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
        result = generate_level_preview.delay(instance.id,
                                              instance.level_config)
        # saving task id to cache, so that it could be
        # retrieved in GetPreviewImage to return image
        # generation status
        cache.set(instance.id, result.id)


class GetPreviewImage(APIView):
    permission_classes = (IsAuthenticated,)
    view_name = 'get-preview-image'

    # TODO I don't like the idea with caching and whatnot
    # I think I should add the 'status' field to the Level model
    # because now this is too tightly coupled with the celery task
    def get(self, request: Request, level_id, *args, **kwargs):
        """
        Returns the level generation status and the preview image
        if the generation succeeded

        Responses:

        200 OK
        {
          'status': 'SUCCESS/PENDING/FAILED,
          'image': null or 'url'
        }

        404 Not Found
        410 Gone - Level generation failed, you will have to restart it

        """
        try:
            level = Level.objects.get(pk=level_id)
        except Level.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response = dict()
        if level.image.name:
            response['status'] = 'SUCCESS'
            response['image'] = request.build_absolute_uri(level.image.url)
        else:
            task_id = cache.get(level_id)

            if not task_id and not level.image.name:
                return Response(status=status.HTTP_410_GONE)

            task = AsyncResult(task_id, app=celery_app)
            response['status'] = task.state

            if task.state == 'SUCCESS':
                cache.delete(level_id)
                response['image'] = request.build_absolute_uri(level.image.url)

        return Response(data=response)
