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
print_variables_time = int(5)  # 5 Seconds

# Set the BAS inputs and outputs
global Pressure_switch, Pump_I, Pump_Low_I, Dry_Well, Pump_Min_I, Well_Run
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
    while True:
        global Pressure_switch, Pump_I 
        Pressure_switch = m.getContactCh(1,1)  # Read from BAS DI 1
        Pump_I = m.getUIn(1,2)            # Read from BAS AI 2
        await asyncio.sleep(Input_Read_time())
        # Start the sensor update task
        asyncio.create_task(update_sensor_values())

async def control_well_run():
    while True:
        if Pressure_switch == 1 and Dry_Well == 0:
            m.setTriac(1, 1, 1)  # Turn on Well_Run
        else:
            m.setTriac(1, 1, 0)  # Turn off Well_Run
        await asyncio.sleep(Input_Read_time)
        asyncio.create_task(control_well_run())

async def print_variables():
    while True:
        print(f"Pressure_switch: {Pressure_switch}, Pump_I: {Pump_I}")
        await asyncio.sleep(print_variables_time)
        print("pressure switch:", Pressure_switch)
        print("pump current:", Pump_I)
        asyncio.create_task(print_variables())
