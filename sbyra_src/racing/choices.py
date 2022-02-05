from django.db import models


class YachtClassChoices(models.TextChoices):
    # CONSTANT = DB_Value, User Display Value
    A = "A", "Class A"
    A1 = "A1", "Class A1"
    B = "B", "Class B"
    C = "C", "Class C"
