import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO_TRIG = 23
GPIO_ECHO = 22
Buzzer = 18

GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(Buzzer, GPIO.OUT)

GPIO.output(Buzzer, True)
buzzerpin = GPIO.PWM(Buzzer, 0.25)
buzzerpin.start(1)
print("PWM setup begins")

def beep_frequency(dist):
    if dist > 50:
        return 2
    elif dist <=50 and dist >=30:
        return 3
    elif dist < 30 and dist >=20:
        return 4
    elif dist < 20 and dist >= 10:
        return 5
    elif dist < 10:
        return 6
    else:
        return 0.25
 
def distance():
    print("Measuring distance")
    GPIO.output(GPIO_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
        
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
        
    measured_time = stop_time - start_time
    distance_both_ways = measured_time * 34300
    distance = distance_both_ways / 2
    
    print("Completed")
    return distance

if __name__ == "__main__":
    print("Running")
    try:
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            freq = beep_frequency(dist)
            buzzerpin.ChangeFrequency(freq)
            time.sleep(1)
                
    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()
        buzzerpin.stop()
            