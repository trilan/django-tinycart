import sys

from django.core.management.base import BaseCommand

from tinycart.models import CartItem


class Command(BaseCommand):

    help = 'Remove lost (deleted) products from cart items.'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity'))
        count_lost_items = 0

        for item in CartItem.objects.all():
            if item.product is None:
                item.delete()
                count_lost_items += 1

        if verbosity > 0:
            sys.stdout.write('Delete %d cart items\n' % count_lost_items)
