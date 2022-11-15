#!/usr/bin/env python3

"""
Columbia W4111 Intro to databases
Project1 webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# XXX: The Database URI should be in the format of:
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "jl6016"
DB_PASSWORD = "0232"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":" + \
    DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


# Here we create a test table and insert some values in it
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute(
    """INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request 
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request

    The variable g is globally accessible
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


# @app.route is a decorator around index() that means:
# @app.route("/foobar/", methods=["POST", "GET"])

@app.route('/')
def index():
    return render_template("index.html", **{"data":["No query by now"]})


# @app.route('/')
# def index():
#   print (request.args)
#   return render_template("index.html")


@app.route('/show_data', methods=['GET'])
def show_data():

    return redirect('/')


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    # crashes
    collision_id = request.form['collision_id']
    crash_date = request.form['crash_date']
    crash_time = request.form['crash_time']
    # victims
    victim_id = request.form['victim_id']
    position_in_vehicle = request.form['position_in_vehicle']
    bodily_injury = request.form['bodily_injury']
    # vehicles
    vehicle_id = request.form['vehicle_id']
    vehicle_type = request.form['vehicle_type']
    # locations
    location_id = request.form['location_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    borough = request.form['borough']
    zip_code = request.form['zip_code']
    on_street_name = request.form['on_street_name']
    off_street_name = request.form['off_street_name']
    # contributingfactors
    factor_id = request.form['factor_id']
    description = request.form['description']
    # consequences
    consequence_id = request.form['consequence_id']
    nperson_injured = request.form['nperson_injured']
    nperson_killed = request.form['nperson_killed']
    npedestrian_injured = request.form['npedestrian_injured']
    npedestrian_killed = request.form['npedestrian_killed']
    ncyclist_injured = request.form['ncyclist_injured']
    ncyclist_killed = request.form['ncyclist_killed']
    nmotorist_injured = request.form['nmotorist_injured']
    nmotorist_killed = request.form['nmotorist_killed']

    # print(collision_id, victim_id, vehicle_id,location_id,factor_id,consequence_id)

    cmd_crashes = 'INSERT INTO crashes VALUES ((:collision_id),(:crash_date),(:crash_time))'
    cmd_victims = 'INSERT INTO victims VALUES ((:victim_id),(:position_in_vehicle),(:bodily_injury))'
    cmd_vehicles = 'INSERT INTO vehicles VALUES ((:vehicle_id),(:vehicle_type))'
    cmd_locations = 'INSERT INTO locations VALUES ((:location_id),(:latitude),(:longitude),(:borough),(:zip_code),(:on_street_name),(:off_street_name))'
    cmd_contributingfactors = 'INSERT INTO contributingfactors VALUES ((:factor_id),(:description))'
    cmd_consequences = 'INSERT INTO consequences VALUES ((:consequence_id),(:nperson_injured),(:nperson_killed),(:npedestrian_injured),(:npedestrian_killed),(:ncyclist_injured),(:ncyclist_killed),(:nmotorist_injured),(:nmotorist_killed))'

    cmd_cause = 'INSERT INTO cause VALUES ((:factor_id), (:collision_id))'
    cmd_sit = 'INSERT INTO sit VALUES ((:victim_id), (:vehicle_id), (:position_in_vehicle),(:bodily_injury))'
    cmd_result = 'INSERT INTO result VALUES ((:collision_id), (:consequence_id), (:crash_date),(:crash_time))'
    cmd_occur = 'INSERT INTO occur VALUES ((:collision_id),(:location_id), (:crash_date),(:crash_time))'
    cmd_involve = 'INSERT INTO involve VALUES ((:collision_id), (:victim_id))'

    g.conn.execute(text(cmd_crashes), collision_id=int(collision_id), crash_date=crash_date, crash_time=crash_time)
    g.conn.execute(text(cmd_victims), victim_id=int(victim_id), position_in_vehicle=position_in_vehicle, bodily_injury=bodily_injury)
    g.conn.execute(text(cmd_vehicles), vehicle_id=int(vehicle_id), vehicle_type=vehicle_type)
    g.conn.execute(text(cmd_locations), location_id=int(location_id), latitude=latitude, longitude=longitude, borough=borough, zip_code=int(zip_code), on_street_name=on_street_name, off_street_name=off_street_name)
    g.conn.execute(text(cmd_contributingfactors), factor_id=int(factor_id), description=description)
    g.conn.execute(text(cmd_consequences), consequence_id=int(consequence_id), nperson_injured=int(nperson_injured), nperson_killed=int(nperson_killed), npedestrian_injured=int(npedestrian_injured), npedestrian_killed=int(npedestrian_killed), ncyclist_injured=int(ncyclist_injured), ncyclist_killed=int(ncyclist_killed), nmotorist_injured=int(nmotorist_injured), nmotorist_killed=int(nmotorist_killed))

    g.conn.execute(text(cmd_cause), factor_id=int(factor_id), collision_id=int(collision_id))
    g.conn.execute(text(cmd_sit), victim_id=int(victim_id), vehicle_id=int(vehicle_id), position_in_vehicle=position_in_vehicle, bodily_injury=bodily_injury)
    g.conn.execute(text(cmd_result), collision_id=int(collision_id), consequence_id=int(consequence_id), crash_date=crash_date, crash_time=crash_time)
    g.conn.execute(text(cmd_occur), collision_id=int(collision_id), location_id=int(location_id), crash_date=crash_date, crash_time=crash_time)
    g.conn.execute(text(cmd_involve), collision_id=int(collision_id), victim_id=int(victim_id))

    return redirect('/')
    
@app.route("/showCrashes", methods = ["POST"])
def showCrashes():
  numOfCrashes = request.form['numOfCrashes']
  if numOfCrashes.isdigit():
    numOfCrashes = int(numOfCrashes)
  elif numOfCrashes == "" or numOfCrashes == "ALL":
    numOfCrashes = 1e9
  else:
    return render_template("index.html", **{"data": ["Invalid Input!!"]})
  cmd_show = """
  select *
  from crashes
  limit (:numOfCrashes)
  """
  cursor = g.conn.execute(text(cmd_show), numOfCrashes = numOfCrashes)
  arr = []
  for result in cursor:
    arr.append(result)
  context = dict(data = arr)
  return render_template("index.html", **context)

@app.route("/vvc", methods = ["POST"])
def vvc():
    crashIds = request.form['crashId']
    crashIds = crashIds.split(',')

    cmd_vvc = """
    select c.collision_id, v.victim_id, vh.vehicle_id, vh.vehicle_type
    from crashes as c, involve as i, sit as s, victims as v, vehicles as vh
    where c.collision_id = i.collision_id and v.victim_id = i.victim_id and v.victim_id = s.victim_id
    and s.vehicle_id = vh.vehicle_id and c.collision_id = (:crashId)
    """

    arr = []
    for i in range(len(crashIds)):
        cursor = g.conn.execute(text(cmd_vvc), crashId = int(crashIds[i]))
        for result in cursor:
            arr.append(result)
    
    context = dict(data = arr)
    return render_template("index.html", **context)

@app.route("/BodyInjury", methods = ["POST"])
def BodyInjury():
    victimId = request.form['victimId']
    cmd_BodyInjury = """
    select victim_id, bodily_injury
    from victims
    where victim_id = (:victimId)
    """
    
    arr=[]
    cursor = g.conn.execute(text(cmd_BodyInjury), victimId = int(victimId))
    for result in cursor:
        arr.append(result)
    context = dict(data = arr)
    return render_template("index.html", **context)


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using

            python server.py

        Show the help text using

            python server.py --help

        """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
