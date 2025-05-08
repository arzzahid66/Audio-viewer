import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(
    page_title="Audio Transcription Viewer",
    page_icon="🎵",
    layout="wide"
)

# Title
st.title("Audio Transcription Viewer")

# Function to load data
def load_data():
    # Read the CSV file
    try:
        df = pd.read_csv('transcriptions.csv')
        return df
    except FileNotFoundError:
        st.error("transcriptions.csv file not found!")
        return None

# Function to save data
def save_data(df):
    df.to_csv('transcriptions.csv', index=False)
    st.success("Changes saved successfully!")

# Function to get audio file path
def get_audio_path(filename):
    return os.path.join('audios', filename)

# Load data
df = load_data()

if df is not None:
    # Display each row with audio player
    for index, row in df.iterrows():
        col1, col2, col3 = st.columns([1, 2, 4])
        
        with col1:
            st.write(f"**#{index + 1}**")  # Display index
            audio_path = get_audio_path(row['filename'])
            if os.path.exists(audio_path):
                st.audio(audio_path)
            else:
                st.error(f"Audio file not found: {audio_path}")
        
        with col2:
            st.write(f"**{row['filename']}**")
        
        with col3:
            # Create a unique key for each text area
            text_key = f"transcription_{index}"
            
            # Add edit button
            if st.button(f"Edit #{index + 1}", key=f"edit_{index}"):
                st.session_state[f"editing_{index}"] = True
            
            # Show text area if editing is enabled
            if st.session_state.get(f"editing_{index}", False):
                edited_text = st.text_area("Transcription", row['transcription'], key=text_key, height=150)
                
                # Add save and cancel buttons
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("Save", key=f"save_{index}"):
                        df.at[index, 'transcription'] = edited_text
                        save_data(df)
                        st.session_state[f"editing_{index}"] = False
                        st.rerun()
                
                with col_cancel:
                    if st.button("Cancel", key=f"cancel_{index}"):
                        st.session_state[f"editing_{index}"] = False
                        st.rerun()
            else:
                st.write(row['transcription'])
        
        st.markdown("---")  # Add a separator between entries