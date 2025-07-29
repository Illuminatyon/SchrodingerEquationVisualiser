"""
Minimal Streamlit app for testing if Streamlit works correctly.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Streamlit Test App",
    page_icon="🧪",
    layout="wide",
)

# Title and description
st.title("Streamlit Test Application")
st.markdown("""
This is a minimal Streamlit app to test if Streamlit is working correctly.
If you can see this text and the elements below, Streamlit is functioning properly.
""")

# Sidebar
st.sidebar.header("Test Controls")
test_slider = st.sidebar.slider("Test Slider", 0, 100, 50)
test_checkbox = st.sidebar.checkbox("Test Checkbox", value=True)
test_selectbox = st.sidebar.selectbox(
    "Test Dropdown",
    ["Option 1", "Option 2", "Option 3"]
)

# Main content
st.header("Test Elements")

# Text input
test_input = st.text_input("Enter some text", "Hello, Streamlit!")
st.write(f"You entered: {test_input}")

# Display the slider value
st.subheader("Slider Value")
st.write(f"The slider value is: {test_slider}")

# Conditional display based on checkbox
if test_checkbox:
    st.success("The checkbox is checked!")
else:
    st.error("The checkbox is unchecked!")

# Display selected option
st.subheader("Selected Option")
st.write(f"You selected: {test_selectbox}")

# Create and display a simple plot
st.subheader("Test Plot")
fig, ax = plt.subplots(figsize=(10, 4))
x = np.linspace(0, 10, 100)
y = np.sin(x) * test_slider/50
ax.plot(x, y)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.set_title("Test Sine Wave (amplitude controlled by slider)")
st.pyplot(fig)

# Add a button
if st.button("Click Me!"):
    st.balloons()
    st.write("Button was clicked!")

# Add a progress bar
st.subheader("Progress Bar")
progress_bar = st.progress(0)
for i in range(100):
    # Update progress bar
    progress_bar.progress(i + 1)

st.success("If you can see all the elements above, Streamlit is working correctly!")