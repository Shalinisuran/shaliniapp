import streamlit as st

st.title("Wage Tool – Basic Test")
st.write("🎉 If you can see this message, the app is finally running without indentation issues.")

transaction_options = [
"Home to Home → Promotion",
"Home to Home → New Joinee wage",
"Home to Home → Confirmation",
"Home to Home → Probation",
"Home to Host → Transfer"
]

transaction_type = st.selectbox("Transaction type", transaction_options)

st.write("You selected:", transaction_type)
