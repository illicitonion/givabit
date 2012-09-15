import os

from google.appengine.ext import db

SKIP_TRANSACTIONS_FOR_TEST = 'SKIP_TRANSACTIONS_FOR_TEST' in os.environ

def transactionally(fn):
    if SKIP_TRANSACTIONS_FOR_TEST:
        fn()
    else:
        db.run_in_transaction(fn)
