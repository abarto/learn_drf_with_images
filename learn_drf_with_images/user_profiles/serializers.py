from rest_framework.serializers import HyperlinkedModelSerializer

from .models import UserProfile

class UserProfileSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'date_of_birth', 'phone_number', 'gender')
        readonly_fields = ('url', 'image')
