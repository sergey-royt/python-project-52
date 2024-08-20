# Generated by Django 5.0.7 on 2024-08-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0002_tasklabelrelation_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='labels', through='tasks.TaskLabelRelation', to='labels.label', verbose_name='Labels'),
        ),
    ]
