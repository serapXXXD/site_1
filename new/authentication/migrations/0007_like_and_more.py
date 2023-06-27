# Generated by Django 4.2 on 2023-06-17 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_created_at_post_updated_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0006_alter_subscription_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'лайки',
                'ordering': ['-id'],
            },
        ),
        migrations.RemoveConstraint(
            model_name='subscription',
            name='usnuque_together_subscriber_author',
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('subscriber', 'author'), name='unuque_together_subscriber_author'),
        ),
        migrations.AddField(
            model_name='like',
            name='liked_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blog.post'),
        ),
        migrations.AddField(
            model_name='like',
            name='liker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('liker', 'liked_post'), name='unique_together_liker_post'),
        ),
    ]
