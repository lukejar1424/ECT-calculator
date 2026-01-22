import streamlit as st
import math

# Custom theme (maroon red + black from logo)
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
    .stButton > button {
        background-color: #A6192E; /* Maroon red */
        color: white;
    }
    h1, h2, h3, h4 {
        color: #A6192E;
    }
    .stSelectbox, .stNumberInput {
        border-color: #000000; /* Black accents */
    }
    </style>
""", unsafe_allow_html=True)

# Logo at top
st.image("armor_logo.png", use_container_width=True)

# Title and description
st.title("RSC Box ECT Calculator")
st.markdown("Enter box and pallet details below to calculate the Recommended Minimum ECT. Brought to you by Armor Packaging.")

# Dictionaries for lookups (exact match to Excel SWITCH formulas)
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

# Tabs for organization
tab1, tab2, tab3, tab4 = st.tabs(["Box Information", "Pallet Load", "Strength Reduction Factors", "Results"])

with tab1:
    st.header("Box Information")
    L = st.number_input("Box length (L) inches", value=17.125, step=0.125)
    w = st.number_input("Box width (w) inches", value=8.75, step=0.125)
    W = st.number_input("Package weight (W) lb", value=11.25, step=0.25)
    flute_type = st.selectbox("Board flute type", options=list(flute_thickness.keys()), index=0)  # Default "C"

with tab2:
    st.header("Pallet Load")
    n = st.number_input("Number of layers of packages (n)", value=9, step=1)
    npl = st.number_input("Number of packages per layer (npl)", value=10, step=1)
    Ns = st.number_input("Number of pallet load stacked in storage (Ns)", value=2, step=1)
    pallet_weight = st.number_input("Pallet weight lb", value=45, step=1)
    Nd = st.number_input("Number of pallet load stacked in transit (Nd)", value=1, step=1)
    
    # Diagram with explanations
    st.subheader("Palletized Load Diagram")
    st.image("pallet_diagram.png", use_container_width=True)
    st.markdown("""
    - **n (layers)**: Vertical arrow → height of boxes stacked on one pallet (e.g., 9 layers high).
    - **npl (packages per layer)**: Horizontal arrows → number of boxes side-by-side per layer (e.g., 10 per row).
    - **Ns (storage stacking)**: Downward arrow on top → how many full pallets are stacked in warehouse (e.g., 2 pallets high).
    - **Nd (transit stacking)**: Similar to Ns but for shipping (e.g., 1 pallet high, with dynamic factor applied).
    """)

with tab3:
    st.header("Strength Reduction Factors (SRF)")
    rh_storage = st.selectbox("Relative humidity in storage (%)", options=list(rh_factor.keys()), index=4)  # Default 50
    rh_transit = st.selectbox("Relative humidity in transit (%)", options=list(rh_factor.keys()), index=3)  # Default 45
    dwell_storage = st.selectbox("Storage warehouse dwell time", options=list(dwell_factor.keys()), index=5)  # Default "3d."
    dwell_transit = st.selectbox("Storage transit dwell time", options=list(dwell_factor.keys()), index=8)  # Default "30d."

    st.subheader("Handling Factors")
    
    with st.expander("Interlocking stacking or column stacking"):
        stacking_type = st.selectbox("Stacking type", options=["Interlocking", "Column"], index=0)
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://blog.robotiq.com/hs-fs/hubfs/Stacking_Column_V2.jpg?width=323&height=202&name=Stacking_Column_V2.jpg", caption="Column Stacking: Aligned straight up for max stability but less interlock (factor 1.0)", use_container_width=True)
        with col2:
            st.image("https://blog.robotiq.com/hs-fs/hubfs/Stacking_Interlock_V2.jpg?width=323&height=202&name=Stacking_Interlock_V2.jpg", caption="Interlocking Stacking: Offset for better grip but reduced strength (factor 0.6)", use_container_width=True)

    with st.expander("Overhang off the edge of the pallet"):
        overhang = st.selectbox("Overhang", options=list(overhang_factor.keys()), index=2)  # Default "0.8in."
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://www.shipit.ca/wp-content/uploads/2015/04/pallet-overhang.jpg", caption="Overhang: Boxes hanging off edge, reduced stability (factor 0.6-0.9)", use_container_width=True)
        with col2:
            st.image("https://www.packagingrevolution.net/wp-content/uploads/2012/05/pallet-load.jpg", caption="No overhang: Flush edges with pallet for full support (factor 1.0)", use_container_width=True)

    with st.expander("Gapped Pallet"):
        gapped_pallet = st.selectbox("Gapped Pallet", options=["Yes", "No"], index=0)
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://www.palletone.com/wp-content/uploads/2024/01/101-anatomy-of-a-stringer-pallet.jpg", caption="Gapped wooden pallet: Spaces between boards, less support (factor 0.8)", use_container_width=True)
        with col2:
            st.image("https://www.rosepallet.com/wp-content/uploads/2020/06/block-pallet.jpg", caption="Solid wooden pallet: Full board coverage for better support (factor 1.0)", use_container_width=True)

    with st.expander("Misalignment"):
        misalignment = st.selectbox("Misalignment", options=list(misalignment_factor.keys()), index=0)  # Default "0in."
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://www.easycargo3d.com/wp-content/webp-express/webp-images/uploads/2023/10/Palletization-part-3-1.jpg.webp", caption="Aligned stacking: Boxes perfectly stacked on top of each other (factor 1.0)", use_container_width=True)
        with col2:
            st.image("https://www.researchgate.net/publication/289150258/figure/fig9/AS:1008538268753933@1617465669985/Test-setup-for-misaligned-three-high-stacks-of-boxes-along-the-long-edge.ppm", caption="Misaligned stacking: Boxes offset or shifted, reducing strength (factor 0.45-0.74)", use_container_width=True)

# ───────────────────────────────────────────────
# Calculations (exact match to Excel, with safety checks)
# ───────────────────────────────────────────────
inside_perimeter = 2 * (L + w)
board_thickness = flute_thickness[flute_type]

PWC_s = (pallet_weight / npl) * (Ns - 1) if npl != 0 else 0
SSp_s = (Ns * n - 1) * W + PWC_s
PWC_d = (pallet_weight / npl) * (Nd - 1) if npl != 0 else 0
SSp_d = ((Nd * n - 1) * W + PWC_d) * 3  # Dynamic factor of 3

interlock_factor = 0.6 if stacking_type == "Interlocking" else 1.0
gapped_factor = 0.8 if gapped_pallet == "Yes" else 1.0

factors = [interlock_factor, overhang_factor[overhang], gapped_factor, misalignment_factor[misalignment]]
factors_sorted = sorted(factors)
small1 = factors_sorted[0]
small2 = factors_sorted[1]

SRF_s = (rh_factor[rh_storage] * dwell_factor[dwell_storage]) * small1 * small2
SRF_d = (rh_factor[rh_transit] * dwell_factor[dwell_transit]) * small1 * small2

CS_s = SSp_s / SRF_s if SRF_s != 0 else 0
CS_d = SSp_d / SRF_d if SRF_d != 0 else 0

max_cs = max(CS_s, CS_d)
ect = max_cs / (5.87 * math.sqrt(board_thickness * inside_perimeter)) if board_thickness > 0 and inside_perimeter > 0 else 0

# ── Tab 4: Results ───────────────────────────────
with tab4:
    st.header("Results")
    st.markdown(f"**Inside Perimeter:** {inside_perimeter:.2f} inches")
    st.markdown(f"**Board Thickness:** {board_thickness:.4f} inches")
    st.markdown(f"**PWC(s):** {PWC_s:.2f} lb")
    st.markdown(f"**SSp(s):** {SSp_s:.2f} lb")
    st.markdown(f"**PWC(d):** {PWC_d:.2f} lb")
    st.markdown(f"**SSp(d):** {SSp_d:.2f} lb")
    st.markdown(f"**SRF(s):** {SRF_s:.4f}")
    st.markdown(f"**SRF(d):** {SRF_d:.4f}")
    st.markdown(f"**CS(s):** {CS_s:.2f} lb")
    st.markdown(f"**CS(d):** {CS_d:.2f} lb")
    st.markdown(f"### Recommended Minimum ECT: {ect:.2f} lb/in")
