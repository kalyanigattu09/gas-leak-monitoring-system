import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GasReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gas_level', models.PositiveSmallIntegerField()),
                ('status', models.CharField(choices=[('SAFE', 'Safe'), ('WARNING', 'Warning'), ('DANGER', 'Danger')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gas_readings', to='rooms.room')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField()),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('RESOLVED', 'Resolved')], default='ACTIVE', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='rooms.room')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='gasreading',
            index=models.Index(fields=['room', '-timestamp'], name='monitoring__room_id_8a1b2c_idx'),
        ),
        migrations.AddIndex(
            model_name='gasreading',
            index=models.Index(fields=['status', '-timestamp'], name='monitoring__status_3d4e5f_idx'),
        ),
        migrations.AddIndex(
            model_name='alert',
            index=models.Index(fields=['status', '-timestamp'], name='monitoring__status_6g7h8i_idx'),
        ),
        migrations.AddIndex(
            model_name='alert',
            index=models.Index(fields=['room', '-timestamp'], name='monitoring__room_id_9j0k1l_idx'),
        ),
    ]
