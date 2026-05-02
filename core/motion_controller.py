class MotionController:
    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode

        if not simulation_mode:
            from hardware.jetson_gpio import JetsonMotor
            self.motor = JetsonMotor()

    def forward(self):
        if self.simulation_mode:
            print("FORWARD")
        else:
            self.motor.forward()

    def backward(self):
        if self.simulation_mode:
            print("BACKWARD")
        else:
            self.motor.backward()

    def left(self):
        if self.simulation_mode:
            print("LEFT")
        else:
            self.motor.left()

    def right(self):
        if self.simulation_mode:
            print("RIGHT")
        else:
            self.motor.right()

    def stop(self):
        if self.simulation_mode:
            print("STOP")
        else:
            self.motor.stop()