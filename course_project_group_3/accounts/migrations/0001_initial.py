# Generated by Django 4.1 on 2024-04-04 00:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BankAccount",
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
                    "account_number",
                    models.PositiveIntegerField(blank=True, unique=True),
                ),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("savings", "Savings"),
                            ("checking", "Checking"),
                            ("credit", "Credit"),
                            ("loan", "Loan"),
                            ("investment", "Investment"),
                            ("retirement", "Retirement"),
                            ("other", "Other"),
                        ],
                        default="checking",
                        max_length=50,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "transaction_limit",
                    models.DecimalField(
                        decimal_places=2, default=1000.0, max_digits=10
                    ),
                ),
                (
                    "overdraft_limit",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("last_transaction_date", models.DateTimeField(blank=True, null=True)),
                (
                    "interest_rate",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                (
                    "monthly_fee",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
                ),
                (
                    "withdrawal_fee",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
                ),
                (
                    "minimum_balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "account_opening_date",
                    models.DateField(default=datetime.datetime.now),
                ),
                ("account_closure_date", models.DateField(blank=True, null=True)),
                ("is_joint_account", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bank_accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserSetting",
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
                ("theme", models.CharField(default="light", max_length=100)),
                ("language", models.CharField(default="en", max_length=100)),
                ("is_notifications_enabled", models.BooleanField(default=True)),
                ("font_size", models.IntegerField(default=12)),
                ("profile_img_url", models.URLField(blank=True, null=True)),
                ("timezone", models.CharField(default="UTC", max_length=50)),
                ("preferred_currency", models.CharField(default="USD", max_length=3)),
                ("email_notifications", models.BooleanField(default=True)),
                ("dark_mode_start_time", models.TimeField(blank=True, null=True)),
                ("dark_mode_end_time", models.TimeField(blank=True, null=True)),
                ("show_balance_on_dashboard", models.BooleanField(default=True)),
                (
                    "monthly_income",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("credit_score", models.IntegerField(default=0)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Setting",
                "verbose_name_plural": "User Settings",
                "db_table": "user_settings",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
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
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("deposit", "Deposit"),
                            ("withdrawal", "Withdrawal"),
                            ("transfer", "Transfer"),
                            ("expense", "Expense"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "transaction_limit",
                    models.DecimalField(
                        decimal_places=2, default=1000.0, max_digits=10
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("img_url", models.URLField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(auto_now=True)),
                ("description", models.TextField(blank=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="accounts.bankaccount",
                    ),
                ),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
                "db_table": "transactions",
            },
        ),
        migrations.CreateModel(
            name="CreditCard",
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
                ("credit_limit", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "available_credit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("due_date", models.DateField(blank=True, null=True)),
                ("reward_points", models.IntegerField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="credit_cards",
                        to="accounts.bankaccount",
                    ),
                ),
            ],
            options={
                "verbose_name": "Credit Card",
                "verbose_name_plural": "Credit Cards",
                "db_table": "credit_cards",
            },
        ),
    ]