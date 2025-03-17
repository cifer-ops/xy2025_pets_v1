# Generated by Django 3.2.7 on 2022-07-25 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Registered'), ('1', 'Passed'), ('2', 'Passed')], default='0', max_length=1024, verbose_name='status')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
            options={
                'verbose_name': 'adoption',
                'verbose_name_plural': 'adoption',
            },
        ),
        migrations.RemoveField(
            model_name='zan',
            name='pet',
        ),
        migrations.RemoveField(
            model_name='zan',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='collect',
            options={'verbose_name': 'Collect', 'verbose_name_plural': 'Collect'},
        ),
        migrations.AlterModelOptions(
            name='petsinfo',
            options={'verbose_name': 'PetsInfo', 'verbose_name_plural': 'PetsInfo'},
        ),
        migrations.AlterModelOptions(
            name='petstype',
            options={'verbose_name': 'PetsType', 'verbose_name_plural': 'PetsType'},
        ),
        migrations.RemoveField(
            model_name='petsinfo',
            name='author',
        ),
        migrations.RemoveField(
            model_name='petsinfo',
            name='chubanshe',
        ),
        migrations.RemoveField(
            model_name='petsinfo',
            name='shou_count',
        ),
        migrations.RemoveField(
            model_name='petsinfo',
            name='show_time',
        ),
        migrations.AlterField(
            model_name='collect',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create_time'),
        ),
        migrations.AlterField(
            model_name='collect',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='age',
            field=models.IntegerField(default=0, verbose_name='age'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='area',
            field=models.CharField(max_length=1024, verbose_name='area'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='atype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.petstype', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create_time'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='intro',
            field=models.CharField(max_length=1024, verbose_name='introduce'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='showimg',
            field=models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='show image'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='status',
            field=models.CharField(choices=[('0', 'Publish'), ('1', 'Adopted person selected'), ('2', 'Adopted')], default='0', max_length=1024, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='petsinfo',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='petstype',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='petstype',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='type name'),
        ),
        migrations.AlterField(
            model_name='petstype',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='modify'),
        ),
        migrations.DeleteModel(
            name='CommentInfo',
        ),
        migrations.DeleteModel(
            name='Zan',
        ),
        migrations.AddField(
            model_name='adoption',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.petsinfo'),
        ),
        migrations.AddField(
            model_name='adoption',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
