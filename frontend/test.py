# import streamlit as st
# # Background image using HTML and CSS
# page_bg_img = '''
#     <style>
#         body {
#             background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
#             background-size: cover;
#         }
#     </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)

import streamlit as st

# Display image from URL
image_url = "https://images.unsplash.com/photo-1542281286-9e0a16bb7366"
st.image(image_url, caption='Your Image Caption', use_column_width=True)

# Or, display image from a local file
local_image_path = "bg.png"
st.image(local_image_path, caption='Your Image Caption', use_column_width=True)
