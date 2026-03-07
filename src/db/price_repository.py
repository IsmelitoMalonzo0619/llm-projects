from .connection import get_connection

def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT price FROM prices WHERE city = ?",
            (city.lower(),)
        )

        result = cursor.fetchone()

        if result:
            return f"Ticket price to {city} is ${result[0]}"
        else:
            return "No price data available for this city"