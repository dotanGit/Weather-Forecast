import requests

API_KEY = "20c994c2f69ace498e297314b2bb1a89"

def get_data(place, forecast_days=None, kind=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data['list']
    number_values = 8 * forecast_days
    filtered_data = filtered_data[:number_values]
    if kind == "Temperature":
        # [expression for variable in iterable] - value is a temporary variable that contains what's inside filtered_data in place main and in place temp
        filtered_data = [value["main"]['temp'] for value in filtered_data]
    if kind == "Sky":
        filtered_data = [value["weather"][0]["main"] for value in filtered_data]

    return filtered_data

if __name__ == "__main__":
    print(get_data(place="Tokyo", forecast_days=3, kind="Temperature"))