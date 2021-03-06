#!/usr/bin/python3

# File: player_skeleton.py
# Date: Jan. 23, 2018
# Description: AI soccer skeleton algorithm
# Author(s): Luiz Felipe Vecchietti, Chansol Hong, Inbae Jeong
# Current Developer: Chansol Hong (cshong@rit.kaist.ac.kr)

from __future__ import print_function

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.serializer import MsgPackSerializer
from autobahn.wamp.types import ComponentConfig
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

import argparse

#reset_reason
NONE = 0
GAME_START = 1
SCORE_MYTEAM = 2
SCORE_OPPONENT = 3
GAME_END = 4
DEADLOCK = 5 # when the ball is stuck for 5 seconds

#coordinates
MY_TEAM = 0
OP_TEAM = 1
BALL = 2
X = 0
Y = 1
TH = 2

class Component(ApplicationSession):
    """
    AI Base + Skeleton
    """ 

    def __init__(self, config):
        ApplicationSession.__init__(self, config)

    def onConnect(self):
        print("Transport connected")
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

##############################################################################
        def init_variables(self, info):
            # Here you have the information of the game (virtual init())
            # List: game_time, goal, number_of_robots, penalty_area, codewords,
            #       robot_height, robot_radius, max_linear_velocity, field, team_info,
            #       {rating, name}, axle_length, resolution, ball_radius
            # self.game_time = info['game_time']
            # self.field = info['field']
            self.max_linear_velocity = info['max_linear_velocity']
            print("Initializing variables...")
            return
##############################################################################
            
        try:
            info = yield self.call(u'aiwc.get_info', args.key)
        except Exception as e:
            print("Error: {}".format(e))
        else:
            print("Got the game info successfully")
            try:
                self.sub = yield self.subscribe(self.on_event, args.key)
                print("Subscribed with subscription ID {}".format(self.sub.id))
            except Exception as e2:
                print("Error: {}".format(e2))
               
        init_variables(self, info)
        
        try:
            yield self.call(u'aiwc.ready', args.key)
        except Exception as e:
            print("Error: {}".format(e))
        else:
            print("I am ready for the game!")
            
            
    @inlineCallbacks
    def on_event(self, f):        
        #print("event received")

        @inlineCallbacks
        def set_wheel(self, robot_wheels):
            yield self.call(u'aiwc.set_speed', args.key, robot_wheels)
            return
        
        if 'reset_reason' in f: 
            if (f['reset_reason'] == GAME_START):
                print("Game started : " + str(f['time']))
            if (f['reset_reason'] == SCORE_MYTEAM):
                print("My team scored : " + str(f['time']))
            elif (f['reset_reason'] == SCORE_OPPONENT):
                print("Opponent scored : " + str(f['time']))
            if(f['reset_reason'] == GAME_END):
                print("Game ended.")

##############################################################################
                #(virtual finish())
                #save your data
                with open(args.datapath + '/result.txt', 'w') as output:
                    #output.write('yourvariables')
                    output.close()
                #unsubscribe; reset or leave  
                yield self.sub.unsubscribe()
                print("Unsubscribed...")
                try:
                    yield self.leave()
                except Exception as e:
                    print("Error: {}".format(e))
##############################################################################

        # If the optional coordinates are given
        #if 'coordinates' in f:
            # myteam = f['coordinates'][MY_TEAM]
            # opponent = f['coordinates'][OP_TEAM]
            # ball =  f['coordinates'][BALL]

            # myteam0_x = f['coordinates'][MY_TEAM][0][X]
            # myteam0_x = f['coordinates'][MY_TEAM][0][Y]
            # myteam0_x = f['coordinates'][MY_TEAM][0][TH]
        
        if 'EOF' in f:
            if (f['EOF']):
                #print("end of frame")

##############################################################################
                #(virtual update())
                wheels = [self.max_linear_velocity for _ in range(10)]
                set_wheel(self, wheels)
##############################################################################            

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip")
    parser.add_argument("port")
    parser.add_argument("realm")
    parser.add_argument("key")
    parser.add_argument("datapath")
    
    args = parser.parse_args()
    #print ("Arguments:")
    #print (args.server_ip)
    #print (args.port)
    #print (args.realm)
    #print (args.key)
    #print (args.datapath)
    
    ai_sv = "rs://" + args.server_ip + ":" + args.port
    ai_realm = args.realm
    
    # create a Wamp session object
    session = Component(ComponentConfig(ai_realm, {}))

    # initialize the msgpack serializer
    serializer = MsgPackSerializer()
    
    # use Wamp-over-rawsocket
    runner = ApplicationRunner(ai_sv, ai_realm, serializers=[serializer])
    
    runner.run(session, auto_reconnect=True)
