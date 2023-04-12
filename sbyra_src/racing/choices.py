from django.db import models


class YachtClassChoice(models.TextChoices):
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


class SpinnakerClassChoice(models.TextChoices):
    """Spinnaker class choices to establish additional time corrections"""

    # CONSTANT = DB_Value, User Display Value
    S1 = "S1", "Spinnaker class 1"
    S2 = "S2", "Spinnaker class 2"
    S3 = "S3", "Spinnaker class 3"
    S4 = "S4", "Spinnaker class 4"
    S5 = "S5", "Spinnaker class 5"
