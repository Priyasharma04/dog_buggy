import Jetson.GPIO as GPIO

class JetsonMotor:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        self.IN1, self.IN2 = 33, 35
        self.IN3, self.IN4 = 37, 38

        for p in [self.IN1, self.IN2, self.IN3, self.IN4]:
            GPIO.setup(p, GPIO.OUT)

    def forward(self):
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 1)
        GPIO.output(self.IN4, 0)

    def backward(self):
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 1)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 1)

    def left(self):
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 1)
        GPIO.output(self.IN3, 1)
        GPIO.output(self.IN4, 0)

    def right(self):
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 1)

    def stop(self):
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 0)