from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.text import slugify


AMOUNT_VALIDATORS = [MaxValueValidator(10000000), MinValueValidator(1000)]

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

class Transaction(TimeStampMixin):
    """Model to represent Transaction."""

    ref = models.CharField(max_length=50, null=True, blank=True)
    amount = models.PositiveIntegerField(validators=AMOUNT_VALIDATORS)
    verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def verify(self):
        self.verified = True
        self.save()

    def get_amount_in_units(self):
        return self.amount / 100


    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.ref)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.ref)
    

class BankAccount(TimeStampMixin):
    """Model to represent Bank Account."""

    account_number = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    bank_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.account_number}"

