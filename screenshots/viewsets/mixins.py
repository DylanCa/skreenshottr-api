from typing import Any

from django.db.models import QuerySet
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from screenshots.viewsets.permissions import IsOwner


class BaseModelViewSetMixin(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]


class CheckParentPermissionMixin:
    parent_queryset: QuerySet
    parent_lookup_field: str
    parent_lookup_url_kwarg: str

    def __init__(self, **kwargs):
        self.parent_obj: Any = None
        super().__init__(**kwargs)

    def check_permissions(self, request):
        super().check_permissions(request)

        # check permissions for the parent object
        parent_lookup_url_kwarg = self.parent_lookup_url_kwarg or self.parent_lookup_field

        if parent_lookup_url_kwarg not in self.kwargs:
            return

        filter_kwargs = {
            self.parent_lookup_field: self.kwargs[parent_lookup_url_kwarg]
        }
        self.parent_obj = get_object_or_404(self.parent_queryset, **filter_kwargs)
        self.parent_obj._is_parent_obj = True
        super().check_object_permissions(request, self.parent_obj)
