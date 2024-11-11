from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):

    full_name = models.CharField(max_length=255, db_column="FULL_NAME")
    username = models.CharField(max_length=255, unique=True, db_column="USERNAME")
    address = models.CharField(max_length=255, db_column="ADDRESS")
    phone = models.CharField(max_length=10, db_column="PHONE")
    email = models.EmailField(max_length=255, unique=True, db_column="EMAIL")
    password = models.CharField(max_length=255, db_column="PASSWORD")
    date_of_birth = models.DateField(db_column="DOB")

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "USER"
