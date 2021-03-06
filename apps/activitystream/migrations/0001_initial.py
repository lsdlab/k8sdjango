# Generated by Django 2.1.10 on 2019-09-29 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('actor', models.CharField(max_length=255)),
                ('actor_id', models.CharField(max_length=255)),
                ('verb', models.CharField(max_length=255)),
                ('object', models.CharField(blank=True, default='', max_length=255)),
                ('object_id', models.CharField(blank=True, default='', max_length=255)),
                ('target', models.CharField(blank=True, default='', max_length=255)),
                ('target_id', models.CharField(blank=True, default='', max_length=255)),
                ('deleted', models.BooleanField(default=False)),
                ('exchange', models.TextField(blank=True, choices=[('1', '主题'), ('2', '直连'), ('3', '扇形')], max_length=1, null=True)),
                ('routing_key', models.CharField(blank=True, max_length=255, null=True)),
                ('ack', models.NullBooleanField(default=None)),
            ],
            options={
                'verbose_name': '动态消息',
                'verbose_name_plural': '动态消息',
                'ordering': ['-created_at'],
            },
        ),
    ]
