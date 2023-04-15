import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, select-box and subheader
st.title("Weather Forecast For The Next Days")
place = st.text_input("Place: ", placeholder="Type here...")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select Data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")


if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            # Create a temperature plot incase of temperature data
            temperatures = []
            for value in filtered_data:
                temp = value["main"]["temp"]/10
                temperatures.append(temp)
            dates = []
            for date in filtered_data:
                dates.append(date["dt_txt"])
            figure = px.line(x=dates, y=temperatures, labels={"x": "Dates", "y": "Temperatures (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            sky_data = []
            for value in filtered_data:
                sky_data.append((value["dt_txt"], value["weather"][0]["main"]))
            images = {"Clear": "images/clear.png", "Clouds": "images/clouds.png", "Rain": "images/rain.png", "Snow": "images/snow.png"} # contains the path to the images
            cols = st.columns(4)  # Display 4 images in each row
            for date, condition in sky_data:
                image_path = images[condition]
                with cols[0]:
                    st.image(image_path, width=115)
                    st.write(date)
                cols = cols[1:]  # Move to the next column
                if not cols:  # Check if we've reached the end of the row
                    cols = st.columns(4)  # Reset cols to have 4 columns on the next row


    except KeyError:
        st.write("<p style='color:red; font-size:30px'>This place doesn't exist, Please enter somthing else.</p>", unsafe_allow_html=True)