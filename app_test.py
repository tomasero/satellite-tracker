from server import app
from time import strftime, localtime

import os
import json
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

    def test_correct_response(self):
        print 'Test correct response'
        time = strftime("%y/%m/%d,%H:%M:%S+00", localtime())
        tester = app.test_client(self)
        response = tester.post('/get_satellites_locations', data=dict(
                latitude = '37.877652',
                longitude = '-122.262247',
                time = time
            ), follow_redirects=True);
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)

    def test_incorrect_response(self):
        print 'Test incorrect response'
        time = strftime("%y/%m/%d,%H:%M:%S+00", localtime())
        tester = app.test_client(self)
        response = tester.post('/get_satellites_locations', data=dict(
                longitude = '-122.262247',
                time = time
            ), follow_redirects=True);
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Please provide latitude.')
        response = tester.post('/get_satellites_locations', data=dict(
                latitude = '37.877652',
                time = time
            ), follow_redirects=True);
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Please provide longitude.')
        response = tester.post('/get_satellites_locations', data=dict(
                latitude = '37.877652',
                longitude = '-122.262247'
            ), follow_redirects=True);
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Please provide time.')

    def test_no_satellites_visible(self):
        print 'Test no satellites visible'
        time = '15/03/28,06:20:20+12'
        tester = app.test_client(self)
        response = tester.post('/get_satellites_locations', data=dict(
                latitude = '37.877652',
                longitude = '-122.262247',
                time = time
            ), follow_redirects=True);
        self.assertEqual(response.status_code, 420)


    # def test_missing_params(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/get_satellites_locations?a=2&b=6', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     # Check that the result sent is 8: 2+6
    #     self.assertEqual(json.loads(response.data), {"result": 8})

    # This test will purposely fail
    # We are checking that 2+6 is 10
    # def test_sum_fail(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/_add_numbers?a=2&b=6', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.data), {"result": 10})

if __name__ == '__main__':
    unittest.main()