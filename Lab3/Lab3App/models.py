# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ChangesProjectStatus(models.Model):
    id_changing = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Projects', models.DO_NOTHING, db_column='id_project', blank=True, null=True)
    id_customer = models.ForeignKey('Customers', models.DO_NOTHING, db_column='id_customer', blank=True, null=True)
    id_team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='id_team', blank=True, null=True)
    changing_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'changes_project_status'


class Customers(models.Model):
    id_customer = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=256, blank=True, null=True)
    customer_email = models.CharField(max_length=256, blank=True, null=True)
    customer_phone = models.CharField(max_length=256, blank=True, null=True)
    invitings_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Projects(models.Model):
    id_project = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=256, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    finish_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class Teams(models.Model):
    id_team = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=256, blank=True, null=True)
    team_department = models.CharField(max_length=256, blank=True, null=True)
    manager_name = models.CharField(max_length=256, blank=True, null=True)
    developers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'


class History(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    filmCreations_id = models.IntegerField(db_column='FilmCreations_Id')
    filmHistory = models.CharField(db_column='FilmHistory', max_length=80, blank=True, null=True)
    directorHistory = models.CharField(db_column='DirectorHistory', max_length=80, blank=True, null=True)
    studioHistory = models.CharField(db_column='StudioHistory', max_length=80, blank=True, null=True)
    date = models.DateTimeField(db_column='Date')

    class Meta:
        managed = False
        db_table = 'History'

