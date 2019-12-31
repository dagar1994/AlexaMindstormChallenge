print("Started")
import logging
import sys
from datetime import *
import time
import threading
import random
print("Started1 before agt")
from agt import AlexaGadget
print("Started2 after agt")
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_C, OUTPUT_B, OUTPUT_D, LargeMotor, MediumMotor, SpeedDPS
from ev3dev2.sound import Sound
import json


#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
ts = TouchSensor()

class KitchenSinkGadget(AlexaGadget):
    """
    Class that logs each directive received from the Echo device.
    """
    def __init__(self):
        
        super().__init__()
        self.leds = Leds()
        self.motorOne = LargeMotor(OUTPUT_C)
        self.motorTwo = LargeMotor(OUTPUT_B)
        self.motorThree = MediumMotor(OUTPUT_A)
        #self.t1 = ""
        #self.t2 = ""
        #self.TouchIt = TouchSensor(INPUT_4)
        #ts = TouchSensor()



    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        self.leds.set_color('LEFT','RED')
        self.leds.set_color('RIGHT','RED')
        threading.Thread(target=self.buttonListener).start()


    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        self.leds.set_color('LEFT','BLACK')
        self.leds.set_color('RIGHT','BLACK')

    def on_alexa_gadget_statelistener_stateupdate(self, directive):
        """
        Alexa.Gadget.StateListener StateUpdate directive received.
        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alexa-gadget-statelistener-interface.html#StateUpdate-directive
        :param directive: Protocol Buffer Message that was send by Echo device.
        To get the specific state update name, the following code snippet can be used:
        # Extract first available state (name & value) from directive payload
        """
        if len(directive.payload.states) > 0:
            state = directive.payload.states[0]
            name = state.name
            value = state.value
            print('state name:{}, state value:{}'.format(name, value))
            if name == "timers":
                if value == "active":
                    print("Active hai timer abhi")
                    self.motorThree.on(20)
                    #self.motorOne.on_for_degrees(speed = 10, degrees= 90)
                    #self.motorTwo.on_for_degrees(10,-90)
                elif value == "cleared":
                    print("Timer cleared here now")
                    self.motorThree.off()
                    #self.motorThree.on_to_position(10,0)

                    #for i in range(12,168):
                    #self.motorOne.on_to_position(2,0)
                    #self.motorTwo.on_to_position(2,0)
            elif name == "wakeword":
                actualPos = self.motorOne.position
                print(actualPos)
                #self.motorOne.on_to_position(10,0)
                if value == "active":
                    self.leds.set_color('LEFT','GREEN')
                    self.leds.set_color('RIGHT','GREEN')
                    self.motorOne.on_to_position(10,-10,True,True)
                    self.motorOne.wait_until_not_moving()
                    self.motorOne.on_to_position(10,0,True,True)
                    self.motorOne.on_to_position(10,10,True,True)
                    self.motorOne.on_to_position(10,0,True,True)
                elif value == "cleared":
                    self.leds.set_color('LEFT','BLACK')
                    self.leds.set_color('RIGHT','BLACK')
                    #self.motorOne.on_to_position(20,0)

            elif name == "alarms":
                if value == "active":
                    self.leds.set_color('LEFT','RED')
                    self.leds.set_color('RIGHT','RED')
                    self.motorThree.on(20)
                elif value == "cleared":
                    self.motorThree.stop()
                    self.leds.set_color('LEFT','BLACK')
                    self.leds.set_color('RIGHT','BLACK')

            elif name == "reminders":
                if value == "active":
                   self.leds.set_color('LEFT','GREEN')
                   self.leds.set_color('RIGHT','GREEN')
                   #self.leds.set_color('UP','GREEN')
                   #self.leds.set_color('DOWN','GREEN')
                   moveUp = True
                   moveDown = True
                   counter = 0
                   for i in range(0,15):                       
                      #if moveUp:
                      self.motorTwo.on_to_position(10,-10,True,True)
                      self.motorThree.on_to_position(5,-20,True,True)
                      time.sleep(0.3)
                      self.motorTwo.on_to_position(10,70,True,True)
                      #moveUp = False
                      #moveDown = True
                      #elif moveDown:
                      #    self.motorTwo.on_for_degrees(20,0,True,True)
                      #    moveUp = True
                      #    moveDown = False
                        
                elif value == "cleared":
                    self.leds.set_color('LEFT','BLACK')
                    self.leds.set_color('RIGHT','BLACK')
                    self.motorTwo.on_to_position(20,0)
                    self.motorThree.on_to_position(5,70,True,True)
                    #self.leds.set_color('UP','BLACK')
                    #self.leds.set_color('DOWN','BLACK')     
               
                  
    def on_notifications_setindicator(self, directive):
        """
        Notifications SetIndicator directive received.
        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/notifications-interface.html#SetIndicator-directive
        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        print("Notification Set Indicator")

    def on_notifications_clearindicator(self, directive):
        """
        Notifications ClearIndicator directive received.
        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/notifications-interface.html#ClearIndicator-directive
        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        print("Notification Cleared")


    def on_alexa_gadget_musicdata_tempo(self, directive):
        """
        Provides the music tempo of the song currently playing on the Echo device.
        :param directive: the music data directive containing the beat per minute value
        """
        tempo_data = directive.payload.tempoData
        for tempo in tempo_data:

            print("tempo value: {}".format(tempo.value))
            if tempo.value > 0:
                # dance pose
                print(tempo.value)
                #self.right_motor.run_timed(speed_sp=750, time_sp=2500)
                #self.left_motor.run_timed(speed_sp=-750, time_sp=2500)
                #self.hand_motor.run_timed(speed_sp=750, time_sp=2500)
                self.leds.set_color("LEFT", "GREEN")
                self.leds.set_color("RIGHT", "GREEN")
                time.sleep(3)
                # starts the dance loop
                self.trigger_bpm = "on"
                self.t1 = threading.Thread(target=self._dance_loop, args=(tempo.value,)).start()
                self.t2 = threading.Thread(target=self.ledShuffler, args=(tempo.value,)).start()

            elif tempo.value == 0:
                # stops the dance loop
                #print(dir(self.t1))

                self.trigger_bpm = "off"
                self.motorOne.on_to_position(5,0,True,True)
                self.leds.set_color("LEFT", "BLACK")
                self.leds.set_color("RIGHT", "BLACK")




    def danceMoveTwo(self):
        for i in range(0,2):
            self.motorThree.on_for_rotations(15,1,True,False)
            self.motorTwo.on_to_position(15,-30,True,True)
            self.motorOne.on_to_position(5,0,True,True)
            self.motorThree.on_for_rotations(15,1,True,False)
            self.motorTwo.on_to_position(15,45,True,True)
            self.motorOne.on_to_position(5,-60,True,True)
            self.motorThree.on_for_rotations(15,1,True,True)
            self.motorOne.on_to_position(5,0,True,True)
            self.motorThree.on_for_rotations(15,1,True,True)
            self.motorOne.on_to_position(5,60,True,True)
            self.motorThree.on_for_rotations(15,1,True,True)
            self.motorOne.on_to_position(5,0,True,True)


    def danceMoveFive(self):
        for i in range(0,4):
            print("Move five part one")
            print(self.motorTwo.position)
            self.motorTwo.on_to_position(15,-30,True,False)
            #self.motorTwo.wait_until_not_moving()            
            self.motorTwo.on_to_position(20,40,True,False)
            self.motorOne.on_to_position(5,0,True,True)
            self.motorOne.on_to_position(5,60,True,False)        
        
        #for i in range(0,4):
        #    print("Move five part two")
        #    print(self.motorThree.position)
        #    self.motorThree.on_to_position(15,70,True,True)
        #    self.motorOne.on_to_position(5,-60,True,True)
        #    self.motorThree.on_to_position(15,130,True,False)
        #    self.motorOne.on_to_position(5,-60,True,False)

    def danceMoveSix(self):
        for i in range(0,12):
            if self.trigger_bpm != 'on':
                return
            moveUp = True
            moveDown = True

            if moveUp:
                print("Move Six Part One")
                print(self.motorThree.position)
                #self.leds.set_color('LEFT','RED')
                #self.leds.set_color('RIGHT','RED')
                self.motorThree.on_to_position(10,0,True,True)
                self.motorThree.on_to_position(10,70,True,False)
                moveUp = False
                moveDown = True


            if moveDown:
                print("Move Six Part Two")
                #self.leds.set_color('LEFT','GREEN')
                #self.leds.set_color('RIGHT','GREEN')
                print(self.motorTwo.position)
                self.motorTwo.on_to_position(15,-30,True,True)
                self.motorTwo.on_to_position(15,45,True,False)
                moveUp = True
                moveDown = False
            #self.motorTwo.on_to_position(20,-20,True,True)            
            #self.motorOne.on_to_position(5,60,True,False)
            #self.motorTwo.on_to_position(20,20,True,True)
            self.motorOne.on_to_position(5,60,True,True)
            self.motorOne.on_to_position(1,0,True,True)
        


    
    def moveSeven(self):
        start = 0
        for each in range(0,50):
            if self.trigger_bpm != 'on':
                return
            start += 5
            self.motorThree.on_to_position(1,start,True,True)
            time.sleep(0.2)
    
    def moveHands(self):
        self.motorThree.on_to_position(15,30,True,False)
        self.motorTwo.on_to_position(20,0,True,True)

        self.motorThree.on_to_position(15,-30,True,False)
        self.motorTwo.on_to_position(20,55,True,True)


    def moveHands2(self):
        self.motorThree.on_to_position(10,-120,True,False)
        self.motorTwo.on_to_position(15,-10,True,True)
        self.motorThree.on_to_position(10,-50,True,False)
        self.motorTwo.on_to_position(15,45,True,True)

    def danceMoveFour(self):

        if self.trigger_bpm != 'on':
            return
        self.motorOne.on_to_position(8,0,True,True)
        for i in range(0,4):
            print("In move four part one")
            self.moveHands()
        self.motorOne.on_to_position(8,-40,True,True)
        if self.trigger_bpm != 'on':
            return
        for i in range(0,4):
            print("In move four part two")
            self.moveHands()
        self.motorOne.on_to_position(8,0,True,True)
        if self.trigger_bpm != 'on':
            return
        for i in range(0,4):
            print("In move four part three")
            self.moveHands()
        self.motorOne.on_to_position(8,40,True,True)
        if self.trigger_bpm != 'on':
            return
        for i in range(0,4):
            print("In move four part four")
            self.moveHands2()
        self.motorOne.on_to_position(8,0,True,True)
        if self.trigger_bpm != 'on':
            return
        for i in range(0,4):
            print("In move four part five")
            self.moveHands2()





    def danceMoveThree(self):
        self.motorOne.on_to_position(5,0,True,False)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorOne.on_to_position(5,-40,True,False)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorOne.on_to_position(5,0,True,False)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorOne.on_to_position(5,40,True,False)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        self.motorTwo.on_to_position(20,-30,True,True)
        self.motorTwo.on_to_position(20,45,True,True)
        


    def danceMoveOne(self):
        self.motorTwo.on_to_position(20,-30,True,False)
        self.motorOne.on_to_position(5,0,True,True)
        self.motorTwo.on_to_position(20,45,True,False)
        self.motorOne.on_to_position(5,-60,True,True)
        self.motorTwo.on_to_position(20,-30,True,False)
        self.motorOne.on_to_position(5,0,True,True)
        self.motorTwo.on_to_position(20,45,True,False)
        self.motorOne.on_to_position(5,60,True,True)
        self.motorTwo.on_to_position(20,-30,True,False)
    
    def buttonListener(self):
        while True:
            if ts.is_pressed:
                print("Button Pressed")
                self._send_event("buttonPress" ,{"pressed" : "pressedNow"})
            else:
                pass
            time.sleep(0.2)
            
    def ledShuffler(self,bpm):
        color_list = ["GREEN", "RED", "AMBER", "YELLOW"]
        led_color = random.choice(color_list)
        while self.trigger_bpm == "on":
            led_color = "BLACK" if led_color != "BLACK" else random.choice(color_list)
            self.leds.set_color("LEFT", led_color)    
            self.leds.set_color("RIGHT", led_color)
            milli_per_beat = min(1000, (round(60000 / bpm)) * 0.65)
            time.sleep(milli_per_beat / 1000)



    def _dance_loop(self, bpm):
        """
        Perform motor movement in sync with the beat per minute value from tempo data.
        :param bpm: beat per minute from AGT
        """
        motor_speed = 400
        milli_per_beat = min(1000, (round(60000 / bpm)) * 0.65)
        print("Adjusted milli_per_beat: {}".format(milli_per_beat))
        while self.trigger_bpm == "on":

            # Alternate led color and motor direction
            motor_speed = -motor_speed
            #self.danceMoveFive()
            #self.danceMoveSix()
            #self.danceMoveOne()
            #self.danceMoveTwo()
            #self.danceMoveThree()
            if self.trigger_bpm != "on":
                break
            self.danceMoveFour()

            if self.trigger_bpm != "on":
                break
            self.danceMoveFive()

            if self.trigger_bpm != "on":
                break
            self.danceMoveSix()

            if self.trigger_bpm != "on":
                break
            self.moveSeven()

            if self.trigger_bpm != "on":
                break

            #self.right_motor.run_timed(speed_sp=motor_speed, time_sp=150)
            #self.left_motor.run_timed(speed_sp=-motor_speed, time_sp=150)

            time.sleep(milli_per_beat / 1000)

        print("Exiting BPM process.")
        self.motorTwo.on_to_position(5,75,True,True)
        self.motorThree.on_to_position(5,75,True,True)
        self.motorOne.on_to_position(5,0,True,True)

    def _send_event(self, name, payload):
        """
        Sends a custom event to trigger a sentry action.
        :param name: the name of the custom event
        :param payload: the sentry JSON payload
        """
        self.send_custom_event('Custom.Mindstorms.Gadget', name, payload)

    def on_custom_mindstorms_gadget_control(self, directive):
        """
        Handles the Custom.Mindstorms.Gadget control directive.
        :param directive: the custom directive with the matching namespace and name
        """
        print("Directive", directive)
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload))
            control_type = payload["type"]
            print("Control Type",control_type)
            if control_type == "dance":
                print("Move command found")
                self.danceMoveFive()
                self._send_event("completion", {'danceMove' : 'completed'})
            elif control_type == "rotate":
                self.motorOne.on_to_position(5,190,True,True)
                self.motorOne.on_to_position(5,-150,True,True)
                self.motorTwo.on_to_position(10,-30,True,True)
                self.motorThree.on_to_position(5,-20,True,True)
                time.sleep(1)
                #self.motorTwo.on_to_position(5,40,True,True)
                #time.sleep(2)
                #self.motorOne.on_to_position(5,0,True,True)
                self._send_event("completion",{'startGame':'completed'})
            elif control_type == "movefinger" :
                time.sleep(1.4)
                print("Delay 1.4")
                self.motorTwo.on_to_position(15,-20,True,True)
                self.motorTwo.on_to_position(15,40,True,True)
                #while not ts.is_pressed:
                #    print("Touch Sensor is not pressed")
                    #self._send_event("completion",{'flying':'made'})
                #self._send_event("completion",{'flying':'completed'})
            elif control_type == "movefingeragain":
                time.sleep(1.2)
                print("Delay 1.2")
                self.motorTwo.on_to_position(15,-20,True,True)
                self.motorTwo.on_to_position(15,40,True,True)
            elif control_type == "movefingerfirst":
                time.sleep(0.3)
                print("Delay 0.3")
                self.motorTwo.on_to_position(15,-20,True,True)
                self.motorTwo.on_to_position(15,40,True,True)
            elif control_type == "chill":
                self.motorOne.on_to_position(5,20,True,True)
                self.motorTwo.on_to_position(5,55,True,True)
                self.motorThree.on_to_position(5,40,True,True)
                #self._send_event("completion",{'backtoPos':'completed'})
            elif control_type == "rotatetwo":
                self.motorOne.on_to_position(5,190,True,True)
                self.motorOne.on_to_position(5,-150,True,True)
                self.motorOne.on_to_position(5,20,True,True)
                time.sleep(0.5)
                self.motorTwo.on_to_position(10,-40,True,True)
                self.motorThree.on_to_position(5,-30,True,True)
                self._send_event("completion",{'playerturn':'completed'})
            elif control_type == "startdance":
                print("Robot should be dancing now")
                time.sleep(4)
                self.trigger_bpm = "on"
                self.danceMoveFour()
                self.danceMoveFive()
                self._send_event("completion",{'dance' : 'statue'})
        except KeyError:
            print("Missing expected parameters: {}".format(directive))



    def on_alerts_setalert(self, directive):
        """
        Alerts SetAlert directive received.
        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alerts-interface.html#SetAlert-directive
        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        print(directive.payload)
        #for state in directive.payload.states:
        if directive.payload.type == "TIMER":
            timeToStart = directive.payload.scheduledTime
            token = directive.payload.token
            timeNow = datetime.now()
            print(timeNow)
            #for i in range(12,168):
            self.motorTwo.on_to_position(25,120)
            self.motorTwo.on_to_position(25,0)
                #self.motorTwo.on_to_position(-1,i)
                #time.sleep(1.935)
                #print(i)
                #print("Motor is holding")
                #print(self.motorOne.is_holding)
                #print("Motor is running")
                #print(self.motorOne.is_running)
                #print("Motor is stalled")
                #print(self.motorOne.is_stalled)
            print("Set Alert is done")
        
        elif directive.payload.type == "ALARM":
            timeToStart = directive.payload.scheduledTime
            token = directive.payload.token
            print(timeToStart)
            print(token)
            self.leds.set_color('LEFT','YELLOW')
            self.leds.set_color('RIGHT','YELLOW')

        elif directive.payload.type == "REMINDER":
            self.leds.set_color('LEFT','AMBER')
            self.leds.set_color('RIGHT','AMBER')
            #self.leds.set_color('UP','AMBER')
            #self.leds.set_color('DOWN','AMBER')


    def on_alerts_deletealert(self, directive):
        """
        Alerts DeleteAlert directive received.
        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alerts-interface.html#DeleteAlert-directive
        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        print(directive.payload)
        #for state in directive.payload.states:
        #    if state.value == "cleared":
        #           self.motorTwo.run_timed(speed_sp=1000,time_sp=1000)
        print("Delete Alert")


if __name__ == '__main__':
    KitchenSinkGadget().main()
