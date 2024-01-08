import streamlit as st
import requests
import pandas as pd

# Define the base URL for your FastAPI server
BASE_URL = "http://127.0.0.1:8000"  # Update with your actual FastAPI server URL

st.title("Data Downloader and Chatbot App")

# Data Downloader Section
st.header("Data Downloader")

# User input for Data Downloader
keywords = st.text_input("Enter keywords:")
download_format = st.selectbox("Select download format:", ["csv", "json"])

# Store display_data in session state
if 'display_data' not in st.session_state:
    st.session_state.display_data = None

# Store downloaded_data in session state
if 'downloaded_data' not in st.session_state:
    st.session_state.downloaded_data = None

# Store resource_id in session state
if 'resource_id' not in st.session_state:
    st.session_state.resource_id = None

# Trigger search and display databases on button click
if st.button("Search Databases"):
    search_endpoint = f"{BASE_URL}/search"
    search_params = {"query": keywords, "search_fields": ["title", "description"], "sort_by": "title", "ascending": True}
    search_response = requests.post(search_endpoint, json=search_params)

    if search_response.status_code == 200:
        st.session_state.display_data = search_response.json().get("data")
        st.success("Databases found:")
    else:
        st.error(f"Error during search: {search_response.text}")

# Extract relevant information for display
display_data = st.session_state.display_data
if display_data is not None and len(display_data) > 0:
    display_data_info = [{"resource_id": entry["resource_id"],
                          "title": entry["title"],
                          "description": entry["description"],
                          "org_type": entry["org_type"],
                          "source": entry["source"]} for entry in display_data]

    # Display the databases in a table
    df_display = pd.DataFrame(display_data_info)
    st.table(df_display)

    # Input box for choosing a row
    chosen_database_index = st.number_input("Pick a row (enter index):", min_value=0, max_value=len(display_data_info)-1)

    # Store the chosen index in session state
    st.session_state.chosen_database_index = chosen_database_index

    # Download button
    if st.button("Download"):
        resource_id = display_data_info[chosen_database_index]["resource_id"]
        st.session_state.resource_id = resource_id  # Store resource_id in session state
        st.success(resource_id)

        # Call the download API
        download_endpoint = f"{BASE_URL}/download/{resource_id}"
        download_params = {"output_format": download_format}
        download_response = requests.get(download_endpoint, params=download_params)

        if download_response.status_code == 200:
            # Save the downloaded data to session state
            st.session_state.downloaded_data = pd.DataFrame(download_response.json().get("data"))
            st.success("Data downloaded successfully!")

# Chatbot Section
st.header("Chatbot")

# Use the downloaded_data from session state
downloaded_data = st.session_state.downloaded_data

# Check if data is downloaded before allowing chatbot interaction
if downloaded_data is not None:
    # User input for Chatbot
    st.write(downloaded_data)
    user_question = st.text_input("Ask a question about the downloaded data:")

    # Trigger chatbot response on button click
    if st.button("Ask Chatbot"):
        resource_id = st.session_state.resource_id  # Retrieve resource_id from session state
        chatbot_endpoint = f"{BASE_URL}/chatbot/{resource_id}"
        chatbot_params = {"user_question": user_question}
        chatbot_response = requests.get(chatbot_endpoint, params=chatbot_params)

        if chatbot_response.status_code == 200:
            chatbot_response_text = chatbot_response.json().get("chatbot_response")
            st.success("Chatbot response:")
            st.write(chatbot_response_text)
        else:
            st.error(f"Error during chatbot interaction: {chatbot_response.text}")
else:
    st.warning("No data downloaded yet. Please download data before using the chatbot.")
