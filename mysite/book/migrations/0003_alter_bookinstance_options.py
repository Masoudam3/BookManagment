# Generated by Django 3.2.11 on 2022-01-10 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_read_private_section', 'VIP_user'), ('user_watcher', 'User Watcher'))},
        ),
    ]