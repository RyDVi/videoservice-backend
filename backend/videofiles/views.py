from backend.filters import UUIDInFilter
from backend.views import RelatedViewSetsMixin
from organization.base.views import AppModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework import parsers, response
from rest_framework.decorators import action, parser_classes
from django_filters.rest_framework import FilterSet
from videofiles.filters import VideoFilters

from videofiles.models import SubtitleFile, Video, VideoFile
from videofiles.serializers import SubtitleFileSerializer, VideoSerializer, VideoFileSerializer


class VideoViewSet(RelatedViewSetsMixin, AppModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filterset_class = VideoFilters
    


class VideoFileFilter(FilterSet):
    video = UUIDInFilter()

class VideoFileViewSet(RelatedViewSetsMixin, AppModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer
    filterset_class = VideoFileFilter
    filterset_fields = ['video']


    # TODO: permissions
    @action(methods=['PUT'], detail=True)
    @parser_classes([parsers.MultiPartParser, parsers.FileUploadParser])
    def upload_video(self, request, pk):
        # TODO: check of mimetype of video
        video = self.get_object()
        file_obj = request.FILES['file']
        s = self.get_serializer(
            instance=video, data={"video": video.video_id, "sound_studio": video.sound_studio, "file": file_obj}, context={"request": request})
        s.is_valid(raise_exception=True)
        s.save()
        return response.Response(s.data, status=200)


class SubtitleFileViewSet(RelatedViewSetsMixin, AppModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = SubtitleFile.objects.all()
    serializer_class = SubtitleFileSerializer

    # TODO: permissions
    @action(methods=['PUT'], detail=True)
    @parser_classes([parsers.MultiPartParser, parsers.FileUploadParser])
    def upload_subtitle(self, request, pk):
        # TODO: check of mimetype of subtitles
        subtitle = self.get_object()
        file_obj = request.FILES['file']
        s = self.get_serializer(
            instance=subtitle, data={"video": subtitle.video_id, "studio_name": subtitle.studio_name, "file": file_obj}, context={"request": request})
        s.is_valid(raise_exception=True)
        s.save()
        return response.Response(s.data, status=200)
