temperature: float = float(input("Enter temperature in : "))
unit: str = input("Enter unit (C for Celsius, F for Fahrenheit): ")

if unit.upper() == 'C':
    converted_temp = (temperature * 9/5) + 32
    print(f"{temperature}°C is {converted_temp}°F")
elif unit.upper() == 'F':
    converted_temp = (temperature - 32) * 5/9
    print(f"{temperature}°F is {converted_temp}°C")
else:
    print("Invalid unit. Please enter 'C' or 'F'.")