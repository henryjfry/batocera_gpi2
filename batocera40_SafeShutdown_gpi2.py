
import RPi.GPIO as GPIO
import os
import time
from multiprocessing import Process

#initialize pins
#powerPin = 3 #pin 5
#ledPin = 14 #TXD
#resetPin = 2 #pin 13
#powerenPin = 4 #pin 5

powerPin = 26
powerenPin = 27
hdmiPin = 18

# initialize GPIO settings
def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(powerPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(hdmiPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(powerenPin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(powerenPin, GPIO.HIGH)

def file_matching_lines(filename, txt):
        results = []
        with open(filename) as f:
                for each_result in [line for line in f if txt in line]:
                        results.append(each_result)
        return results

#waits for user to hold button up to 1 second before issuing poweroff command
def poweroff():
        while True:
                #self.assertEqual(GPIO.input(powerPin), GPIO.LOW)
                #GPIO.wait_for_edge(powerPin, GPIO.FALLING)
                #start = time.time()
                print(powerPin)
                print(GPIO.input(powerPin))
                while GPIO.input(powerPin) == GPIO.HIGH:
                        time.sleep(0.5)
                os.system("batocera-es-swissknife --emukill")
                time.sleep(1)
                #os.system("shutdown -h now")
                os.system("poweroff")


def lcdrun_first():
        hdmi_test = GPIO.input(18)
        print(hdmi_test)
        if hdmi_test == 1:
                hdmi_test = 'hdmi'
                print(hdmi_test)
                if len(file_matching_lines('/boot/config.txt', 'enable_dpi_lcd=1')) > 0:
                        os.system('mount -o remount, rw /boot')
                        os.system('mount -o remount, rw /')
                        os.system('rm -f /boot/config_lcd.txt')
                        os.system('cp -f "/boot/config.txt" "/boot/config_lcd.txt"')
                        os.system('rm -f /boot/config.txt')
                        os.system('cp -f "/boot/config_hdmi.txt" "/boot/config.txt"')
                        os.system('rm -f /boot/config.txt')
                        os.system('cp -f "/boot/config_hdmi.txt" "/boot/config.txt"')
                        os.system('batocera-audio set alsa_output._sys_devices_platform_soc_fef00700.hdmi_sound_card0.hdmi-stereo')
                        os.system('shutdown -r now ')
                        os.system('sleep 10')
        else:
                hdmi_test = 'lcd'
                print(hdmi_test)
                if len(file_matching_lines('/boot/config.txt', 'enable_dpi_lcd=1')) == 0:
                        os.system('mount -o remount, rw /boot')
                        os.system('mount -o remount, rw /')
                        os.system('rm -f /boot/config_hdmi.txt')
                        os.system('cp -f "/boot/config.txt" "/boot/config_hdmi.txt"')
                        os.system('rm -f /boot/config.txt')
                        os.system('cp -f "/boot/config_lcd.txt" "/boot/config.txt"')
                        os.system('batocera-audio set alsa_output.usb-GeneralPlus_USB_Audio_Device-00.analog-stereo')
                        os.system('shutdown -r now')
                        os.system('sleep 10')

def lcdrun_next():
        hdmi_test = GPIO.input(18)
        if hdmi_test == 1:
                hdmi_test = 'hdmi'
                if len(file_matching_lines('/boot/config.txt', 'enable_dpi_lcd=1')) > 0:
                        os.system('mount -o remount, rw /boot')
                        os.system('mount -o remount, rw /')
                        os.system('rm -f /boot/config_lcd.txt')
                        os.system('cp -f "/boot/config.txt" "/boot/config_lcd.txt"')
                        os.system('rm -f /boot/config.txt')
                        os.system('cp -f "/boot/config_hdmi.txt" "/boot/config.txt"')
                while GPIO.input(18) == 1:
                        time.sleep(0.5)
        else:
                hdmi_test = 'lcd'
                if len(file_matching_lines('/boot/config.txt', 'enable_dpi_lcd=1')) == 0:
                        os.system('mount -o remount, rw /boot')
                        os.system('mount -o remount, rw /')
                        os.system('rm -f /boot/config_hdmi.txt')
                        os.system('cp -f "/boot/config.txt" "/boot/config_hdmi.txt"')
                        os.system('rm -f /boot/config.txt')
                        os.system('cp -f "/boot/config_lcd.txt" "/boot/config.txt"')
                while GPIO.input(18) == 0:
                        time.sleep(0.5)

def lcdrun():
        while True:
                lcdrun_next()
                time.sleep(1)

if __name__ == "__main__":
        #initialize GPIO settings
        init()
        lcdrun_first()
        #create a multiprocessing.Process instance for each function to enable parallelism
        powerProcess = Process(target = poweroff)
        powerProcess.start()
        lcdrunProcess = Process(target = lcdrun)
        lcdrunProcess.start()

        powerProcess.join()
        lcdrunProcess.join()

        GPIO.cleanup()

