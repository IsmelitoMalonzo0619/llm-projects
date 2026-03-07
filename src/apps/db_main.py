import sys

from db import init_db, insert_db, get_ticket_price


def main():
    init_db()
    insert_db()

    print(get_ticket_price("london"))


if __name__ == "__main__":
    print(sys.path)
    main()