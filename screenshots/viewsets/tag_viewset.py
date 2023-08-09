from screenshots.models import Tag, Screenshot
from screenshots.serializers import TagSerializer
from .mixins import BaseModelViewSetMixin, CheckParentPermissionMixin


class TagViewSet(CheckParentPermissionMixin,
                 BaseModelViewSetMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    parent_queryset = Screenshot.objects.all()
    parent_lookup_field = 'pk'
    parent_lookup_url_kwarg = 'screenshot_pk'

    lookup_field = 'pk'

    def get_queryset(self):
        filters = {"owner": self.request.user}
        parent = self.get_parent()

        if parent:
            filters['screenshot'] = parent.id

        return Tag.objects.filter(**filters).order_by('id')

    def get_parent(self):
        if "screenshot_pk" in self.kwargs:
            return Screenshot.objects.get(pk=self.kwargs["screenshot_pk"])
        else:
            return None

    def perform_create(self, serializer):
        instance = serializer.save()
        parent = self.get_parent()

        if parent:
            parent.tags.add(instance)

        return instance

    def perform_destroy(self, instance):
        parent = self.get_parent()

        if parent:
            parent.tags.remove(instance)
        else:
            instance.delete()
