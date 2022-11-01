from rest_framework import generics


class UpdateAPIView(generics.UpdateAPIView):
    """ Base UpdateAPIView with following additions:
        - POST request method was added
    """

    http_method_names = ['post', 'patch', ]

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        # log_serializer_change(self.request, self.get_object(), serializer=serializer)
        serializer.save()


class DestroyAPIView(generics.DestroyAPIView):
    """ Base DestroyAPIView with following additions:
        - POST request method added;
        - does not perform actual database deletion, only marks object as deleted
    """
    http_method_names = ['post', 'delete', ]

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
