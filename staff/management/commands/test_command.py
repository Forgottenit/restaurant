# from django.core.management.commands.test import Command as TestCommand
# import os

# class Command(TestCommand):
#     def handle(self, *args, **options):
#         print("Custom test command is being executed.")  # Add this line
#         os.environ['USE_SQLITE_FOR_TEST'] = '1'
#         try:
#             super().handle(*args, **options)
#         finally:
#             del os.environ['USE_SQLITE_FOR_TEST']

from django.core.management.commands.test import Command as TestCommand
from django.test import TestCase
from django.test.utils import override_settings

class Command(TestCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--use-sqlite', action='store_true', help='Use SQLite for testing')

    def handle(self, *args, **options):
        if options['use_sqlite']:
            sqlite_db_settings = {
                'DATABASES': {
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    }
                }
            }
            with override_settings(**sqlite_db_settings):
                super().handle(*args, **options)
        else:
            super().handle(*args, **options)