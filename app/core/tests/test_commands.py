from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class  CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """ Test wainting for db connection when it is 
            already ready to accept connections
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True ## override ret value of get item
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1) #just called once to return true
    

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts) : ## ts object passed from patch
       "test wainting for db connection to become ready before starting our application"
       with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
           gi.side_effect =[OperationalError] * 5 + [True]
           call_command('wait_for_db')
           # just called 6 times to return true
           self.assertEqual(gi.call_count, 6)
