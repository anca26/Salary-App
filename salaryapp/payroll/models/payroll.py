from django.db import models

class PayrollRun(models.Model):
    
    manager = models.ForeignKey("Employee", on_delete=models.PROTECT, related_name="payroll_runs")
    period = models.DateField(help_text="1st of the month", db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [("manager", "period")]
        indexes = [
            models.Index(fields=["period","manager"]),
        ]
        
    def __str__(self):
        return f"PayrollRun for {self.manager} - {self.period.strftime('%Y-%m')}"
    
    
class PayrollLine(models.Model):
    run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name="lines")
    employee = models.ForeignKey("Employee", on_delete=models.PROTECT, related_name="payroll_lines")

    # canonical period mirror (helps with queries and uniqueness)
    period = models.DateField(help_text="1st of month", db_index=True)

    working_days = models.PositiveSmallIntegerField()
    vacation_days = models.PositiveSmallIntegerField(default=0)
    bonus_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    salary_to_pay = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("run", "employee")]
        indexes = [
            models.Index(fields=["period", "employee"]),
            models.Index(fields=["run"]),
        ]

    def __str__(self):
        return f"PayrollLine(run={self.run_id}, emp={self.employee_id}, {self.period})"