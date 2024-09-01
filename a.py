import streamlit as st

# Set the title of the app
st.title("Mera Pehla Streamlit App")

# Add a text input box
name = st.text_input("Apna Naam Daalain:")

# Display a greeting based on the name provided
if name:
    st.write(f"Hello, {name}! Ye mera pehla Streamlit app hai.")
else:
    st.write("Apna naam daalain jisse hum aapko greet kar saken.")

# Add a short description
st.write("""
    Ye ek simple Streamlit application hai jo basic functionalities dikhata hai.
    Aap isko apne projects aur ideas ko showcase karne ke liye use kar sakte hain.
""")

# Add a button that shows a message when clicked
if st.button("Click Me"):
    st.write("Button clicked! Aap ne button click kiya hai.")
