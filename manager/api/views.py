from rest_framework import generics

from .serializers import InstanceSerializer, HostSerializerGet
from manager.models import Instance, Host

# class MultipleFieldLookupMixin(object):
#     def get_object(self):
#         queryset = self.get_queryset()  # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             print('------{}----'.format(field))
#             print('------{}----'.format(self.kwargs[field]))
#             if self.kwargs[field]:  # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         obj = generics.get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj


class InstanceAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'name'
    serializer_class = InstanceSerializer

    def get_queryset(self):
        return Instance.objects.all()

    # def get_queryset(self):
    #     qs = Instance.objects.all()
    #     query = self.request.GET.get("search")
    #     if query is not None:
    #         qs = qs.filter(Q(name__icontains=query))
    #     return  qs

class HostAPIView(generics.RetrieveAPIView): #, MultipleFieldLookupMixin):
    queryset = Host.objects.all()
    lookup_field = 'name'
    serializer_class = HostSerializerGet

    def get_queryset(self):
        return Host.objects.all()

