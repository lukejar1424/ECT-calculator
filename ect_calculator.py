import streamlit as st
import math

# Title and description
st.title("RSC Box ECT Calculator")
st.markdown("Enter box and pallet details below to calculate the Recommended Minimum ECT. Defaults match your sample Excel file.")

# Dictionaries for lookups (from your Excel SWITCH formulas)
flute_thickness = {
    "C": 0.1875,
    "BC": 0.3125,
    "B": 0.125
}

rh_factor = {
    30: 1.07, 35: 1.07, 40: 1.05, 45: 1.03, 50: 1.0,
    55: 0.97, 60: 0.93, 65: 0.89, 70: 0.85, 75: 0.77,
    80: 0.71, 85: 0.64, 90: 0.56
}

dwell_factor = {
    "1h.": 0.87, "6h.": 0.79, "12h.": 0.76, "1d.": 0.73,
    "2d.": 0.7, "3d.": 0.68, "5d.": 0.66, "10d.": 0.63,
    "30d.": 0.6, "60d.": 0.57, "90d.": 0.55, "180d.": 0.52,
    "1yr.": 0.5, "2yr.": 0.46
}

overhang_factor = {
    "0in.": 1.0, "0.4in.": 0.9, "0.8in.": 0.8,
    "1in.": 0.7, ">1in.": 0.6
}

misalignment_factor = {
    "0in.": 1.0, "0.5in.": 0.74, "1in.": 0.57, "1.5in.": 0.45
}

# Inputs: Box Information
st.header("Box Information")
L = st.number_input("Box length (L)", value=17.125, step=0.125)
w = st.number_input("Box width (w)", value=8.75, step=0.125)
W = st.number_input("Package weight (W)", value=11.25, step=0.25)
flute_type = st.selectbox("Board flute type", options=list(flute_thickness.keys()), index=0)  # Default "C"

# Pallet Load
st.header("Pallet Load")
n = st.number_input("Number of layers of packages (n)", value=9, step=1)
npl = st.number_input("Number of packages per layer (npl)", value=10, step=1)
Ns = st.number_input("Number of pallet load stacked in storage (Ns)", value=2, step=1)
pallet_weight = st.number_input("Pallet weight", value=45, step=1)
Nd = st.number_input("Number of pallet load stacked in transit (Nd)", value=1, step=1)

# Strength Reduction Factors
st.header("Strength Reduction Factors (SRF)")
rh_storage = st.selectbox("Relative humidity in storage (%)", options=list(rh_factor.keys()), index=4)  # Default 50
rh_transit = st.selectbox("Relative humidity in transit (%)", options=list(rh_factor.keys()), index=3)  # Default 45
dwell_storage = st.selectbox("Storage warehouse dwell time", options=list(dwell_factor.keys()), index=5)  # Default "3d."
stacking_type = st.selectbox("Interlocking stacking or column stacking", options=["Interlocking", "Column"], index=0)
overhang = st.selectbox("Overhang off the edge of the pallet", options=list(overhang_factor.keys()), index=2)  # Default "0.8in."
gapped_pallet = st.selectbox("Gapped Pallet", options=["Yes", "No"], index=0)
misalignment = st.selectbox("Misalignment", options=list(misalignment_factor.keys()), index=0)  # Default "0in."
dwell_transit = st.selectbox("Storage transit dwell time", options=list(dwell_factor.keys()), index=8)  # Default "30d."

# Calculations
inside_perimeter = 2 * (L + w)
board_thickness = flute_thickness[flute_type]

# Pallet calculations
PWC_s = (pallet_weight / npl) * (Ns - 1)
SSp_s = (Ns * n - 1) * W + PWC_s
PWC_d = (pallet_weight / npl) * (Nd - 1)
SSp_d = ((Nd * n - 1) * W + PWC_d) * 3  # Dynamic factor of 3

# SRF factors
interlock_factor = 0.6 if stacking_type == "Interlocking" else 1.0
gapped_factor = 0.8 if gapped_pallet == "Yes" else 1.0

# List of the four factors for SMALL(1) and SMALL(2)
factors = [interlock_factor, overhang_factor[overhang], gapped_factor, misalignment_factor[misalignment]]
factors_sorted = sorted(factors)
small1 = factors_sorted[0]
small2 = factors_sorted[1]

# SRF_s and SRF_d
SRF_s = (rh_factor[rh_storage] * dwell_factor[dwell_storage]) * small1 * small2
SRF_d = (rh_factor[rh_transit] * dwell_factor[dwell_transit]) * small1 * small2

# CS_s and CS_d
CS_s = SSp_s / SRF_s if SRF_s != 0 else 0
CS_d = SSp_d / SRF_d if SRF_d != 0 else 0

# Final ECT
max_cs = max(CS_s, CS_d)
ect = max_cs / (5.87 * math.sqrt(board_thickness * inside_perimeter)) if max_cs != 0 else 0

# Display results
st.header("Results")
st.markdown(f"**Inside Perimeter:** {inside_perimeter:.2f}")
st.markdown(f"**Board Thickness:** {board_thickness:.4f}")
st.markdown(f"**PWC(s):** {PWC_s:.2f}")
st.markdown(f"**SSp(s):** {SSp_s:.2f}")
st.markdown(f"**PWC(d):** {PWC_d:.2f}")
st.markdown(f"**SSp(d):** {SSp_d:.2f}")
st.markdown(f"**SRF(s):** {SRF_s:.4f}")
st.markdown(f"**SRF(d):** {SRF_d:.4f}")
st.markdown(f"**CS(s):** {CS_s:.2f}")
st.markdown(f"**CS(d):** {CS_d:.2f}")
st.markdown(f"### Recommended Minimum ECT: {ect:.2f}")
