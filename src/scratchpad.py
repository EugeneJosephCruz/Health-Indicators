import streamlit as st

# Define a function to display the home page
def display_home():
    st.title("Home Page")
    st.write("Welcome to the home page!")
    if st.button("Go to Page 1"):
        st.session_state.current_page = "page_1"
    if st.button("Go to Page 2"):
        st.session_state.current_page = "page_2"

# Define a function to display Page 1
def display_page_1():
    st.title("Page 1")
    st.write("You are now on Page 1.")
    if st.button("Go Home"):
        st.session_state.current_page = "home"
    if st.button("Go to Page 2"):
        st.session_state.current_page = "page_2"

# Define a function to display Page 2
def display_page_2():
    st.title("Page 2")
    st.write("You are now on Page 2.")
    if st.button("Go Home"):
        st.session_state.current_page = "home"
    if st.button("Go to Page 1"):
        st.session_state.current_page = "page_1"

# Initialize the current page in session state if it's not already set
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Display the current page based on the value in session state
if st.session_state.current_page == "home":
    display_home()
elif st.session_state.current_page == "page_1":
    display_page_1()
elif st.session_state.current_page == "page_2":
    display_page_2()
