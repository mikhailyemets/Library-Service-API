from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "book",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "book",
                    "expected_return_date",
                ),
                "description": (
                    "By creating instance from admin panel "
                    "book inventory not decreased."
                )
            }
        ),
        (
            "Return book",
            {
                "fields": ("actual_return_date",),
                "description": (
                    "By setting actual return date from admin panel "
                    "book inventory not increased."
                )
            }
        )
    )

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {
            "expected_return_date": (
                "Minimum expected return date: tomorrow."
            ),
            "actual_return_date": (
                "Setting this field mean that borrowed book returned."
            ),
        }
        kwargs.update({"help_texts": help_texts})
        return super().get_form(request, obj, **kwargs)
