import sys
import socket

from .SamModule import SamModule

class CameraProcessing(SamModule):

    is_following_lane = False
    waiting_for_green = False

    previous = 0

    # Tune pd: https://robotics.stackexchange.com/questions/167/what-are-good-strategies-for-tuning-pid-loops
    # https://robotic-controls.com/learn/programming/pd-feedback-control-introduction

    # Get there faster => Smaller Kp
    # Less Overshoot => Smaller Kp, larger Kd
    # Less Vibration => Larger Kd

    # Kp => Increase to make larger corrections
    # Kd => Increase to make damping greater
    Kp = 0.01547 #0.01547
    Kd = 0.0123  #0.0123

    def __init__(self, kargs):
        super().__init__(module_name="CameraProcessing", is_local=True, identi="camera", **kargs)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 5005))

        self.sam.listening_to[sock] = self._process_socket

    def _process_socket(self, soc):
        data = soc.recv(1024)
        if data:
            self.message_received(data.decode("utf-8", 'ignore').strip())

    def stdin_request(self, message):
        if message == "go":
            self.is_following_lane = True

        elif message == "stop":
            self.is_following_lane = False

    def message_received(self, message):
        if self.waiting_for_green:                          # we got to a red line, and now waiting for green.
            msg_parts = message.strip().split(" ")
            if len(msg_parts) != 4:
                self.debug_run(self.write_to_stdout, "4 ")

            try:
                center = int(msg_parts[0])
                mid = int(msg_parts[1])
                command = msg_parts[2]
                ratio = int(msg_parts[3])
            except ValueError:
                self.debug_run(self.write_to_stdout, "Something in this was not the correct type: " + message)
                return

            if command == "green":
                self.waiting_for_green = False
                self.sam['camera'].message_received("ready")    # Tells map module we can move to next state

        if self.is_following_lane:                              # If we are in the state of following a lane...

            msg_parts = message.strip().split(" ")
            if len(msg_parts) != 4:
                self.debug_run(self.write_to_stdout, "4 ")
            try:
                center = int(msg_parts[0])
                mid = int(msg_parts[1])
                command = msg_parts[2]
                ratio = int(msg_parts[3])
            except ValueError:
                self.debug_run(self.write_to_stdout, "Something in this was not the correct type: " + message)
                return

            center = 617 #620
            diff = center - mid

            output = -(self.Kp * diff) - (self.Kd * (diff-self.previous))

            # Hit read line:
            if command == 'stop':
                self.debug_run(self.write_to_stdout, 'Stop')
                self.sam['motor'].stdin_request('stop')
                self.is_following_lane = False
                self.waiting_for_green = True                   # Following lanes always end in red,
                                                                # so we stop following lane and wait for green
                return

            self.debug_run(self.write_to_stdout, "Output is: " + str(output))

            # speed(ml + output, mr - output)
            ml, mr = self.sam['motor'].current_speed
            self.sam['motor'].stdin_request("turn " + str(ml+output) + " " + str(mr - output))

            self.previous = diff

