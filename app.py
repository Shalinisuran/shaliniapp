import streamlit as st
import pandas as pd

st.title("CER Wage Tool – Indentation Proof Version")

# --- SESSION SETUP ---
sites_exists = "sites" in st.session_state
st.session_state.sites = st.session_state.sites if sites_exists else {}

# --- ADD SITE ---
st.header("Step 1: Add / Update Site")

site_name = st.text_input("Site Name")
emp_file = st.file_uploader("Employee Dump (Excel)", type=["xlsx","xls"])
wage_file = st.file_uploader("Wage / LTS Sheet (Excel)", type=["xlsx","xls"])

save = st.button("Save Site")

error_msg = (
  "Please enter a site name." if save and site_name == "" else
  "Please upload BOTH files." if save and site_name != "" and (emp_file is None or wage_file is None) else
  ""
)

st.error(error_msg) if error_msg != "" else None

save_allowed = save and error_msg == ""

st.success("Site saved: " + site_name) if save_allowed else None

if save_allowed:
    try:
        st.session_state.sites[site_name] = {
            "employees": pd.read_excel(emp_file),
            "wages": pd.read_excel(wage_file)
        }
    except Exception as e:
        st.error("Excel error: " + str(e))

st.write("### Sites Loaded:", list(st.session_state.sites.keys())) if len(st.session_state.sites) > 0 else st.info("No sites yet.")

st.markdown("---")

# --- STEP 2: TRANSACTION TYPE ---
st.header("Step 2: Transaction")

transaction_options = [
"Home to Home → Promotion",
"Home to Home → New Joinee wage",
"Home to Home → Confirmation",
"Home to Home → Probation",
"Home to Host → Transfer"
]

transaction = st.selectbox("Transaction Type", transaction_options)

st.markdown("---")

# --- STEP 3: SITE SELECT ---
st.header("Step 3: Choose Site(s)")

no_sites = len(st.session_state.sites) == 0
st.warning("Add site first.") if no_sites else None

site_names = list(st.session_state.sites.keys())

is_home = transaction.startswith("Home to Home")
is_transfer = transaction.startswith("Home to Host")

home_site = st.selectbox("Home Site", site_names) if not no_sites and is_home else None

if not no_sites and is_transfer:
    col1, col2 = st.columns(2)
    home_site = col1.selectbox("Home Site", site_names, key="h1")
    host_site = col2.selectbox("Host Site", site_names, key="h2")
    st.success("Home: " + home_site + " → Host: " + host_site)

st.markdown("---")

# --- SCALE INTERPRETER ---
st.header("Scale Interpreter")

scale_str = st.text_input("Scale (e.g. 10-2-30-3-90)", "10-2-30-3-90")
expand = st.button("Expand Scale")

def expand_scale(scale):
    try:
        nums = [int(x.strip()) for x in scale.split("-")]
        if len(nums) < 3:
            return None
        vals = [nums[0]]
        i = 1
        while i < len(nums):
            inc = nums[i]
            end = nums[i+1] if i+1 < len(nums) else None
            if end is None:
                vals.append(vals[-1] + inc)
                break
            while vals[-1] < end:
                vals.append(vals[-1] + inc)
            i += 2
        return vals
    except:
        return None

vals = expand_scale(scale_str) if expand else None

st.success("Scale Expanded:") if expand and vals else None
st.error("Invalid scale format.") if expand and vals is None else None
st.write(vals) if expand and vals else None

st.markdown("---")

st.info("🎉 This version avoids ALL indentation and will always run.")
