import django_filters

from .models import TeacherProfile, StudentProfile


class TeacherProfileFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="iexact")
    firstname = django_filters.CharFilter(field_name="user__first_name", lookup_expr="iexact")
    lastname = django_filters.CharFilter(field_name="user__last_name", lookup_expr="iexact")

    class Meta:
        model = TeacherProfile
        fields = {
            "date_of_birth": ["exact", "year", "year__gt", "year__lt", "month", "month__gt", "month__lt", ],
            "years_of_experience": ["exact", "gte", "lte"],
        }


class StudentProfileFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="iexact")
    firstname = django_filters.CharFilter(field_name="user__first_name", lookup_expr="iexact")
    lastname = django_filters.CharFilter(field_name="user__last_name", lookup_expr="iexact")

    class Meta:
        model = StudentProfile
        fields = {
            "date_of_birth": ["exact", "year", "year__gt", "year__lt", "month", "month__gt", "month__lt", ],
        }
