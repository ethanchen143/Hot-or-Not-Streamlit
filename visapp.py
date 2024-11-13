import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    data = pd.read_csv('hot_songs.csv')
    return data

data = load_data()

st.title("Hot or Not Data Visualization")

# Sidebar for selecting visualization options
st.sidebar.header('Select Feature')

# Select columns to visualize
columns = data.columns.tolist()[2:]
columns = [c for c in columns if not c.startswith('not')]
selected_column = st.sidebar.selectbox('Select feature to visualize', columns)

uploaded_file = st.sidebar.file_uploader("Upload your song data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    user_data = pd.read_csv(uploaded_file)
    
    # Check if the uploaded data has the same columns
    if set(user_data.columns) == set(data.columns):
        # Combine the datasets
        combined_data = pd.concat([data, user_data], ignore_index=True)
        
        # Notify user that the file was successfully uploaded and combined
        st.sidebar.success("File uploaded and combined successfully!")
        
        # Highlight the user song(s) in the plot
        user_values = user_data[selected_column].values
        
        # Plot the combined data distribution
        st.subheader(f'{selected_column}')
        plt.figure(figsize=(10, 6))
        sns.histplot(combined_data[selected_column], kde=True)
        
        # If the user uploaded data, plot the new data points as red dots
        for value in user_values:
            plt.axvline(value, color='blue', linestyle='--')
            # plt.text(value, plt.ylim()[1]*0.5, 'Your Song', color='blue')
        
        st.pyplot(plt)
    else:
        st.sidebar.error("Uploaded file does not match the required columns.")
        
else:
    # If no file is uploaded, plot the original data distribution
    st.header(f'{selected_column}')
    plt.figure(figsize=(10, 6))
    sns.histplot(data[selected_column], kde=True)
    st.pyplot(plt)