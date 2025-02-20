import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


PRAISE_TEXTS = [
    "Отличная работа!", "Молодец!", "Ты лучший!",
    "Так держать!", "Прекрасный результат!"
]


def get_schoolkid(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print(f'Ученик "{name}" не найден.')
        return None
    except Schoolkid.MultipleObjectsReturned:
        print(
            f'Найдено несколько учеников с именем "{name}". Уточните запрос.'
        )
        return None


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    bad_marks.update(points=5)


def remove_chastisements(schoolkid):
    chastisements_to_delete = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements_to_delete.delete()


def create_commendation(student_name, subject_name):
    schoolkid = get_schoolkid(student_name)
    if not schoolkid:
        return

    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_name,
    ).order_by("-date")

    if not last_lesson:
        print(f'Ошибка: Урок по предмету "{subject_name}" для {student_name} не найден.')
        return

    Commendation.objects.create(
        schoolkid=schoolkid,
        teacher=last_lesson.teacher,
        text=random.choice(PRAISE_TEXTS),
        created=last_lesson.date,
        subject=last_lesson.subject,
    )
