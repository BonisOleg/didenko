"""Seed кроків процесу на /posluhy/."""

from django.core.management.base import BaseCommand

from src.services.models import ProcessStep

DEFAULTS = (
    ('Первинна консультація', 'Безкоштовний аналіз вашої ситуації.', 10),
    ('Аудит та підготовка', 'Збір документів та оцінка ризиків.', 20),
    ('Подача заяви до суду', 'Відкриття провадження у справі.', 30),
    ('Отримання рішення', 'Повне або часткове списання боргів.', 40),
)


class Command(BaseCommand):
    help = 'Seed ProcessStep defaults (idempotent if table empty).'

    def handle(self, *args, **options):
        if ProcessStep.objects.exists():
            self.stdout.write('ProcessStep вже є — пропуск')
            return
        ProcessStep.objects.bulk_create(
            [
                ProcessStep(title=t, text=txt, sort_order=order, is_active=True)
                for t, txt, order in DEFAULTS
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'ProcessStep seed: {len(DEFAULTS)}'))
