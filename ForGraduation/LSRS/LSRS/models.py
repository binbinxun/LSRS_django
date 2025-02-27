# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime
from django.utils import timezone
from django.db.models.signals import pre_save
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver


class Seats(models.Model):
    objects = models.Manager()
    seat_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    seat_type = models.CharField(max_length=50, blank=True, null=True)

    def is_available_between(self, start_time, end_time):
        """
        检查该座位在指定时间段是否可用
        """
        return not self.reservation_set.filter(
            models.Q(status__in=['reserved', 'in_use']) &
            models.Q(start_time__lt=end_time) &
            models.Q(end_time__gt=start_time)
        ).exists()
    class Meta:
        managed = True
        db_table = 'seats'


class UsersManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_active', True)
        user.save(using=self._db)
        return user
#
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
    USERNAME_FIELD = "username"
    password = models.CharField(max_length=128)
    last_login=models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'users'
    objects=UsersManager()
    def __str__(self):
        return self.username

class a(models.Model):
    a=models.CharField(max_length=10)
    pass
class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, blank=False, null=False)
    seat = models.ForeignKey('Seats',on_delete= models.CASCADE, blank=False, null=False)
    reservation_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, default='reserved')
    checked_in = models.IntegerField(blank=True, null=True)
    check_in_time = models.DateTimeField(blank=True, null=True)
    objects=models.Manager()
    class Meta:
        managed = True
        db_table = 'reservations'
        indexes = [
            models.Index(fields=['seat', 'start_time', 'end_time']),
            models.Index(fields=['status', 'end_time'])
        ]

    def is_expired(self):
        """检查预约是否过期"""
        return self.end_time < timezone.now()

@receiver(pre_save, sender=Reservations)
def update_expired_reservations(sender, instance, **kwargs):
        """
        在保存前检查预约是否过期
        """
        if instance.is_expired() and instance.status != 'expired':
            instance.status = 'expired'