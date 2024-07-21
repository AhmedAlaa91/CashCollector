from django.core.management.base import BaseCommand
from...utilities.scripts.callCheckAllUsersStatus import checkUserStatusApi
class Command(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **kwargs):

        checkUserStatusApi()
        #self.stdout.write(responseStatus)

        self.stdout.write('Users Status Check is running')