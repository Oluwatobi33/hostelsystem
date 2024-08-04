# Generated by Django 4.2.14 on 2024-08-03 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("customer_name", models.CharField(max_length=100)),
                ("check_in_date", models.DateField()),
                ("check_out_date", models.DateField()),
                ("is_paid", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Candidate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=50)),
                ("lastname", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=15)),
                ("address", models.CharField(max_length=150)),
                ("city", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("dob", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Other", "Other"),
                        ],
                        max_length=10,
                    ),
                ),
                ("special_requests", models.TextField(blank=True, null=True)),
                (
                    "profile_pic",
                    models.ImageField(blank=True, null=True, upload_to="img/candidate"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "room_type",
                    models.CharField(
                        choices=[("1", "Single"), ("2", "Double"), ("3", "Suite")],
                        max_length=2,
                    ),
                ),
                ("username", models.CharField(db_index=True, max_length=100)),
                (
                    "email",
                    models.EmailField(db_index=True, max_length=200, unique=True),
                ),
                (
                    "matric_number",
                    models.EmailField(
                        blank=True, max_length=200, null=True, unique=True
                    ),
                ),
                (
                    "application_number",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "user_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Undergraduate", "Undergraduate"),
                            ("Postgraduate", "Postgraduate"),
                            ("Jupeb", "Jupeb"),
                            ("Topup", "Topup"),
                            ("Parent", "Parent"),
                            ("Staff", "Staff"),
                            ("Others", "Others"),
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female")],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("100", "100"),
                            ("200", "200"),
                            ("300", "300"),
                            ("400", "400"),
                            ("Spill Over", "Spill Over"),
                            ("Jupeb", "Jupeb"),
                            ("Topup", "Topup"),
                            ("Others", "Others"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "phone_no",
                    models.CharField(blank=True, default="", max_length=15, null=True),
                ),
                ("department", models.CharField(blank=True, max_length=200, null=True)),
                ("programme", models.CharField(blank=True, max_length=200, null=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_student", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_created", models.DateTimeField(auto_now_add=True)),
                ("is_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserMaster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=50)),
                ("password", models.CharField(max_length=50)),
                ("role", models.CharField(max_length=50)),
                ("is_active", models.BooleanField(default=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_created", models.DateTimeField(auto_now_add=True)),
                ("is_updated", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Receipt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("transaction_reference", models.CharField(max_length=100)),
                ("date_generated", models.DateTimeField(auto_now_add=True)),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="homeapp.booking",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.PositiveBigIntegerField()),
                (
                    "hostel_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("room_type", models.CharField(blank=True, max_length=200, null=True)),
                ("session", models.CharField(blank=True, max_length=200, null=True)),
                ("room_upgrade", models.BooleanField(default=False)),
                ("ref", models.CharField(max_length=210)),
                ("email", models.EmailField(max_length=200)),
                ("verified", models.BooleanField(default=False)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="homeapp.room",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="homeapp.candidate",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=50)),
                ("company_contact", models.CharField(max_length=50)),
                ("company_website", models.URLField()),
                ("firstname", models.CharField(max_length=50)),
                ("lastname", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=150)),
                ("telephone", models.CharField(max_length=15)),
                ("description", models.TextField()),
                ("logo_pic", models.ImageField(upload_to="img/company")),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="homeapp.usermaster",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="candidate",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="homeapp.usermaster"
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="homeapp.room"
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="homeapp.candidate"
            ),
        ),
    ]
