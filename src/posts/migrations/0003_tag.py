# Generated by Django 3.1.7 on 2021-04-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210414_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created att')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified.', verbose_name='modified att')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('active', models.BooleanField(default=True)),
                ('posts', models.ManyToManyField(blank=True, to='posts.Post')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]