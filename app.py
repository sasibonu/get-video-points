import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


def load_transcript(file):
    if file is not None:
        if file.name.endswith('.csv'):
            return(pd.read_csv(file))
        elif file.name.endswith('.json'):
            return(pd.read_json(file))
        else:
            st.write("File unsupported format")
            return(None)
    else:
        return(None)
    

def create_transcript_panel(transcript_df):
    st.sidebar.write("This is the transcript panel.")
    st.sidebar.write(transcript_df)


def create_video_panel(video_path, transcript_df):
    st.write("Video Panel")
    st.video(video_path, format="video/mp4")

    st.write("Click timestamps")

    for index, rows in transcript_df.iterrows():

        startTime = convert_video_time(rows['Start Time'])

        html_string = f'''
        <p><a href='#', onClick='event.preventDefault(); goTime("{startTime}");'>{rows['Start Time']} - {rows['End Time']}</a> {rows['Text']}</p>




        <script>
        function goTime(startTime) {{
    
            var video = window.parent.document.querySelector("video")
            console.log("Getting", startTime)
            if (video) {{
                video.currentTime = startTime
                console.log("Playing Video")
                video.play()
            }}
   
        }}

        </script>


        '''

        components.html(html_string,height=40)


def convert_video_time(startTime):
    hours, mins, secs = startTime.split(":")
    hours = int(hours)
    mins = int(mins)
    secs = int(secs)
    return(hours*3600+mins*60+secs)



def main():

    if 'transcript_df' not in st.session_state:
        st.session_state.transcript_df = None
    if 'video_file' not in st.session_state:
        st.session_state.transcript_df = None

    transcript_file = st.sidebar.file_uploader("Upload file for transcript.")
    if transcript_file is not None:
        st.session_state.transcript_df = load_transcript(transcript_file)
        if st.session_state.transcript_df is not None:
            create_transcript_panel(st.session_state.transcript_df)


    video_file = st.sidebar.file_uploader("Upload video file.")
    if video_file is not None:
        st.session_state.video_file = video_file
        if st.session_state.video_file is not None:
            create_video_panel(st.session_state.video_file, st.session_state.transcript_df)

if __name__ == "__main__":
    main()