import unittest
import api
import requests
import json
import sys


test1 =  {   
        'id': 'HD3H4B',
        'driver': 'khali',
        'origin':'kampala',
        'to':'Ntida',
        'time': '3:00PM',
        'join': False,
        }
test2 =  {   
        'id': '9DEF45',
        'driver': 'swaibu',
        'origin':'kampala',
        'to':'Ntida',
        'time': '3:00PM',
        'join': False,
        }

test3 =  {   
        'id': '9DHD42',
        'driver': 'swaibu>',
        'origin':'kampala',
        'to':'Ntida',
        'time': '3:00PM',
        'join': False,
        }
test4 =  {   
        'id': 'WDHD73',
        'driver': 'john',
        'origin':'kampala',
        'to':'Ntida',
        'time': '3:00PM',
        'join': False,
        }
test5 =  {   
        'id': 'WDG47G',
        'driver': 'amanda',
        'origin':'kampala',
        'to':'Ntida',
        'time': '3:00PM',
        'join': False,
        }

test6 =  {
        'id': 'WDG47J',   
        'driver': 'dora',
        'origin':'kampala',
        'to':'Ntida',
        'time': '3:00PM',
        'join': False
        }

class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()
        self.ride = {
                'id': '9DEF45',
                'driver': 'matovu',
                'origin':'kampala',
                'to':'Ntida',
                'time': '3:00PM',
                'join': False,
                }

    def test_abort_if_ride_doesnt_exist(self):
        response = self.app.get('/app/v1/rides/EGH35T')
        self.assertEqual(response.status_code,405)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"message": "The requested ride  doesn't exist"}
        )
    
    def test_abort_if_no_rides(self):
        response = self.app.get('/app/v1/rides')
        self.assertEqual(response.status_code,405)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"message": "Ooops No rides at the moment"}
        )
    
    def test_ride_creation(self):
        """Test API can create a ride (POST request)"""
        response = self.app.post('/app/v1/rides',
                                    content_type='application/json',
                                    data=json.dumps(self.ride))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {'message':'ride created successfully'}
        )
    
    def test_update_ride(self):
        response = self.app.put('/app/v1/rides/9DEF45',
                                    content_type='application/json',
                                    data=json.dumps(test2))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"massage":"Ride updated successfully"}
        )
    
    def test_invalid_characters(self):
        response = self.app.post('/app/v1/rides',
                                    content_type='application/json',
                                    data=json.dumps(test3))
        self.assertEqual(response.status_code,400)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"message": " you have  used an Invalid character "}
        )
        
    def test_request_ride(self):
            response = self.app.post('/app/v1/rides',
                                        content_type='application/json',
                                        data=json.dumps(test4))
            self.assertEqual(response.status_code, 201)
            response = self.app.patch('/app/v1/rides/9DEF45/requests',
                                        content_type='application/json',
                                        data=json.dumps(test4))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                json.loads(response.get_data().decode(sys.getdefaultencoding())), 
                {"massage":"A request to join this ride has been sent"}
            )
    def test_delete_ride(self):
            response = self.app.post('/app/v1/rides',
                                        content_type='application/json',
                                        data=json.dumps(test5))
            self.assertEqual(response.status_code, 201)
            response = self.app.delete('/app/v1/rides/WDG47G',
                                        content_type='application/json',
                                        data=json.dumps(test5))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                json.loads(response.get_data().decode(sys.getdefaultencoding())), 
                {'message':'ride deleted successfully'}
            )
    
    def test_driver_exist(self):
        response = self.app.post('/app/v1/rides',
                                    content_type='application/json',
                                    data=json.dumps(test1))
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/app/v1/rides',
                                    content_type='application/json',
                                    data=json.dumps(test1))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {'message':'Ooops  driver already exist'}
        )

    def test_query_rides(self):
            response = self.app.post('/app/v1/rides',
                                        content_type='application/json',
                                        data=json.dumps(test6))
            self.assertEqual(response.status_code, 201)
            response = self.app.get('/app/v1/rides',
                                        content_type='application/json',
                                        data=json.dumps(test6))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(test6['driver'],'dora')
            self.assertEqual(test6['origin'],'kampala')
    
        


    
if __name__ == "__main__":
    unittest.main()