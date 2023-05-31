from django.db import models
from films.models import Film

from organization.base.models import AppOrgModel
from videofiles.constants import RESOLUTION_TYPE_CHOICES, ResolutionType
from django.utils.translation import gettext_lazy as _
from django.utils.text import get_valid_filename
from django.conf import settings


class Video(AppOrgModel):
    """
    От класса Film отличается тем, что содержит файлы, а не информацию о фильме.
    Сериал включает сезон и серию.
    Фильм всегда включает только серию 1 и разные сезоны (части фильма).
    """
    film = models.ForeignKey(
        Film, related_name="video", verbose_name=_("film info"), on_delete=models.RESTRICT)
    season = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("season of film"))
    series = models.PositiveIntegerField(
        default=1, verbose_name=_("film series"))

    class Meta:
        db_table = "video"
        constraints = [models.UniqueConstraint(
            fields=["film", "season", "series"], name="unique series by season"
        )]


def videofile_path(instance, filename):
    film_name = get_valid_filename(instance.video.film.original_name)
    season = instance.video.season
    seria = instance.video.series
    resolution = instance.resolution
    sound_studio = get_valid_filename(instance.sound_studio)
    return 'video/{film_name}/season_{season}/seria_{seria}/{resolution}_{sound_studio}_{film_name}'.format(film_name=film_name, season=season, seria=seria, resolution=resolution, sound_studio=sound_studio)


class VideoFile(AppOrgModel):
    video = models.ForeignKey(
        Video, related_name="videofiles", on_delete=models.CASCADE, verbose_name=_("video of file"))
    resolution = models.CharField(
        choices=RESOLUTION_TYPE_CHOICES, default=ResolutionType.SD, verbose_name=_("video resolution"), max_length=4)
    file = models.FileField(upload_to=videofile_path, null=True,
                            storage=settings.CDN_STORAGE, max_length=512)
    sound_studio = models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = "videofiles"
        constraints = [models.UniqueConstraint(
            fields=["video", "resolution", "sound_studio"], name="unique resolution of file for video")]


class SubtitleFile(AppOrgModel):
    video = models.ForeignKey(
        Video, related_name="subtitlefiles", on_delete=models.CASCADE, verbose_name=_("subtitle of file"))
    file = models.FileField(upload_to="subtitle", null=True)
    studio_name = models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = "subtitlefiles"
        constraints = [models.UniqueConstraint(
            fields=["video", "studio_name"], name="unique subtitle file for studio")]
