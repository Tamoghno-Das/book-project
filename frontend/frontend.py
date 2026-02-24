import streamlit as st
import requests
import pandas as pd

BASE_URL = "https://book-project-l4d0.onrender.com"

st.set_page_config(page_title="Book App", layout="wide")

st.title(" Book Management Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    ["View Books", "Search", "Add Book", "Delete Book"]
)

# View Books
if menu == "View Books":
    st.subheader("All Books")

    response = requests.get(f"{BASE_URL}/books")

    if response.status_code == 200:
        books = response.json()
        df = pd.DataFrame(books)
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Failed to load books")


# Search
elif menu == "Search":
    st.subheader("Search Book")

    col1, col2 = st.columns(2)

    with col1:
        book_id = st.number_input("Book ID", min_value=1)

        if st.button("Search by ID"):
            res = requests.get(f"{BASE_URL}/books/{book_id}")
            if res.status_code == 200:
                st.success("Found")
                st.json(res.json())
            else:
                st.error("Not found")


# Add Book
elif menu == "Add Book":
    st.subheader("Add New Book")

    with st.form("book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        description = st.text_area("Description")
        rating = st.slider("Rating", 1, 5)
        year = st.number_input("Published Year", 2000, 2030)

        submit = st.form_submit_button("Add Book")

        if submit:
            data = {
                "title": title,
                "author": author,
                "description": description,
                "rating": rating,
                "published_date": year
            }

            res = requests.post(f"{BASE_URL}/create-book", json=data)

            if res.status_code == 201:
                st.success("Book Added")
            else:
                st.error("Error")


# Delete
elif menu == "Delete Book":
    st.subheader("Delete Book")

    book_id = st.number_input("Book ID", min_value=1)

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/books/{book_id}")

        if res.status_code == 204:
            st.success("Deleted")
        else:
            st.error("Not found")
