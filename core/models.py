from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=64, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        unique_together = ("name",)
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class Assignee(models.Model):
    user = models.OneToOneField(User, related_name="profile", verbose_name="Пользователь")
    organization = models.ManyToManyField(Organization, related_name="assignees", verbose_name="Организация",
                                          blank=True)
    organiz_login = models.ForeignKey(Organization, related_name="login_assignees", blank=True, null=True,
                                      verbose_name="Авторизировался в")

    class Meta:
        unique_together = ("user",)
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.user.email


class Task(models.Model):
    STATUS_CHOICES = ((1, "Не начато"),
                      (2, "Принято на выполнение"),
                      (3, "Выполняется"),
                      (4, "Закончено"),
                      (5, "Удалено"))

    PRIORITY_CHOICES = ((1, "Низкий"),
                        (2, "Средний"),
                        (3, "Высокий"),
                        (4, "Безотлагательный"))

    name = models.CharField(max_length=64, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    assignee = models.ForeignKey(Assignee, verbose_name="Исполнитель")
    organization = models.ForeignKey(Organization, verbose_name="Организация")
    deadline = models.DateTimeField(verbose_name="Дедлайн", blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, verbose_name="Статус")
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, verbose_name="Приоритет")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.name
