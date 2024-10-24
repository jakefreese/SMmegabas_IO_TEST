import megabas as m
import time
import asyncio

def setTriac(output, relay, state):
    # Placeholder function to control the triac output
    print(f"Setting Triac: output={output}, relay={relay}, state={state}")

# timer durations
Pump_Low_I_time = int(30) # 30 Seconds
Dry_Well_Time = int(900)  # 900 Seconds 15min
Input_Read_time = int(1)  # 1 Second

# Set the BAS inputs and outputs
Well_Run_output = m.setTriac(1,1)            # BAS Traic 1
Dry_Well_Lamp = m.setTriac(1,2)     # BAS Triac 2
Pressure_switch = m.getContactCh(1,1)  # BAS DI 1
Pump_I = m.getUIn(1,2)          # BAS AI 2 

# Variables
Pump_Low_I = 0          # Initialize Pump_Low_I
Dry_Well = 0            # Initialize Dry_Well
Pump_Min_I = 8          # Initialize Pump_Min_I 8 Amps minimum current
Well_Run = 0            # Initialize Well_Run

async def update_sensor_values():
    global Pressure_switch, Pump_I
    while True:
        Pressure_switch = m.getContactCh(1,1)  # Read from BAS DI 1
        Pump_I = m.getUIn(1,2)            # Read from BAS AI 2
        await asyncio.sleep(Input_Read_time())
        # Start the sensor update task
        asyncio.create_task(update_sensor_values())
