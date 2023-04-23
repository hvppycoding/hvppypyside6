from hvppypyside6.examples import systemtrayicon

def print_examples():
    print("=" * 33 + " Example List " + "=" * 33)
    print("1. System Tray Icon")
    print("=" * 80)
    print()

def main():
    print_examples()
    example = input("Enter example number: ")
    if example == "1":
        systemtrayicon.main()
    else:
        print("No example found.")