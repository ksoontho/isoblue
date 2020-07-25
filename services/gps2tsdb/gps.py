#!/usr/bin/python3
print("Hello")
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import postgres

def fix(*args):
    #print(args)
    print("Time: ", args[0], "\tLat: ", args[3], "\tLng: ", args[4])
    print("Inserting lat and lng for timestanp ", args[0])
    db.run("INSERT INTO gps (time, lat, lng) VALUES (to_timestamp(%s), %s, %s)", (float(args[0]), float(args[3]), float(args[4]) ) )
    print("Finsihed inserting lat and lng for timestamp ", args[0])


print("Initing db var")
global db 
print("Initing Postgres obj")
db = postgres.Postgres(url='postgresql://avena:password@postgres/avena')
print("finished initing Postgres obj: ", db)

print("Ensuring timescaledb extension is activated")
db.run("CREATE EXTENSION IF NOT EXISTS timescaledb;")
print("Ensuring tables are setup properly")
db.run("""
        CREATE TABLE IF NOT EXISTS gps (
          time timestamptz UNIQUE NOT NULL,
          lat double precision NOT NULL,
          lng double precision NOT NULL);""")
print("Ensuring GPS point table is a timescaledb hypertable")
db.run("SELECT create_hypertable('gps', 'time', if_not_exists => TRUE, migrate_data => TRUE);")
print("Finished settting up tables")


DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
bus.add_signal_receiver(fix, signal_name='fix', dbus_interface="org.gpsd")

loop = GLib.MainLoop()
loop.run()
