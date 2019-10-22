import uuid
from enum import IntEnum
from django.db import models
from django.contrib.postgres.fields import JSONField


class Status(IntEnum):
    CREATED = 0
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    output_directory = models.CharField(max_length=400)


class Job(BaseModel):
    app = JSONField(null=False)
    external_id = models.CharField(max_length=50)
    job_store_location = models.CharField(max_length=1000)
    working_dir = models.CharField(max_length=1000)
    status = models.IntegerField(choices=[(status.value, status.name) for status in Status], default=Status.CREATED)
    inputs = JSONField(blank=True, null=False)
    outputs = JSONField(blank=True, null=False)
    track_cache = JSONField(blank=True, null=True)


class CommandLineToolJob(BaseModel):
    root = models.ForeignKey(Job, blank=False, null=False, on_delete=models.CASCADE)
    status = models.IntegerField(choices=[(status.value, status.name) for status in Status], default=0)
    started = models.DateTimeField(blank=True)
    submitted = models.DateTimeField(blank=True)
    finished = models.DateTimeField(blank=True)
    job_name = models.CharField(max_length=100)
    job_id = models.CharField(max_length=20)
    details = JSONField(blank=True, null=True)
