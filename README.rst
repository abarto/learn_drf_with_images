learn_drf_with_images
=====================

Introduction
------------

This project was created to provide a complete example that illustrates how to implement image uploads and models with image fields with `Django REST Framework <http://www.django-rest-framework.org/>`_.

The model
---------

There's only one class that represents the typical "User Profile" use case on a `Django <https://www.djangoproject.com/>`_ site:

::

    def upload_to(instance, filename):
        return 'user_profile_image/{}/{}'.format(instance.user_id, filename)


    class UserProfile(models.Model):
        GENDER_UNKNOWN = 'U'
        GENDER_MALE = 'M'
        GENDER_FEMALE = 'F'
        GENDER_CHOICES = (
            (GENDER_UNKNOWN, _('unknown')),
            (GENDER_MALE, _('male')),
            (GENDER_FEMALE, _('female')),
        )

        user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
        date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
        phone_number = PhoneNumberField(_('phone number'), blank=True)
        gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
        image = models.ImageField(_('image'), blank=True, null=True, upload_to=upload_to)

With the exception of the ``phone_number`` field (which uses `django-phonenumber-field <https://github.com/stefanfoulis/django-phonenumber-field>`_), the rest of the fields are regular Django fields, including the ``image`` which is the subject of this project and represents an image for the associated user.

The API
-------

As with all Django REST Framework APIs, we need to define serializers, views (or viewsets) and hook the views in the site's URLs. Let's start with the serializers:

::

    class UserProfileSerializer(HyperlinkedModelSerializer):
        class Meta:
            model = UserProfile
            fields = ('url', 'date_of_birth', 'phone_number', 'gender', 'image')
            readonly_fields = ('url', 'image')

It couldn't be simpler. ``UserProfileSerializer`` it's just a ``HyperlinkedModelSerializer`` that handles the ``UserProfile`` model. Given that it is not possible to handle uploads using the default JSON parser, we marked the image field as read-only.

The views are a little more interesting:

::

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

We have a ``GenericViewSet`` combined with ``RetrieveModelMixin`` and ``UpdateModelMixin`` to provide retrieve and update funcionality for our ``UserProfile`` model (It doesn't make sense to provide list or destroy in this context). The interesting part is the ``image`` method, which is exposed as a view using ``@detail_route`` decorator.

The trick here is that the method is also decorated using ``@parser_classes`` where we declare that the requests should be parsed using ``FormParser`` or ``MultiPartParser``, and this is what is going to allow us to handle the uploaded files.

When the method is invoked, we check that the request data contains an ``upload`` entry, and if it does we delete the image associated with the user profile, replace it with the ``UploadedFile`` contents and return a ``Response`` with status code 201 (Created). If ``upload`` is not in the request data, we return a fail response with status 400 (Bad Request).

The last part is to set up the URLs for our API:

::

    router = DefaultRouter()
    router.register(r'user_profiles', UserProfileViewSet)

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include(router.urls)),
        url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]

We used a Django REST Framework ``Router`` which wires everything automatically and thus save us a lot of work. Notice that we're also using `Django OAuth Toolkit <https://github.com/evonove/django-oauth-toolkit>`_ to provide authentication for our API.

Usage
-----

The following session illustrates the typical usage of our API.

::

    $ curl --header "Content-Type: application/x-www-form-urlencoded" --header "Accept: application/json; indent=4" --request POST --data "username=admin&password=admin&client_id=zmfZyf7EAGJJ6imph3qtwGtoH8eqt1VdVmRZh7NC&grant_type=password" http://localhost:8000/o/token/; echo
    {"access_token": "PkwvCYq0cRYfvpJeXvc4czFKvohwea", "expires_in": 36000, "token_type": "Bearer", "scope": "write read", "refresh_token": "jl3Y5Mo7fLaHvJDWCQv5I9g4zbLHkT"}

    $ curl --header "Authorization: Bearer PkwvCYq0cRYfvpJeXvc4czFKvohwea" --header "Accept: application/json; indent=4" --request GET http://localhost:8000/user_profiles/1/; echo
    {
        "url": "http://localhost:8000/user_profiles/1/",
        "date_of_birth": "2015-07-07",
        "phone_number": "+41524204242",
        "gender": "M",
        "image": "http://localhost:8000/media/user_profile_image/1/admin.png"
    }

    $ curl --verbose --header "Authorization: Bearer PkwvCYq0cRYfvpJeXvc4czFKvohwea" --header "Accept: application/json; indent=4" --request POST --form upload=@admin2.jpg http://localhost:8000/user_profiles/1/image/; echo
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 8000 (#0)
    * Initializing NSS with certpath: sql:/etc/pki/nssdb
    > POST /user_profiles/1/image/ HTTP/1.1
    > User-Agent: curl/7.40.0
    > Host: localhost:8000
    > Authorization: Bearer PkwvCYq0cRYfvpJeXvc4czFKvohwea
    > Accept: application/json; indent=4
    > Content-Length: 3737
    > Expect: 100-continue
    > Content-Type: multipart/form-data; boundary=------------------------f915e8f2eaef4479
    >
    * Done waiting for 100-continue
    * HTTP 1.0, assume close after body
    < HTTP/1.0 201 CREATED
    < Date: Tue, 07 Jul 2015 01:34:01 GMT
    < Server: WSGIServer/0.2 CPython/3.4.2
    < Vary: Accept
    < Location: http://localhost:8000/media/user_profile_image/1/admin2.jpg
    < X-Frame-Options: SAMEORIGIN
    < Allow: POST, OPTIONS
    <
    * Closing connection 0

    $ curl --header "Authorization: Bearer PkwvCYq0cRYfvpJeXvc4czFKvohwea" --header "Accept: application/json; indent=4" --request GET http://localhost:8000/user_profiles/1/; echo
    {
        "url": "http://localhost:8000/user_profiles/1/",
        "date_of_birth": "2015-07-07",
        "phone_number": "+41524204242",
        "gender": "M",
        "image": "http://localhost:8000/media/user_profile_image/1/admin2.jpg"
    }

A `Vagrant <https://www.vagrantup.com/>`_ configuration file is included if you want to test the service yourself.

Feedback
--------

As usual, I welcome comments, suggestions and pull requests.
