# Import necessary libraries
import streamlit as st # Streamlit for creating the web app
import plotly.express as px # Plotly for creating interactive plots
from backend import get_data # Import a function for retrieving weather data

# Add title, text input, slider, select-box and subheader
st.title("Weather Forecast For The Next Days") # Create the title of the web app
place = st.text_input("Place: ", placeholder="Type here...") # Create a text input field for user to enter place
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days") # Create a slider to select number of forecast days
option = st.selectbox("Select Data to view", ("Temperature", "Sky")) # Create a select-box to choose between temperature and sky view
st.subheader(f"{option} for the next {days} days in {place}") # Create a subheader showing what the user has selected

if place:
    try:
        filtered_data = get_data(place, days) # Call the get_data function to retrieve weather data based on user input

        # Get the temperature data
        if option == "Temperature":
            # Create a temperature plot in case of temperature data
            temperatures = []
            for value in filtered_data:
                temp = value["main"]["temp"]/10 # Convert temperature from Kelvin to Celsius
                temperatures.append(temp)
            dates = []
            for date in filtered_data:
                dates.append(date["dt_txt"]) # Get the date/time information from the weather data
            figure = px.line(x=dates, y=temperatures, labels={"x": "Dates", "y": "Temperatures (C)"}) # Create a line plot using Plotly
            st.plotly_chart(figure) # Display the plot in the web app

        # Get the sky data
        if option == "Sky":
            sky_data = []
            for value in filtered_data:
                sky_data.append((value["dt_txt"], value["weather"][0]["main"])) # Extract the date/time and weather condition information from the weather data
            images = {"Clear": "images/clear.png", "Clouds": "images/clouds.png", "Rain": "images/rain.png", "Snow": "images/snow.png"} # contains the path to the images
            cols = st.columns(4)  # Display 4 images in each row
            for date, condition in sky_data:
                image_path = images[condition] # Get the image path based on the weather condition
                with cols[0]:
                    st.image(image_path, width=115) # Display the image in the web app
                    st.write(date) # Display the date/time information below the image
                cols = cols[1:]  # Move to the next column
                if not cols:  # Check if we've reached the end of the row
                    cols = st.columns(4)  # Reset cols to have 4 columns on the next row

    except KeyError:
        st.write("<p style='color:red; font-size:30px'>This place doesn't exist, Please enter somthing else.</p>", unsafe_allow_html=True) # Display an error message if the user enters an invalid location
