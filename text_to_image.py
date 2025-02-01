import streamlit as st 
import requests
from PIL import Image
import io


API_URL = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
headers = {"Authorization": "Bearer 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"}

# variables
progress_text = "Operation in progress. Please wait. _may take up to a minute_"
url = "https://huggingface.co/ZB-Tech/Text-to-Image"

st.header("📝 Text to Image Generator 🖼️")
st.info("_This project is only made possible thanks to ✨ Hugging Face AI models ✨! Visit their website -> [🤗](%s)_" % url)

st.subheader('Your prompt please')
st.write("e.g., _a cat drinking coffee on the moon 🌕_")
user_input = st.text_input("")

def query(payload):
    global progress_bar
    progress_bar.progress(20, text=progress_text)
    response = requests.post(API_URL, headers=headers, json=payload)
    progress_bar.progress(35,text=progress_text)
    if response.status_code == 200:
        progress_bar.progress(40, text=progress_text)
        return response.content
    else:
        st.error(f"Error: {response.status_code}")
        st.error(response.text)
        return None

if user_input:
    progress_bar = st.progress(10,text=progress_text)
    image_bytes = query({
        "inputs": user_input,
    })

    if image_bytes:
        progress_bar.progress(60, text=progress_text)
        try:
            image = Image.open(io.BytesIO(image_bytes))
            progress_bar.progress(100, text="Complete!")
            st.balloons()
            st.subheader("Mission accomplished 🥳 🎉")
            st.image(image)
        except Exception as e:
            print(f"Error opening image: {e}")
        else:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)
            st.write("Want to download the image? ⬇️")
            st.download_button(
                label="Download Image",
                data=buffered,
                file_name=f"{user_input[0:7]}_ai_image.png",
                mime="image/png"
            )
else:
    st.write("Awaiting your command 🫡")


