# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    seat = models.ForeignKey('Seats', models.DO_NOTHING, blank=True, null=True)
    reservation_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    checked_in = models.IntegerField(blank=True, null=True)
    check_in_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservations'


class Seats(models.Model):
    objects = models.Manager
    seat_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    seat_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seats'


class UsersManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)
    def create_user(self, username, email, password=None, **extra_fields):
        pass

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        创建并返回一个超级用户（superuser）
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # 创建超级用户
        return self.create_user(username, email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin,models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = "user_id"
    password = models.CharField(max_length=128)
    last_login=models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'users'
    objects=UsersManager()
    def __str__(self):
        return self.username
class a(models.Model):
    id=models.AutoField(primary_key=True)