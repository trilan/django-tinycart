import sys

from django.core.management.base import BaseCommand

from tinycart.models import CartItem


def delete_objects(verbosity=1):
    stdout = sys.stdout
    count_lost_items = 0
    for item in CartItem.objects.all():
        if item.product is None:
            item.delete()
            count_lost_items += 1
    if verbosity > 0:
        stdout.write('Delete %d cart items\n' % count_lost_items)


class Command(BaseCommand):

    help = 'Remove lost (deleted) products from cart items.'

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        delete_objects(verbosity=self.verbosity)
