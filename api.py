import requests
# this library send request to api for access their data
import matplotlib.pyplot as plt
# this library provide data visualization of data like plots and charts but in this code we as plot so we write plt
from matplotlib.patches import Wedge
# this libray is for creating pie charts, or other circular visualization
import numpy as np
# this library is used for to do mathematical calculation

# Constants
API_KEY = 'a6630d20529b784e3089bada0a770a1f'
# create variable to add api key inside there so we can access whenever we required by variable
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
city_name = input("Enter city name: ")

# based on api key we access url to fetch data and access through url
# create function to fetch weather data
def fetch_weather_data(city, api_key):
    try:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
            # unit metric means firstly data show in f unit convert that unit metric so it automatically show in c with the use library numpy
        }
        response = requests.get(BASE_URL, params=params)
        # we get request through given url based upon our api key and store in variable so whenever required we access through variable
        response.raise_for_status()
        # check HTTP request status if it is failed then run exception code
        return response.json()
    except requests.exceptions.RequestException as equal:
        raise RuntimeError(f"Error fetching weather data: {equal}")

# Function to create a gauge chart
def create_gauge(ax, value, title, min_val, max_val, segments, colors):
    # we give parameter ax to draw a gauge area then ,
    # value give parameter to show value of data in text form,
    # title parameter for which data present,
    # min_value show in graph
    # max_value show in graph
    # segment show section to design various section in graph
    # colors is used to decide color in section which section has which color is more suitable
    ax.set_aspect("equal")
    # set aspect derive ratio of x-axis and y-axis and we derive equal


    # Draw gauge segments
    for i, color in enumerate(colors):
        start_angle = 180 - (i + 1) * (180 / len(colors))
        # I want to draw gauge in half circle, so i give 180 so give section divide to 180 so it exactly same measure than others
        end_angle = 180 - i * (180 / len(colors))
        # as it is above i derive to end circle formula so it make short and look like a pie chart
        ax.add_patch(Wedge((0, 0), 1, start_angle, end_angle, facecolor=color, edgecolor="white"))
        # wedge according to formula of start angle and end angle we draw with matplotlib library wedge
    # Draw needle mathematical formula
    normalized_value = (value - min_val) / (max_val - min_val)
    needle_angle = 180 * (1 - normalized_value)
    theta = np.radians(needle_angle)
    ax.plot([0, 0.9 * np.cos(theta)], [0, 0.9 * np.sin(theta)], color="black", linewidth=3)

    # Add value text above needle formula
    text_x = 1.1 * np.cos(theta)
    text_y = 1.1 * np.sin(theta)
    ax.text(text_x, text_y, f"{value}", ha="center", va="center", fontsize=12, fontweight="bold")

    # Add theta labels
    for angle, label in zip(np.linspace(180, 0, len(segments)), segments):
        theta_label = np.radians(angle)
        ax.text(1.1 * np.cos(theta_label), 1.1 * np.sin(theta_label), label, ha="center", va="center", fontsize=10)

    # Add title
    ax.set_title(title, fontsize=12, fontweight="bold", y=1.2)
    ax.axis("off")

# Main script
if __name__ == "__main__":


    try:
        # Fetch weather data
        data = fetch_weather_data(city_name, API_KEY)

        # Extract weather details
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        description = data["weather"][0]["description"].capitalize()

        # Create dashboard
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        # Humidity gauge
        create_gauge(
            axs[0, 0], humidity, "Humidity (%)", 0, 100,
            ["0", "20", "40", "60", "80", "100"],
            ["#26c6da", "#4dd0e1", "#80deea", "#b2ebf2", "#e0f7fa"]
        )

        # Temperature gauge
        create_gauge(
            axs[0, 1], temperature, "Temperature (°C)", -50, 50,
            ["-50", "-30", "-10", "0", "10", "30", "50"],
            ["#4caf50", "#8bc34a", "#cddc39", "#ffc107", "#ff5722"]
        )

        # Weather description
        axs[1, 0].bar([0], [1], color="orange", label=description)
        axs[1, 0].set_title("Weather Description")
        axs[1, 0].set_xticks([0])
        axs[1, 0].set_xticklabels([description])
        axs[1, 0].set_yticks([])
        axs[1, 0].text(0, 0.5, description, fontsize=14, fontweight="bold", ha="center", color="black")
        axs[1, 0].legend(loc="upper right")

        # Pressure bar chart
        axs[1, 1].bar(["Pressure"], [pressure], color="green")
        axs[1, 1].set_title("Pressure (hPa)")
        axs[1, 1].set_ylabel("hPa")
        axs[1, 1].grid(True)
        axs[1, 1].text(
            0, pressure / 2, f"{pressure} hPa",
            ha="center", va="center", fontsize=12, fontweight="bold", color="white"
        )
        # Adjust layout and show the dashboard
        plt.tight_layout()
        plt.suptitle(f"Weather Dashboard for {city_name}", fontsize=16, y=1.02)
        plt.show()

    # if there is an error then it run below code
    except RuntimeError as e:
        print(e)
    except (KeyError, ValueError) as e:
        print(f"Error processing weather data: {e}")
