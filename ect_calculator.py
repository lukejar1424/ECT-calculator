import streamlit as st
import math

# ───────────────────────────────────────────────
# Custom theme (maroon red + black from logo)
# ───────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
    .stButton > button {
        background-color: #A6192E;
        color: white;
    }
    h1, h2, h3 {
        color: #A6192E;
    }
    .stSelectbox, .stNumberInput {
        border-color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Logo at top
st.image("armor_logo.png", width=None)

# Title and description
st.title("RSC Box ECT Calculator")
st.markdown("Calculate the **Recommended Minimum ECT** for Regular Slotted Containers based on pallet, storage, and transit conditions. Brought to you by **Armor Packaging**.")

# ───────────────────────────────────────────────
# Lookups (verified against your Excel)
# ───────────────────────────────────────────────
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

# ───────────────────────────────────────────────
# Tabs
# ───────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Box Information", "Pallet Load", "Strength Reduction Factors", "Results"])

# ── Tab 1: Box Information ───────────────────────
with tab1:
    st.header("Box Information")
    L = st.number_input("Box length (L) – inches", min_value=1.0, value=17.125, step=0.125, format="%.3f")
    w = st.number_input("Box width (w) – inches", min_value=1.0, value=8.75, step=0.125, format="%.3f")
    W = st.number_input("Package weight (W) – lb", min_value=0.1, value=11.25, step=0.25, format="%.2f")
    flute_type = st.selectbox("Board flute type", options=list(flute_thickness.keys()), index=0)

# ── Tab 2: Pallet Load ───────────────────────────
with tab2:
    st.header("Pallet Load")
    n = st.number_input("Number of layers of packages (n)", min_value=1, value=9, step=1)
    npl = st.number_input("Number of packages per layer (npl)", min_value=1, value=10, step=1)
    Ns = st.number_input("Number of pallet loads stacked in storage (Ns)", min_value=1, value=2, step=1)
    pallet_weight = st.number_input("Pallet weight – lb", min_value=0.0, value=45.0, step=1.0)
    Nd = st.number_input("Number of pallet loads stacked in transit (Nd)", min_value=1, value=1, step=1)

    st.subheader("Palletized Load Diagram")
    st.image("pallet_diagram.png", width=None)
    st.markdown("""
    **Key labels:**
    - ↓ **n** = number of box layers stacked on one pallet  
    - ↔ **npl** = number of boxes per layer (side-by-side)  
    - ↑ **Ns** = how many full pallets are stacked vertically in storage  
    - ↑ **Nd** = how many full pallets are stacked vertically in transit  
    """)

# ── Tab 3: Strength Reduction Factors ────────────
with tab3:
    st.header("Strength Reduction Factors (SRF)")

    # Non-visual inputs
    rh_storage = st.selectbox("Relative humidity in storage (%)", options=list(rh_factor.keys()), index=4)
    rh_transit = st.selectbox("Relative humidity in transit (%)", options=list(rh_factor.keys()), index=3)
    dwell_storage = st.selectbox("Storage warehouse dwell time", options=list(dwell_factor.keys()), index=5)
    dwell_transit = st.selectbox("Transit dwell time", options=list(dwell_factor.keys()), index=8)

    st.subheader("Visual & Handling Factors")

    # Overhang
    st.markdown("**Overhang off the edge of the pallet**")
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.image("https://freightsnap.com/wp-content/uploads/2019/01/Pallet_Packing_Illustrations-03.jpg",
                 caption="Minimal / no overhang\n→ better stability (factor ≈ 1.0)")
    with col_o2:
        st.image("https://assests.polcdn.com/blog/best-way-to-pack-pallets/avoid-overhang.jpg",
                 caption="Significant overhang\n→ reduced strength (factor 0.6–0.9)")

    # Gapped Pallet
    st.markdown("**Gapped Pallet**")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.image("https://plasticpalletsales.com/wp-content/uploads/2022/04/Closed-Deck-Solid-Deck-Pallets.png",
                 caption="Closed / solid deck\n→ full support (factor 1.0)")
    with col_g2:
        st.image("https://www.goplasticpallets.com/wp-content/uploads/2024/12/GPP-Open-vs-Closed-2024.png",
                 caption="Gapped / open deck\n→ less support (factor 0.8)")

    # Misalignment
    st.markdown("**Misalignment**")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.image("https://igps.net/wp-content/uploads/2024/03/iGPS-Blog-Stacking-Loaded-Pallets-Everything-You-Need-to-Know_v1.jpg",
                 caption="Properly aligned\n→ stronger stack (factor 1.0)")
    with col_m2:
        st.image("https://www.researchgate.net/publication/289150258/figure/fig9/AS:1008538268753933@1617465669985/Test-setup-for-misaligned-three-high-stacks-of-boxes-along-the-long-edge.ppm",
                 caption="Misaligned / offset\n→ weaker stack (factor 0.45–0.74)")

    # Stacking type
    st.markdown("**Stacking type**")
    stacking_type = st.selectbox("Interlocking or column stacking", ["Column", "Interlocking"], index=1)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.image("https://blog.robotiq.com/hs-fs/hubfs/Stacking_Column_V2.jpg?width=323&height=202&name=Stacking_Column_V2.jpg",
                 caption="Column stacking\n→ aligned vertically\n→ higher strength (factor 1.0)")
    with col_s2:
        st.image("https://blog.robotiq.com/hs-fs/hubfs/Stacking_Interlock_V2.jpg?width=323&height=202&name=Stacking_Interlock_V2.jpg",
                 caption="Interlocking stacking\n→ offset layers\n→ reduced strength (factor 0.6)")

# ───────────────────────────────────────────────
# Calculations (exact match to your Excel)
# ───────────────────────────────────────────────
inside_perimeter = 2 * (L + w)
board_thickness = flute_thickness[flute_type]

PWC_s = (pallet_weight / npl) * (Ns - 1) if npl != 0 else 0
SSp_s = (Ns * n - 1) * W + PWC_s
PWC_d = (pallet_weight / npl) * (Nd - 1) if npl != 0 else 0
SSp_d = ((Nd * n - 1) * W + PWC_d) * 3

interlock_factor = 0.6 if stacking_type == "Interlocking" else 1.0
gapped_factor = 0.8 if gapped_pallet == "Yes" else 1.0

factors = [
    interlock_factor,
    overhang_factor[overhang],
    gapped_factor,
    misalignment_factor[misalignment]
]
factors_sorted = sorted(factors)
small1 = factors_sorted[0]
small2 = factors_sorted[1]

SRF_s = (rh_factor[rh_storage] * dwell_factor[dwell_storage]) * small1 * small2
SRF_d = (rh_factor[rh_transit] * dwell_factor[dwell_transit]) * small1 * small2

CS_s = SSp_s / SRF_s if SRF_s != 0 else 0
CS_d = SSp_d / SRF_d if SRF_d != 0 else 0

max_cs = max(CS_s, CS_d)
ect = max_cs / (5.87 * math.sqrt(board_thickness * inside_perimeter)) if max_cs > 0 and board_thickness > 0 else 0

# ── Tab 4: Results ───────────────────────────────
with tab4:
    st.header("Calculation Results")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.metric("**Recommended Minimum ECT**", f"{ect:.1f} lb/in")
    with col2:
        st.metric("Controlling CS", f"{max_cs:.0f} lb", delta="Storage" if CS_s > CS_d else "Transit")

    with st.expander("Detailed breakdown", expanded=False):
        st.markdown(f"**Inside perimeter** = {inside_perimeter:.2f} in")
        st.markdown(f"**Board thickness** = {board_thickness:.4f} in")
        st.markdown("---")
        st.markdown(f"**Storage**   CS = **{CS_s:.0f}** lb    SRF = **{SRF_s:.4f}**")
        st.markdown(f"**Transit**    CS = **{CS_d:.0f}** lb    SRF = **{SRF_d:.4f}**")
        st.markdown("---")
        st.markdown(f"PWC(s) = {PWC_s:.1f} lb")
        st.markdown(f"SSp(s) = {SSp_s:.1f} lb")
        st.markdown(f"PWC(d) = {PWC_d:.1f} lb")
        st.markdown(f"SSp(d) = {SSp_d:.1f} lb")

st.caption("ECT Calculator • Armor Packaging • v1.3 • 2026")
