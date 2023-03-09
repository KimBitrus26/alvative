# Generated by Django 4.1.7 on 2023-03-09 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alvative_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DumpPaystackData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dump_data', models.TextField()),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
