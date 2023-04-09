from django.db import models


class YachtClassChoices(models.TextChoices):
    """Yacht table classifications"""

    # CONSTANT = "DB_Value", "User Display Value"
    A = "A", "Class A"
    A1 = "A1", "Class A1"
    B = "B", "Class B"
    C = "C", "Class C"
    J = "J", "Class J24"


class CompletionStatusChoice(models.TextChoices):
    """Completion status choices for the Event class"""

    # CONSTANT = DB_Value, User Display Value
    CMP = "CMP", "Completed"
    DNC = "DNC", "Did Not Complete"
    DSQ = "DSQ", "Disqualified"
