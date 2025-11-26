import streamlit as st
import pandas as pd

# SESSION STORAGE FOR SITES
if "sites" not in st.session_state:
st.session_state.sites = {}

st.title("CER Wage Tool Prototype – v1")
st.write("✔ Sites\n✔ Transactions\n✔ Home→Home & Home→Host\n✔ Scale Interpreter\n")

st.header("Step 1: Add / Update Site Data")

site_name = st.text_input("Enter Site Name")

emp_file = st.file_uploader("Upload Employee Dump (Excel)", type=["xlsx", "xls"])
wage_file = st.file_uploader("Upload Wage / LTS Sheet (Excel)", type=["xlsx", "xls"])

save_clicked = st.button("Save Site")

if save_clicked:
if site_name == "":
st.error("Please enter a site name.")
if emp_file is None or wage_file is None:
st.error("Please upload BOTH employee dump and wage sheet.")
if site_name != "" and emp_file is not None and wage_file is not None:
try:
emp_df = pd.read_excel(emp_file)
wage_df = pd.read_excel(wage_file)

st.session_state.sites[site_name] = {
"employees": emp_df,
"wages": wage_df
}

st.success("Saved site: " + site_name)
st.write("Employee Dump Preview")
st.dataframe(emp_df.head())
st.write("Wage Sheet Preview")
st.dataframe(wage_df.head())

except Exception as e:
st.error("Error reading files: " + str(e))

if len(st.session_state.sites) > 0:
st.write("### Sites Loaded:")
st.write(list(st.session_state.sites.keys()))
else:
st.info("No sites loaded yet.")

st.markdown("---")

st.header("Step 2: Choose Transaction Type")

transaction_options = [
"Home to Home → Promotion",
"Home to Home → New Joinee wage",
"Home to Home → Confirmation",
"Home to Home → Probation",
"Home to Host → Transfer"
]

transaction = st.selectbox("Transaction Type", transaction_options)

st.markdown("---")

st.header("Step 3: Select Site(s)")

if len(st.session_state.sites) == 0:
st.warning("Please add at least ONE site in Step 1 first.")
else:
site_names = list(st.session_state.sites.keys())

if transaction.startswith("Home to Home"):
selected_home = st.selectbox("Select Home Site", site_names)
st.success("Home Site Selected: " + selected_home)

if transaction.startswith("Home to Host"):
col1, col2 = st.columns(2)
with col1:
selected_home = st.selectbox("Home Site", site_names, key="home_site2")
with col2:
selected_host = st.selectbox("Host Site", site_names, key="host_site2")
st.success("Home: " + selected_home + " → Host: " + selected_host)

st.markdown("---")

st.header("Step 4: Basic Scale Interpreter")

st.write("Enter scale string like: 10-2-30-3-90")

scale_str = st.text_input("Scale String", "10-2-30-3-90")

btn_expand = st.button("Expand Scale")

if btn_expand:
# SCALE INTERPRETER WITHOUT INDENTATION ISSUES
try:
parts = [int(x.strip()) for x in scale_str.split("-")]
if len(parts) < 3:
st.error("Invalid scale format. Minimum must be start-inc-end.")
else:
values = []
current = parts[0]
values.append(current)
i = 1
steps = 0
max_steps = 300

while i < len(parts) and steps < max_steps:
inc = parts[i]
end = None
if i + 1 < len(parts):
end = parts[i + 1]

while True:
current = current + inc
values.append(current)
steps = steps + 1

if end is not None and current >= end:
break
if end is None:
break
if steps >= max_steps:
break

i = i + 2

st.success("Scale Expanded")
st.write(values)
st.write("Min:", min(values), "Max:", max(values))

except:
st.error("Error interpreting scale. Please check your format.")

st.markdown("---")

st.info("🎉 Base app structure ready. Next: add logic for each transaction type.")
