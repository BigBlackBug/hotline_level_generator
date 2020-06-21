import http

# Create your views here.
from rest_framework import views
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class EmailVerifiedView(views.APIView):
    renderer_classes = (JSONRenderer,)
    view_name = 'email-verified'

    def get(self, request, *args, **kwargs):
        return Response(status=http.HTTPStatus.OK, data={
            "status": "verified"
        })
