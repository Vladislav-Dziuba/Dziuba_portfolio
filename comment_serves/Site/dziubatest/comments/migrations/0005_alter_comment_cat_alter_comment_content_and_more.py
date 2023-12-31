# Generated by Django 4.2.3 on 2023-07-17 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_alter_comment_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comments.category', verbose_name='Бинарная оценка'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, verbose_name='Текст отзыва'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pred',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Распознавание'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='score',
            field=models.PositiveIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], null=True, verbose_name='Score'),
        ),
    ]
