from organization.base.serializers import AppOrgModelSerializer
from videofiles.models import Video, VideoFile, SubtitleFile


class VideoSerializer(AppOrgModelSerializer):

    class Meta(AppOrgModelSerializer.Meta):
        model = Video
        fields = AppOrgModelSerializer.Meta.fields + ('film', "series", "season")


class VideoFileSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = VideoFile
        fields = AppOrgModelSerializer.Meta.fields + \
            ('video', 'resolution', 'file', "sound_studio",)
        kwargs = {'file': {'required': False}}

    def save(self, **kwargs):
        if getattr(self.instance, 'file', None) and hasattr(self.instance.file, 'url') and self.validated_data.get('file') is None:
            self.instance.file.delete()
        return super().save(**kwargs)


class SubtitleFileSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = SubtitleFile
        read_only_fields = AppOrgModelSerializer.Meta.read_only_fields
        fields = read_only_fields + ('video', 'file', 'studio_name')
        kwargs = {'file': {'required': False}}
