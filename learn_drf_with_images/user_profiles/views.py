from rest_framework.decorators import detail_route, parser_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .models import UserProfile
from .permissions import IsAdminOrIsSelf
from .serializers import UserProfileSerializer


class UserProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminOrIsSelf,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @detail_route(methods=['POST'], permission_classes=[IsAdminOrIsSelf])
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        if 'upload' in request.data:
            user_profile = self.get_object()

            user_profile.image.delete()

            upload = request.data['upload']

            user_profile.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': user_profile.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class UserProfileMultiPartParserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminOrIsSelf,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @parser_classes((MultiPartParser,))
    def update(self, request, *args, **kwargs):
        if 'upload' in request.data:
            user_profile = self.get_object()

            user_profile.image.delete()

            upload = request.data['upload']

            user_profile.image.save(upload.name, upload)

        return super(UserProfileMultiPartParserViewSet, self).update(request, *args, **kwargs)
