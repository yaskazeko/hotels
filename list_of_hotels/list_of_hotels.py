import requests

def get_hotels_with_phones(city_name="Berlin", limit=100):
    overpass_query = f"""
    [out:json][timeout:25];
    area["name"="{city_name}"]["boundary"="administrative"]["admin_level"="8"]->.searchArea;
    (
      node["tourism"="hotel"](area.searchArea);
      way["tourism"="hotel"](area.searchArea);
      relation["tourism"="hotel"](area.searchArea);
    );
    out center tags;
    """

    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": overpass_query})
    response.raise_for_status()
    data = response.json()

    hotels = []
    seen_names = set()

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name")
        if not name or name in seen_names:
            continue

        phone = (
            tags.get("phone")
            or tags.get("contact:phone")
            or tags.get("contact:mobile")
            or "Не указано"
        )

        seen_names.add(name)
        hotels.append({
            "id": len(hotels) + 1,
            "title": name,
            "phone": phone
        })

        if len(hotels) >= limit:
            break

    return hotels

# Пример использования
if __name__ == "__main__":
    city = "Berlin"
    hotels = get_hotels_with_phones(city)

    print("hotels = [")
    for hotel in hotels:
        print(f'    {hotel},')
    print("]")
