from os import system, name
import ga


def menu():
    """Print a welcome message to the user, with instructions."""
    clear()
    print("Timetable Maker\nPlease ensure that config.json is filled in \
        correctly\nType start to create a timetable with output to a text \
            file, or type help for more commands")
    get_user_input()


def clear():
    """Clear the terminal display."""
    if name == "nt":  # Windows
        _ = system("cls")
    else:  # *nix based systems (Linux, MacOS, etc)
        _ = system("clear")


def get_user_input():
    """Get text input from the user."""
    user_input = input()
    match user_input:
        case "start":
            ga.generate_timetable()
        case "help":
            print("This is the help page that hasn't been written yet")
            get_user_input()
        case _:
            print("'" + user_input + "' is not a recognised command. Type \
                help for the help guide")
            get_user_input()


if __name__ == "__main__":
    menu()
