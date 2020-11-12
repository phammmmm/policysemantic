import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','murdoch_policy.settings')

import django
django.setup()

from murdochpolicyapp import utils

def sendReminders():
    utils.sendReminderBatch()
if __name__ == "__main__":
    sendReminders()