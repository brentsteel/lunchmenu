"""
Simple Lunch Offer Menu - Python Learning Project
This script demonstrates variables, dictionaries, lists, and conditional logic
"""

# VARIABLES: Think of these as labeled boxes that store information
lunch_offer_price = 5.00  # A number variable (float for decimals)
regular_price_sandwich = 3.50
regular_price_crisps = 1.50
regular_price_snack = 2.00

# DICTIONARIES: Store items with their properties
# Format: {"item_name": price}
sandwiches = {
    "Ham & Cheese": 3.50,
    "Tuna Mayo": 3.50,
    "Chicken Salad": 3.50,
    "BLT": 3.50,
    "Egg Mayo": 3.50,
    "Cheese & Pickle": 3.50,
    "Chicken & Bacon": 4.50, # Premium item - doesn't qualify for offer
    "Prawn Mayo": 4.50,  # Premium item - doesn't qualify for offer
    "Steak & Onion": 4.50  # Premium item - doesn't qualify for offer
}

crisps = {
    "Ready Salted": 1.50,
    "Salt & Vinegar": 1.50,
    "Cheese & Onion": 1.50,
    "Prawn Cocktail": 1.50,
    "BBQ": 1.50,
    "Sour Cream": 1.50,
    "Paprika": 1.50,
    "Spicy Chili": 1.50,
    "Chilli and Lime Corn Chips": 1.50
}

snacks = {
    "Apple": 1.00,
    "Banana": 1.00,
    "Kit Kat": 2.00,
    "Granola Bar": 2.00,
    "Cookie": 1.50,
    "Mini Egg Brownie": 2.00,
    "Fruit Pot": 2.50,
    "Yogurt": 2.00,
    "Slice of homemade cake": 3.00 # Premium item - doesn't qualify for offer
}

# LISTS: Items that DON'T qualify for the lunch offer
# These are "premium" items
premium_sandwiches = ["Prawn Mayo", "Steak & Onion", "Chicken & Bacon", "Slice of homemade cake"]

# FUNCTION: A reusable block of code that performs a task
def display_menu(menu_dict, category_name):
    """Display a menu category with numbered options"""
    print(f"\n--- {category_name} ---")
    items = list(menu_dict.keys())  # Convert dictionary keys to a list
    for index, item in enumerate(items, 1):  # enumerate adds numbers starting at 1
        price = menu_dict[item]
        print(f"{index}. {item} - £{price:.2f}")
    return items  # Return the list so we can use it later


def get_user_choice(items, category_name):
    """Get and validate user's menu choice"""
    while True:  # Keep asking until we get valid input
        try:
            choice = int(input(f"\nSelect your {category_name} (enter number): "))
            if 1 <= choice <= len(items):
                return items[choice - 1]  # Return the item name (subtract 1 because lists start at 0)
            else:
                print(f"Please enter a number between 1 and {len(items)}")
        except ValueError:
            print("Please enter a valid number")


def check_offer_eligibility(sandwich_choice):
    """Check if the selected items qualify for the lunch offer"""
    # CONDITIONAL LOGIC: Make decisions based on conditions
    if sandwich_choice in premium_sandwiches:
        return False  # Premium sandwiches don't qualify
    else:
        return True  # Regular sandwiches qualify


def calculate_total(sandwich, crisp, snack, qualifies_for_offer):
    """Calculate the total price"""
    if qualifies_for_offer:
        return lunch_offer_price
    else:
        # Add up individual prices
        total = sandwiches[sandwich] + crisps[crisp] + snacks[snack]
        return total


# MAIN PROGRAM STARTS HERE
def main():
    """Main function that runs the lunch menu program"""
    print("=" * 50)
    print("Welcome to the Lunch Offer Menu!")
    print("=" * 50)
    print("\nLunch Offer: Any sandwich, crisps & snack for £5.00*")
    print("*Excludes premium sandwiches")
    
    # Display menus and get choices
    sandwich_items = display_menu(sandwiches, "SANDWICHES")
    sandwich_choice = get_user_choice(sandwich_items, "sandwich")
    
    crisp_items = display_menu(crisps, "CRISPS")
    crisp_choice = get_user_choice(crisp_items, "crisps")
    
    snack_items = display_menu(snacks, "SNACKS")
    snack_choice = get_user_choice(snack_items, "snack")
    
    # Check if order qualifies for offer
    qualifies = check_offer_eligibility(sandwich_choice)
    
    # Calculate total
    total = calculate_total(sandwich_choice, crisp_choice, snack_choice, qualifies)
    
    # Display order summary
    print("\n" + "=" * 50)
    print("YOUR ORDER")
    print("=" * 50)
    print(f"Sandwich: {sandwich_choice}")
    print(f"Crisps:   {crisp_choice}")
    print(f"Snack:    {snack_choice}")
    print("-" * 50)
    
    # CONDITIONAL OUTPUT: Different messages based on offer eligibility
    if qualifies:
        print("✓ LUNCH OFFER APPLIED!")
        print(f"Total: £{total:.2f}")
        savings = (sandwiches[sandwich_choice] + crisps[crisp_choice] + 
                  snacks[snack_choice]) - total
        print(f"You saved: £{savings:.2f}")
    else:
        print("✗ Does not qualify for lunch offer (premium sandwich selected)")
        print(f"Total: £{total:.2f}")
    
    print("=" * 50)


# This runs the program when you execute the script
if __name__ == "__main__":
    main()
