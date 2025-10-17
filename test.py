items: dict[str, str | int] = {}
while True:
    print(""" 
1. Add Item
2. Remove Item
3. Update Quantity
4. Display Inventory
5. Exit
 """)
    user_input = int(input("\nSelect the above options"))

    match user_input:
        case 1:
            item_name = input("Enter item name")
            quantity = int(input("Enter quantity in numbers"))
            items["name"] = item_name
            items["quantity"] = quantity
            ...
        case 2:
           ...
        case 3:
            ...
        case 4:
             print(items)
        case 5:
            break
        case _:
            print("You Choose invalid")
            break
