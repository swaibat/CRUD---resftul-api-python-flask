from flask import Flask,jsonify,Response
from flask_restful import reqparse, abort, Api, Resource 
import string
import random
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# app configuration
# app.config.from_object('config.Baseconfig')

rides = [
    # {   
    #     'id': '9DEF45',
    #     'driver': 'Jake',
    #     'origin':'kampala',
    #     'to':'Ntida',
    #     'time': '3:00PM',
    #     'join': False,
    #     },

    # {   
    #     'id': '78NM45',
    #     'driver': 'Peter',
    #     'origin':'kampala',
    #     'to':'Banda',
    #     'time': '4:00PM',
    #     'join': False,
    #     }
]

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
gen_id = random_generator()
now = datetime.now()


def abort_if_ride_doesnt_exist(ride_id):
    if ride not in rides:
        abort(405, message="The requested ride  doesn't exist")

def abort_if_no_rides(rides):
    if len(rides)== 0:
        abort(405, message ="Ooops No rides at the moment")
    
def driver_exist(driver):
    for ride in rides:
        if ride['driver'] == driver:
            abort(409, message="Ooops  driver already exist")

def invalid_characters(name,invalid_character = '~`!@#$%^&*_+= )(|<,>.?/"{[};]'):
    for value in name:
        if value in invalid_character:
            abort(400, message= " you have  used an Invalid character ")


parser = reqparse.RequestParser()
parser.add_argument('driver', )
parser.add_argument('origin',type=str , help ="you have used an invalid character")
parser.add_argument('to')
parser.add_argument('time',)
parser.add_argument('join', type=bool)

# ride
# shows a single ride item and lets you delete a ride item
class ride(Resource):

    def get(self,ride_id):
        """getting a single ride by Ride Id and we pass in a ride_id argument"""
        abort_if_ride_doesnt_exist(ride_id)
        ride = [ride for ride in rides if ride['id'] == ride_id ]
        return ride, 200
        
    def delete(self,ride_id):
        """Delete a single ride by Ride Id and we pass in a ride_id argument"""
        for ride in rides:
            if ride['id'] == ride_id:
                rides.remove(ride)
        return {'message':'ride deleted successfully'}, 200

    def put(self,ride_id):
        """Updating a single ride by Ride Id and we pass in a ride_id argument"""
        args = parser.parse_args()
        for ride in rides:
            if ride['id'] == ride_id:
                ride['driver'] = args['driver']
                ride['origin'] = args['origin']
                ride['to'] = args['to']
                ride['time'] = args['time']
                ride['join'] = args['join']
        return {"massage":"Ride updated successfully"}, 200

# Request a Ride

class rideRequest(Resource):
    
    def patch(self,ride_id):
        """used Patch to edit a specific line ride date in rides"""
        for ride in rides:
            if ride['id'] == ride_id:
                ride['join'] = True
        return {"massage":"A request to join this ride has been sent"}, 200

# ridesList
# shows a list of all rides, and lets you POST to add new rides
class rideList(Resource):

    def get(self):
        """method for getting all rides"""
        abort_if_no_rides(rides)
        return rides, 200
    
    def post(self):
        """metthod for adding a new ride to rides"""
        args = parser.parse_args()
        driver_exist(args['driver'])
        invalid_characters(args['driver'])
        invalid_characters(args['origin'])
        invalid_characters(args['to'])
        ride = {
        'id': gen_id,
        'driver':args['driver'],
        'origin': args['origin'],
        'to': args['to'],
        'time': now.strftime("%X")
        }
        rides.append(ride)
        return {'message':'ride created successfully'}, 201



##
## routing setup
##
api.add_resource(rideList, '/app/v1/rides')
api.add_resource(ride, '/app/v1/rides/<ride_id>')
api.add_resource(rideRequest, '/app/v1/rides/<ride_id>/requests')


if __name__ == '__main__':
    app.run(debug=True)  