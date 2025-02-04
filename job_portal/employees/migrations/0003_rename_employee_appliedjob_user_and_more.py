# Generated by Django 4.2 on 2024-12-24 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_rename_user_appliedjob_employee_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appliedjob',
            old_name='employee',
            new_name='user',
        ),
        migrations.AddField(
            model_name='appliedjob',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='appliedjob',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.AlterField(
            model_name='appliedjob',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
