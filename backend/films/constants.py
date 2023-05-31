class ContentRating:
    ZERO = 0
    SIX = 6
    TWELVE = 12
    SIXTEEN = 16
    EIGHTEEN = 18


CONTENT_RATING_CHOICES = (
    (ContentRating.ZERO, 0),
    (ContentRating.SIX, 6),
    (ContentRating.TWELVE, 12),
    (ContentRating.SIXTEEN, 16),
    (ContentRating.EIGHTEEN, 18),
)


DEFAULT_GENRES = [
    "Аниме",
    "Биографические",
    "Боевики",
    "Вестерн",
    "Детективы",
    "Детские",
    "Документальные",
    "Драма",
    "Исторические",
    "Комедии",
    "Короткометражные",
    "Криминал",
    "Мелодрама",
    "Мистика",
    "Музыка",
    "Мультфильмы",
    "Мюзикл",
    "Научный",
    "Нуар",
    "Приключения",
    "Психология",
    "Романтика",
    "Семейный",
    "Спорт",
    "Триллер",
    "Фантастика",
    "Фэнтези",
    "Эротика",
    "Зомби",
    "Ужасы",
    "Шпионы"
]

DEFAULT_CATEGORIES = [
    "Фильмы","Сериалы","Мультфильмы"
]

class FilmType:
    FILM = "film"
    SERIAL = "serial"


FILM_TYPE_CHOICES = (
    (FilmType.FILM, "Film"),
    (FilmType.SERIAL, "Serial")
)