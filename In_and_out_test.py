### Current Implementation Analysis

The current implementation in `In_and_out_test.py` involves the following:

1. **Initialization**:
   - The variables `Pressure_switch`, `Pump_I`, `Pump_Low_I`, `Dry_Well`, `Pump_Min_I`, and `Well_Run` are initialized globally.

2. **Asynchronous Functions**:
   - `update_sensor_values()`: Updates sensor values.
   - `control_well_run()`: Controls the `Well_Run` based on `Pressure_switch` and `Dry_Well`.
   - `print_variables()`: Prints the values of the variables periodically.

3. **Task Creation Issue**:
   - Tasks are being created inside the loop, which is redundant and incorrect.

### Suggested Improvements

To handle multiple permissives for the pump run, we can introduce additional checks in the `control_well_run` function and encapsulate the logic in a more modular way.

Here is the improved code:

```python
import megabas as m
import time
import asyncio

class WellSystem:
    def __init__(self):
        # Initialize variables
        self.Pressure_switch = 0
        self.Pump_I = 0
        self.Pump_Low_I = 0
        self.Dry_Well = 0
        self.Pump_Min_I = 8
        self.Well_Run = 0

        # Set the BAS inputs and outputs
        self.Well_Run_output = m.setTriac(1, 1)
        self.Dry_Well_Lamp = m.setTriac(1, 2)
        self.Pressure_switch = m.getContactCh(1, 1)
        self.Pump_I = m.getUIn(1, 2)

        # Timer durations
        self.Input_Read_time = 1  # 1 Second
        self.print_variables_time = 5  # 5 Seconds

        # Permissives for pump run
        self.permissives = {
            "pressure_switch": lambda: self.Pressure_switch == 1,
            "dry_well": lambda: self.Dry_Well == 0,
            # Add more permissives as needed
        }

    async def update_sensor_values(self):
        while True:
            self.Pressure_switch = m.getContactCh(1, 1)  # Read from BAS DI 1
            self.Pump_I = m.getUIn(1, 2)  # Read from BAS AI 2
            await asyncio.sleep(self.Input_Read_time)

    async def control_well_run(self):
        while True:
            if all(check() for check in self.permissives.values()):
                m.setTriac(1, 1, 1)  # Turn on Well_Run
            else:
                m.setTriac(1, 1, 0)  # Turn off Well_Run
            await asyncio.sleep(self.Input_Read_time)

    async def print_variables(self):
        while True:
            print(f"Pressure_switch: {self.Pressure_switch}, Pump_I: {self.Pump_I}")
            await asyncio.sleep(self.print_variables_time)

    async def run(self):
        await asyncio.gather(
            self.update_sensor_values(),
            self.control_well_run(),
            self.print_variables()
        )

if __name__ == "__main__":
    well_system = WellSystem()
    asyncio.run(well_system.run())
```

### Key Changes

- Introduced a `WellSystem` class to encapsulate variables and methods.
- Added a permissives dictionary to store and check pump run conditions.
- Cleaned up task creation to ensure tasks are managed correctly.
- Improved readability and maintainability of the code.

This approach ensures that all pump run permissives are checked collectively, making it easier to add or modify permissive conditions in the future.
