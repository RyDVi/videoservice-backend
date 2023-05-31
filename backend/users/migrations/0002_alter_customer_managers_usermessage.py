# Generated by Django 4.0.5 on 2023-05-27 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customer',
            managers=[
                ('objects', users.managers.CustomerQuerySet()),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(verbose_name='text of message')),
                ('created_at', models.DateTimeField(verbose_name='datetime of creation')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_messages',
            },
        ),
    ]