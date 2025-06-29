def kg_to_lbs(kg):
    return kg * 2.20462

def main():
    try:
        kg = float(input("Enter weight in kilograms: "))
        lbs = kg_to_lbs(kg)
        print(f"{kg} kg is equal to {lbs:.2f} lbs.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()