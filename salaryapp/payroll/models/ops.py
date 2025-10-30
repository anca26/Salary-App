from django.db import models

class IdempotencyKey(models.Model):
    endpoint = models.CharField(max_length=64)    
    key = models.CharField(max_length=128)      
    requester = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL, related_name="idempotency_keys")
    period = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    consumed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, default="CREATED") 

    class Meta:
        unique_together = [("endpoint", "key")]
        indexes = [models.Index(fields=["endpoint", "key"])]
