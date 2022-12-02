from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition, can_proceed
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from garpix_company.helpers import COMPANY_STATUS_ENUM
from garpix_company.managers.company import CompanyActiveManager

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps as django_apps


User = get_user_model()


class AbstractCompany(models.Model):
    """
    Данные о компании.
    """

    COMPANY_STATUS = COMPANY_STATUS_ENUM

    title = models.CharField(max_length=255, verbose_name=_('Название'))
    full_title = models.CharField(max_length=255, verbose_name=_('Полное название'))
    inn = models.CharField(max_length=15, verbose_name=_('ИНН'))
    ogrn = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('ОГРН'))
    kpp = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("КПП"))
    bank_title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Наименование банка"))
    bic = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("БИК банка"))
    schet = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Номер счета"))
    korschet = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Кор. счет"))
    ur_address = models.CharField(max_length=300, verbose_name=_("Юридический адрес"))
    fact_address = models.CharField(max_length=300, verbose_name=_("Фактический адрес"))
    status = FSMField(default=COMPANY_STATUS.ACTIVE, choices=COMPANY_STATUS.CHOICES, verbose_name=_('Статус'))
    participants = models.ManyToManyField(User, through='garpix_company.UserCompany',
                                          verbose_name=_('Участники компании'))
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='owned_companies',
                              verbose_name=_('Владелец'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата изменения'))
    objects = models.Manager()
    active_objects = CompanyActiveManager()

    @classmethod
    def action_permissions(cls):
        from garpix_company.permissions import CompanyAdminOnly, CompanyOwnerOnly
        return {'create': [IsAuthenticated],
                'retrieve': [AllowAny],
                'list': [AllowAny],
                'update': [IsAdminUser | CompanyAdminOnly],
                'partial_update': [IsAdminUser | CompanyAdminOnly],
                'destroy': [IsAdminUser | CompanyAdminOnly],
                'change_owner': [IsAdminUser | CompanyOwnerOnly]}

    class Meta:
        verbose_name = _('Компания')
        verbose_name_plural = _('Компании')
        ordering = ['-id']
        abstract = True

    @transition(field=status, source=COMPANY_STATUS.BANNED, target=COMPANY_STATUS.ACTIVE)
    def comp_active(self):
        pass

    @transition(field=status, source=COMPANY_STATUS.ACTIVE, target=COMPANY_STATUS.BANNED)
    def comp_banned(self):
        pass

    @transition(field=status, source=[COMPANY_STATUS.ACTIVE, COMPANY_STATUS.BANNED], target=COMPANY_STATUS.DELETED)
    def comp_deleted(self):
        pass

    @property
    def can_banned(self):
        return can_proceed(self.comp_banned)

    @property
    def can_deleted(self):
        return can_proceed(self.comp_deleted)

    @property
    def can_active(self):
        return can_proceed(self.comp_active)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.comp_deleted()
        self.save()

    def hard_delete(self):
        super().delete()

    def change_owner(self, new_owner_id, current_owner):
        from .user_company import UserCompany
        if self.owner != current_owner:
            return False, _('Действие доступно только для владельца компании')
        if self.owner.id == new_owner_id:
            return False, _('Пользователь с указанным id уже является владельцем компании')
        try:
            user_company = UserCompany.objects.get(company=self, user_id=int(new_owner_id))
            self.owner = user_company.user
            self.save()
            return True, None
        except UserCompany.DoesNotExist:
            return False, _('Пользователь с указанным id не является сотрудником компании')

    @classmethod
    def invite_confirmation_link(cls, token):
        return f'{settings.SITE_URL}invite/{token}'


def get_company_model():
    """
    Return the Company model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.GARPIX_COMPANY_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("GARPIX_COMPANY_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "GARPIX_COMPANY_MODEL refers to model '%s' that has not been installed" % settings.GARPIX_COMPANY_MODEL
        )
