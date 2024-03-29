# Generated by Django 3.0.7 on 2020-06-18 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=60, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='Last Login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('fullname', models.CharField(max_length=60)),
                ('position', models.CharField(max_length=45)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=22)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('staff_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('code', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Recorded',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=22)),
                ('time_detected', models.DateTimeField()),
                ('image', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=22)),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('classroom_fk', models.ForeignKey(db_column='classroom_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Classroom')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_code', models.CharField(max_length=22)),
                ('academic_year', models.CharField(max_length=22)),
                ('semester', models.CharField(max_length=22)),
                ('course_fk', models.ForeignKey(db_column='course_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('course_staff_fk', models.ForeignKey(db_column='course_staff', on_delete=django.db.models.deletion.CASCADE, related_name='course_staff', to='app.Course')),
                ('scheduleClassroom_fk', models.ForeignKey(db_column='schedule_classroom_fk', on_delete=django.db.models.deletion.CASCADE, related_name='classroom_schedule', to='app.Schedule')),
                ('schedule_fk', models.ForeignKey(db_column='schedule_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=22)),
                ('student_id', models.CharField(max_length=22)),
                ('department_fk', models.ForeignKey(db_column='department_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Department')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_on_time', models.IntegerField()),
                ('attendance_late', models.IntegerField()),
                ('attendance_absent', models.IntegerField()),
                ('attendance_suspended', models.IntegerField()),
                ('section_course_fk', models.ForeignKey(db_column='section_course_fk', on_delete=django.db.models.deletion.CASCADE, related_name='section_course', to='app.Section')),
                ('section_course_staff_fk', models.ForeignKey(db_column='section_course_staff_fk', on_delete=django.db.models.deletion.CASCADE, related_name='section_staff', to='app.Section')),
                ('section_fk', models.ForeignKey(db_column='section_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Section')),
                ('section_schedule_classroom_fk', models.ForeignKey(db_column='section_schedule_classroom_fk', on_delete=django.db.models.deletion.CASCADE, related_name='section_classroom', to='app.Section')),
                ('section_schedule_fk', models.ForeignKey(db_column='section_schedule_fk', on_delete=django.db.models.deletion.CASCADE, related_name='section_schedule', to='app.Section')),
                ('student_fk', models.ForeignKey(db_column='student_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Student')),
            ],
        ),
        migrations.CreateModel(
            name='CourseHasStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Student')),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='course_fk',
            field=models.ForeignKey(db_column='course_fk', on_delete=django.db.models.deletion.CASCADE, to='app.Course'),
        ),
        migrations.AddField(
            model_name='staff',
            name='department_fk',
            field=models.ForeignKey(db_column='department_fk', default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Department'),
        ),
    ]
