# Generated by Django 5.1.4 on 2024-12-19 09:08

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company_logo')),
                ('company_name', models.CharField(max_length=100)),
                ('registration_number', models.CharField(blank=True, max_length=50, null=True)),
                ('company_address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(max_length=20)),
                ('company_mobile', models.CharField(max_length=12)),
                ('company_email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True, null=True)),
                ('company_GSTIN', models.CharField(blank=True, max_length=20, null=True)),
                ('established_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('company_obj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.PositiveIntegerField(unique=True)),
                ('invoice_date', models.DateField(default=django.utils.timezone.now)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('net_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('balance_due', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Partially Paid', 'Partially Paid'), ('Overdue', 'Overdue')], default='Pending', max_length=20)),
                ('remarks', models.TextField(blank=True, help_text='Any additional notes or remarks', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bill_obj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='billapp.company')),
            ],
            options={
                'verbose_name': 'Bill',
                'verbose_name_plural': 'Bills',
                'ordering': ['-invoice_date'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('si_no', models.PositiveIntegerField(null=True)),
                ('items', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('unit', models.CharField(choices=[('pcs', 'Pieces'), ('kg', 'Kilograms'), ('ltr', 'Liters'), ('box', 'Box'), ('doz', 'Dozen')], default='pcs', max_length=50)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, help_text='Discount in %', max_digits=5)),
                ('tax', models.CharField(choices=[('GST', 'GST'), ('CGST', 'CGST'), ('SGST', 'SGST'), ('None', 'No Tax')], default='None', max_length=50)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0.0, help_text='Tax rate in %', max_digits=5)),
                ('stock', models.PositiveIntegerField(default=0, help_text='Current stock available')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('items_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='billapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_name', models.CharField(max_length=100)),
                ('receiver_address', models.TextField()),
                ('receiver_city', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver_state', models.CharField(max_length=100)),
                ('receiver_country', models.CharField(blank=True, default='India', max_length=100, null=True)),
                ('receiver_postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('receiver_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('receiver_alternate_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('receiver_email', models.EmailField(max_length=254)),
                ('receiver_GSTIN', models.CharField(blank=True, help_text='GST Identification Number', max_length=20, null=True)),
                ('receiver_pan', models.CharField(blank=True, help_text='PAN Number', max_length=10, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('receiver_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receivers', to='billapp.company')),
            ],
            options={
                'verbose_name': 'Receiver',
                'verbose_name_plural': 'Receivers',
                'ordering': ['receiver_name'],
            },
        ),
        migrations.CreateModel(
            name='ShipTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_name', models.CharField(max_length=100)),
                ('shipping_address', models.TextField()),
                ('shipping_city', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_state', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_country', models.CharField(blank=True, default='India', max_length=100, null=True)),
                ('shipping_postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('shipping_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('shipping_alternate_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('shipping_email', models.EmailField(max_length=254)),
                ('shipping_instructions', models.TextField(blank=True, help_text='Special instructions for delivery', null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('ship_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='billapp.company')),
            ],
            options={
                'verbose_name': 'Ship To',
                'verbose_name_plural': 'Ship To',
                'ordering': ['shipping_name'],
            },
        ),
    ]