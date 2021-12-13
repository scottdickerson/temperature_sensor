from sense_hat import SenseHat
from emailUtilities import sendEmailTemperatureWarning, check_for_new_control_messages
from datetime import date

sense = SenseHat()
lastEmailSendDate = None
desired_temperature = 60
desired_humidity = 50
state = "RUNNING"

def update_settings():
    new_temperature, new_humidity, action = check_for_new_control_messages()
    global desired_temperature, desired_humidity, state
    
    if new_temperature != None:
        desired_temperature = new_temperature
        print("updating temperature: %s" % new_temperature)
    if new_humidity != None:
        desired_humidity = new_humidity
        print("updating humidity: %s" % new_humidity)
    if action == "START":
        state = "RUNNING"
        print("new state: RUNNING")
    if action == "STOP":
        state = "STOPPED"
        print("new state STOPPED")

while True:
    if state == "RUNNING":
        try:
            temperature = round(sense.get_temperature() * 9/5 + 32) 
            humidity = round(sense.get_humidity())
            today = date.today().strftime("%d/%m/%Y")
            print("todays date %s" % today)
            
            temperatureMessage = "Temp:%sF" % temperature
            humidityMessage = "Hum:%s%%\n" % humidity
            
            print(temperatureMessage)
            print(humidityMessage)
            
            update_settings()
            
            print("desired temperature %s desired_humidity %s" % (desired_temperature, desired_humidity))
            isTemperatureTooLow = temperature < desired_temperature
            isHumidityTooHigh = humidity > desired_humidity

            sense.show_message(text_string=temperatureMessage, text_colour=[255,0,0] if isTemperatureTooLow else [0,255,0])
            sense.show_message(text_string=humidityMessage, text_colour=[255, 0, 0] if isHumidityTooHigh else [0,255,0])
            
            if (isTemperatureTooLow or isHumidityTooHigh): # and lastEmailSendDate != today:
               sendEmailTemperatureWarning(temperature = temperature, desired_temperature=desired_temperature, humidity=humidity, desired_humidity=desired_humidity)
               lastEmailSendDate = today
        except BaseException as err:
           sense.show_message(text_string="Error with sensor")
           print("something went wrong getting temperature", err)
    else:
        sense.show_message(text_string="STOPPED")
        # Do I need to restart?
        update_settings()