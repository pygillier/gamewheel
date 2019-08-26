# Generated by Django 2.2.4 on 2019-08-26 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('appid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('icon_id', models.CharField(max_length=40)),
                ('logo_id', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GameStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playtime', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('steamid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=255)),
                ('real_name', models.CharField(max_length=255)),
                ('profile_url', models.URLField()),
                ('avatar_url', models.URLField()),
                ('avatar_m_url', models.URLField()),
                ('avatar_f_url', models.URLField()),
                ('country_code', models.CharField(max_length=4)),
                ('creation_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('games', models.ManyToManyField(through='library.GameStat', to='library.Game')),
            ],
            options={
                'ordering': ('nickname',),
            },
        ),
        migrations.AddField(
            model_name='gamestat',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Player'),
        ),
    ]
