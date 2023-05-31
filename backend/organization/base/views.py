from rest_framework import viewsets, generics, mixins


class AppGenericAPIView(generics.GenericAPIView):
    """Add filter by organization into queryset."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(queryset.model, "org", None):
            queryset = queryset.filter(**{"org": self.request.org})
        return queryset


class AppGenericViewSet(viewsets.ViewSetMixin, AppGenericAPIView):
    pass


class AppModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    AppGenericViewSet,
):
    pass
