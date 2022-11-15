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

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
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

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"


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
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")



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
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print (request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT * FROM crashes")
  arr = []
  for result in cursor:
    arr.append(result)  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = arr)
  

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)


# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another')
def another():
  return render_template("anotherfile.html")

# @app.route('/show_data', methods=['GET'])
# def show_data():


#   return redirect('/')


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  #crashes
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

  cmd_c = 'INSERT INTO crashes VALUES ((:collision_id),(:crash_date),(:crash_time))'
  cmd_vi = 'INSERT INTO victims VALUES ((:victim_id),(:position_in_vehicle),(:bodily_injury))'
  cmd_ve = 'INSERT INTO vehicles VALUES ((:vehicle_id),(:vehicle_type))'
  cmd_l = 'INSERT INTO locations VALUES ((:location_id),(:latitude),(:longitude),(:borough),(:zip_code),(:on_street_name),(:off_street_name))'
  cmd_f = 'INSERT INTO contributingfactors VALUES ((:factor_id),(:description))'
  cmd_con = 'INSERT INTO consequences VALUES ((:consequence_id),(:nperson_injured),(:nperson_killed),(:npedestrian_injured),(:npedestrian_killed),(:ncyclist_injured),(:ncyclist_killed),(:nmotorist_injured),(:nmotorist_killed))'

  g.conn.execute(text(cmd_c), collision_id = int(collision_id), crash_date = crash_date, crash_time= crash_time)
  g.conn.execute(text(cmd_vi), victim_id = int(victim_id),position_in_vehicle=position_in_vehicle,bodily_injury=bodily_injury)
  g.conn.execute(text(cmd_ve), vehicle_id = int(vehicle_id),vehicle_type=vehicle_type)
  g.conn.execute(text(cmd_l), location_id = int(location_id),latitude=latitude,longitude =longitude,borough=borough,zip_code=int(zip_code),on_street_name=on_street_name,off_street_name=off_street_name)
  g.conn.execute(text(cmd_f), factor_id = int(factor_id),description=description)
  g.conn.execute(text(cmd_con), consequence_id = int(consequence_id),nperson_injured=int(nperson_injured),nperson_killed=int(nperson_killed),npedestrian_injured=int(npedestrian_injured),npedestrian_killed=int(npedestrian_killed),ncyclist_injured=int(ncyclist_injured),ncyclist_killed=int(ncyclist_killed),nmotorist_injured=int(nmotorist_injured),nmotorist_killed=int(nmotorist_killed))

  return redirect('/')



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
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()