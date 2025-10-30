from django.db import models

def archive_upload_path(instance, filename: str) -> str:
    # archives/<year>/<month>/[manager_<id>|employee_<id>]/<filename>
    owner = f"manager_{instance.manager_id}" if instance.manager_id else f"employee_{instance.employee_id}" if instance.employee_id else "system"
    return f"archives/{instance.year}/{instance.month}/{owner}/{filename}"

class FileRecord(models.Model):
    class Category(models.TextChoices):
        MANAGER_CSV = "MANAGER_CSV", "Manager CSV"
        EMPLOYEE_PDF = "EMPLOYEE_PDF", "Employee PDF"

    category = models.CharField(max_length=20, choices=Category.choices)
    file = models.FileField(upload_to=archive_upload_path)

    manager = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL, related_name="csv_files")
    employee = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL, related_name="pdf_files")

    period = models.DateField(help_text="First day of month", db_index=True)

    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()

    run = models.ForeignKey("PayrollRun", null=True, blank=True, on_delete=models.SET_NULL, related_name="files")

    checksum_sha256 = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["category", "year", "month"])]
