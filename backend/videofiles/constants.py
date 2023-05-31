class ResolutionType:
    SD = 480
    HD = 720
    FHD = 1080  # Full HD
    UHD = 2160  # Ultra HD


RESOLUTION_TYPE_CHOICES = (
    (ResolutionType.SD, "480"),
    (ResolutionType.HD, "720"),
    (ResolutionType.FHD, "1080"),
    (ResolutionType.UHD, "2160"),
)

VIDEO_PATH_BY_RESOLUTION = (
    (ResolutionType.SD, "video/480"),
    (ResolutionType.HD, "video/720"),
    (ResolutionType.FHD, "video/1080"),
    (ResolutionType.UHD, "video/2160"),
)
