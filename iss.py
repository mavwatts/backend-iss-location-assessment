#!/usr/bin/env python

__author__ = 'Mavrick Watts'

import requests
import time
import turtle 


def astronauts_in_space():
    '''obtain a list of the astronauts who are currently in space. Print their full names,
    the spacecraft they are currently on board, and the total number of astronauts in space.'''
    response = requests.get('http://api.open-notify.org/astros.json')
    response.raise_for_status()
    return response.json()["people"]


def geographic_location():
    '''obtain the current geographic coordinates (lat/lon) of the space station,
    along with a timestamp.'''
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    location = response.json()["iss_position"]
    lat = float(location["latitude"])
    lon = float(location["longitude"])

    return lat, lon


def iss_time():
    '''Shows the timestamp.'''
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    iss_time = response.json()["timestamp"]

    return time.ctime(iss_time)


def iss_map(Lat, Long):
    '''World map image.'''
    current_time = iss_time()
    screen = turtle.Screen()
    screen.setup(width=720, height=360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.register_shape("iss.gif")
    screen.bgpic("map.gif")
    iss = turtle.Turtle()
    iss.shape("iss.gif")
    iss.setheading(90)
    iss.penup()
    iss.color('red')
    iss.goto(Long, Lat)
    style = ('Arial', 14, 'bold')
    iss.write(current_time, align='center', font=style)
    return screen


def iss_overhead(Lat, Long):
    parameters = {"lat": Lat, "lon": Long}
    response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
    response.raise_for_status()
    over_indy = response.json()['response'][1]['risetime']
    return time.ctime(over_indy)


def main():
    names = ''
    astro_dict = astronauts_in_space()
    for people in astro_dict:
        names += people['name'] + ', '
    print("There are currently {} astronauts onboard".format(len(astro_dict)))
    print('Their names are: ' + names[:-2] + ' and they are on ' + str(people['craft']) + '.')
    Lat, Long = geographic_location()
    print("Latitude: ", Lat)
    print("Longitude: ", Long)
    screen = None
    screen = iss_map(Lat, Long)
    lat_indy = float(39.768452)
    long_indy = float(-86.156212)
    location_indy = turtle.Turtle()
    location_indy.penup()
    location_indy.color('yellow')
    location_indy.goto(long_indy, lat_indy)
    location_indy.dot(5)
    location_indy.hideturtle()
    next_pass = iss_overhead(lat_indy, long_indy)
    style = ('Arial', 12, 'normal')
    location_indy.write(next_pass, align='center', font=style)
    # indy_pass = iss_overhead(lat_indy, long_indy)
    # location_indy.write(indy_pass, font=style)
    if screen is not None:
        print('Click on screen to exit...')
        screen.exitonclick()
        # style = ('Arial',12,'bold')


if __name__ == '__main__':
    main() 