import streamlit as st
import pandas as pd

st.title("CER Wage Tool Prototype – V2 (No Indentation Version)")

# ---------- SESSION SETUP WITHOUT INDENT ----------
sites_exists = "sites" in st.session_state
if not sites_exists:
st.session_state.sites = {}

# ---------- ADD SITE SECTION ----------
st.header("Step 1: Add / Update Site Data")

site_name = st.text_input("Enter Site Name")

emp_file = st.file_uploader("Upload Employee Dump (Excel)", type=["xlsx","xls"])
wage_file = st.file_uploader("Upload Wage / LTS Sheet (Excel)", type=["xlsx","xls"])

save_btn = st.button("Save Site")

if save_btn and site_name == "":
st.error("Please enter a site name.")

if save_btn and site_name != "" and (emp_file is None or wage_file is None):
st.error("Please upload BOTH files for this site.")

save_allowed = save_btn and site_name != "" and emp_file is not None and wage_file is not None

if save_allowed:
try:
emp_df = pd.read_excel(emp_file)
wage_df = pd.read_excel(wage_file)
st.session_state.sites[site_name] = {"employees": emp_df, "wages": wage_df}
st.success("Site saved: " + site_name)
st.write("Employee Dump Preview")
st.dataframe(emp_df.head())
st.write("Wage Sheet Preview")
st.dataframe(wage_df.head())
except Exception as e:
st.error("Error loading Excel files: " + str(e))

# ---------- SHOW SITES ----------
sites_list = list(st.session_state.sites.keys())
if len(sites_list) == 0:
st.info("No sites added yet.")
else:
st.write("### Sites Loaded:")
st.write(sites_list)

st.markdown("---")

# ---------- TRANSACTION TYPE ----------
st.header("Step 2: Select Transaction Type")

transaction_options = [
"Home to Home → Promotion",
"Home to Home → New Joinee wage",
"Home to Home → Confirmation",
"Home to Home → Probation",
"Home to Host → Transfer"
]

transaction = st.selectbox("Transaction Type", transaction_options)

st.markdown("---")

# ---------- SITE SELECTION ----------
st.header("Step 3: Select Site(s)")

if len(sites_list) == 0:
st.warning("Add at least one site to proceed.")
else:
is_home_to_home = transaction.startswith("Home to Home")
is_transfer = transaction.startswith("Home to Host")

if is_home_to_home:
home_site = st.selectbox("Select Home Site", sites_list, key="h1")
st.success("Home Site Selected: " + home_site)

if is_transfer:
col1, col2 = st.columns(2)
home_site = col1.selectbox("Home Site", sites_list, key="h2")
host_site = col2.selectbox("Host Site", sites_list, key="h3")
st.success("Home: " + home_site + " → Host: " + host_site)

st.markdown("---")

# ---------- SCALE INTERPRETER ----------
st.header("Step 4: Scale Interpreter (No Indentation Logic)")

scale_str = st.text_input("Enter Scale (Example: 10-2-30-3-90)", "10-2-30-3-90")
scale_btn = st.button("Expand Scale")

if scale_btn:
parts = scale_str.split("-")
parsed_ok = True
int_parts = []

for part in parts:
try:
int_parts.append(int(part.strip()))
except:
parsed_ok = False

if not parsed_ok:
st.error("Scale format invalid. Must be numbers separated by dashes.")
if parsed_ok and len(int_parts) < 3:
st.error("Scale must be at least: start - increment - end")

run_expand = parsed_ok and len(int_parts) >= 3

if run_expand:
values = []
current = int_parts[0]
values.append(current)
i = 1
steps = 0
max_steps = 300

while i < len(int_parts) and steps < max_steps:
inc = int_parts[i]
end = None
if i + 1 < len(int_parts):
end = int_parts[i + 1]

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

st.success("Scale Expanded Successfully")
st.write(values)
st.write("Min:", min(values), "Max:", max(values))

st.markdown("---")

st.info("🎉 Base App Running Successfully Without Any Python Indentation.")
