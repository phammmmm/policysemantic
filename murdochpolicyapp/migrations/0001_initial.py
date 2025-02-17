# Generated by Django 3.1.3 on 2020-11-15 05:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import murdochpolicyapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['-category_name'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('version', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('created_date', models.DateTimeField()),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('last_review_date', models.DateTimeField()),
                ('review_interval', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('next_review_date', models.DateTimeField()),
                ('document_size', models.IntegerField(default=1)),
                ('document_text', models.TextField()),
                ('feature_words', models.TextField()),
                ('document_file', models.FileField(blank=True, max_length=256, upload_to=murdochpolicyapp.models.get_path, validators=[murdochpolicyapp.models.validate_file_extension])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='murdochpolicyapp.category')),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['-document_type'],
            },
        ),
        migrations.CreateModel(
            name='StopWord',
            fields=[
                ('value', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='murdochpolicyapp.document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentSource', to='murdochpolicyapp.document')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentTarget', to='murdochpolicyapp.document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='murdochpolicyapp.documenttype'),
        ),
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
