from django.db import models


class Card(models.Model):
    card_number = models.CharField(max_length=20, blank=True)
    card_holder = models.CharField(max_length=120, blank=True)
    pin = models.CharField(max_length=4, default="0000")
    is_locked = models.BooleanField(default=False)
    domestic_limit_enabled = models.BooleanField(default=True)
    international_limit_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.card_number or f"Card {self.pk}"


class CreditCardApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    full_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    income = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.full_name


class IssuedCard(models.Model):
    application = models.ForeignKey(
        CreditCardApplication, on_delete=models.CASCADE, related_name="issued_cards",
        null=True, blank=True
    )
    card_number = models.CharField(max_length=20, blank=True)
    card_holder = models.CharField(max_length=150, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_number or f"Issued card {self.pk}"
