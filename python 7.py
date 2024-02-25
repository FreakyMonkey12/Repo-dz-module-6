from datetime import datetime, timedelta


class Field:
    pass


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, record):
        self.contacts.append(record)

    def get_contact(self, name):
        for contact in self.contacts:
            if contact.name.value == name:
                return contact
        return None

    def upcoming_birthdays(self):
        upcoming = []
        today = datetime.now().date()
        for contact in self.contacts:
            if contact.birthday and today < contact.birthday.value:
                if contact.birthday.value - today <= timedelta(days=7):
                    upcoming.append(contact)
        return upcoming


def parse_input(user_input):
    return user_input.split()


def input_error(func):
    def wrapper(args, book):
        try:
            func(args, book)
        except ValueError as e:
            print(e)

    return wrapper


@input_error
def add(args, book):
    name, phone = args
    if book.get_contact(name):
        print("Contact already exists.")
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_contact(record)
        print("Contact added successfully.")


@input_error
def change(args, book):
    name, new_phone = args
    contact = book.get_contact(name)
    if contact:
        contact.phones = [Phone(new_phone)]
        print("Phone number updated successfully.")
    else:
        print("Contact not found.")


@input_error
def phone(args, book):
    name = args[0]
    contact = book.get_contact(name)
    if contact:
        print("Phone numbers:")
        for phone in contact.phones:
            print(phone.value)
    else:
        print("Contact not found.")


@input_error
def all_contacts(args, book):
    if book.contacts:
        print("All contacts:")
        for contact in book.contacts:
            print(contact.name.value)
    else:
        print("No contacts.")


@input_error
def add_birthday(args, book):
    name, birthday = args
    contact = book.get_contact(name)
    if contact:
        contact.add_birthday(birthday)
        print("Birthday added successfully.")
    else:
        print("Contact not found.")


@input_error
def show_birthday(args, book):
    name = args[0]
    contact = book.get_contact(name)
    if contact and contact.birthday:
        print(f"{contact.name.value}'s birthday: {contact.birthday.value.strftime('%d.%m.%Y')}")
    elif contact:
        print(f"{contact.name.value} has no birthday set.")
    else:
        print("Contact not found.")


@input_error
def birthdays(args, book):
    upcoming = book.upcoming_birthdays()
    if upcoming:
        print("Upcoming birthdays for the next week:")
        for contact in upcoming:
            print(f"{contact.name.value}: {contact.birthday.value.strftime('%d.%m.%Y')}")
    else:
        print("No upcoming birthdays.")


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            add(args, book)

        elif command == "change":
            change(args, book)

        elif command == "phone":
            phone(args, book)

        elif command == "all":
            all_contacts(args, book)

        elif command == "add-birthday":
            add_birthday(args, book)

        elif command == "show-birthday":
            show_birthday(args, book)

        elif command == "birthdays":
            birthdays(args, book)

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
