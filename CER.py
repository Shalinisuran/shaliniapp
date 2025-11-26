import streamlit as st
import pandas as pd

# ---------- Helpers ----------
def init_state():
"""Initialize session_state containers."""
if "sites" not in st.session_state:
st.session_state.sites = {}

def expand_scale(scale_str, max_value=None, max_steps=200):
try:
parts = [int(p.strip()) for p in scale_str.split("-")]
except Exception:
return []

if len(parts) < 3:
return []

values = []
start = parts[0]
current = start
values.append(current)

i = 1
steps = 0

while i < len(parts) and steps < max_steps:
inc = parts[i]
end = parts[i + 1] if i + 1 < len(parts) else None

while True:
current += inc
steps += 1

if max_value is not None and current > max_value:
return values

values.append(current)

if end is not None and current >= end:
break

if end is None and steps >= max_steps:
return values

i += 2

return values


# ---------- Main App ----------
def main():
init_state()

st.title("Wage Tool Prototype (v0)")
st.write("Prototype to manage sites and transaction types.")

# ----------------- Add Site -----------------
st.header("Step 1: Add / Update Site Data")

with st.expander("Add a new site"):
site_name = st.text_input("Site name")

st.markdown("**Upload Employee Dump**")
emp_file = st.file_uploader("Employee dump", type=["xlsx"])

st.markdown("**Upload Wage / LTS Info**")
wage_file = st.file_uploader("Wage info", type=["xlsx"])

if st.button("Save site data"):
if not site_name:
st.error("Enter site name.")
elif emp_file is None or wage_file is None:
st.error("Upload BOTH files.")
else:
emp_df = pd.read_excel(emp_file)
wage_df = pd.read_excel(wage_file)

st.session_state.sites[site_name] = {
"employees": emp_df,
"wages": wage_df,
}

st.success(f"Saved site: {site_name}")
st.dataframe(emp_df.head())
st.dataframe(wage_df.head())

if st.session_state.sites:
st.write("Loaded sites:", list(st.session_state.sites.keys()))

st.markdown("---")

# ----------------- Transaction Selection -----------------
st.header("Step 2: Select Transaction Type")

transaction_options = [
"Home to Home → Promotion",
"Home to Home → New Joinee wage",
"Home to Home → Confirmation",
"Home to Home → Probation",
"Home to Host → Transfer",
]

transaction_type = st.selectbox("Transaction", transaction_options)

# ----------------- Site Selection -----------------
st.header("Step 3: Select Site(s)")

if not st.session_state.sites:
st.warning("Add at least one site.")
return

site_names = list(st.session_state.sites.keys())

if transaction_type.startswith("Home to Home"):
home_site = st.selectbox("Home site", site_names)
st.write(f"Selected site: {home_site}")

else:
col1, col2 = st.columns(2)
with col1:
home_site = st.selectbox("Home site", site_names)
with col2:
host_site = st.selectbox("Host site", site_names)
st.write(f"Home: {home_site}, Host: {host_site}")

st.markdown("---")

# ----------------- Scale Interpretation Test -----------------
st.header("Step 4: Scale Interpretation")

scale_str = st.text_input("Enter a scale string", "10-2-30-3-90")

if st.button("Expand scale"):
values = expand_scale(scale_str)
st.write(values[:50])
st.write(f"Min: {min(values)}, Max: {max(values)}")


if __name__ == "__main__":
main()
