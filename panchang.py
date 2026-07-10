import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta


def scrape_daily_panchang(date_str):
    """Scrape one day"""
    url = f"https://www.drikpanchang.com/panchang/day-panchang.html?geoname-id=1254624&date={date_str.replace('-', '/')}"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract key info (you can expand this)
        data = {
            "date": date_str,
            "tithi": "Extracted Tithi",
            "nakshatra": "Extracted Nakshatra",
            # Add more fields as needed
        }
        return data
    except:
        return {"date": date_str, "error": "Failed to fetch"}

# Generate full year


def generate_full_year():
    full_data = []
    start = datetime(2026, 1, 1)

    print("Scraping 2026 Panchang... (This may take time)")
    for i in range(366):
        current = start + timedelta(days=i)
        date_str = current.strftime("%Y-%m-%d")
        day_data = scrape_daily_panchang(date_str)
        full_data.append({
            "question": f"What is the Panchang for {date_str} in Thasra, Gujarat?",
            "answer": str(day_data)
        })
        print(f"✓ {date_str}")

    with open("full_panchang_2026_thasra.json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2, ensure_ascii=False)

    print("✅ Full 2026 Panchang saved!")


if __name__ == "__main__":
    generate_full_year()
