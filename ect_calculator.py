import streamlit as st
import math

# ───────────────────────────────────────────────
# Page config & basic look
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="RSC Box ECT Calculator",
    page_icon="📦",
    layout="wide"
)

# Some nice colors
PRIMARY = "#1E88E5"
SUCCESS = "#43A047"

# ───────────────────────────────────────────────
# Title & intro
# ───────────────────────────────────────────────
st.title("📦 RSC Box ECT Calculator")
st.markdown("Calculate the **Recommended Minimum ECT** for your Regular Slotted Container (RSC) based on pallet, storage & transit conditions.")

# ───────────────────────────────────────────────
# Main layout – two big columns
# ───────────────────────────────────────────────
left_col, right_col = st.columns([5, 4])

# ───────────────────────────────────────────────
# LEFT COLUMN ── INPUTS
# ───────────────────────────────────────────────
with left_col:
    st.header("📋 Input Parameters")

    # ── Box Information ─────────────────────────────
    with st.container(border=True):
        st.subheader("Box Information")
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input("Box length (L)", min_value=1.0, value=17.125, step=0.125, format="%.3f")
            w = st.number_input("Box width (w)", min_value=1.0, value=8.75, step=0.125, format="%.3f")
        with col2:
            W = st.number_input("Package weight (W)  lb", min_value=0.1, value=11.25, step=0.25, format="%.2f")
            flute_type = st.selectbox("Board flute type", ["C", "BC", "B"], index=0)

    # ── Pallet Load ─────────────────────────────────
    with st.container(border=True):
        st.subheader("Pallet Load")
        col1, col2, col3 = st.columns(3)
        with col1:
            n = st.number_input("Layers (n)", min_value=1, value=9, step=1)
        with col2:
            npl = st.number_input("Packages per layer (npl)", min_value=1, value=10, step=1)
        with col3:
            pallet_weight = st.number_input("Pallet weight  lb", min_value=0.0, value=45.0, step=1.0)

    # ── Stacking & Storage ──────────────────────────
    with st.container(border=True):
        st.subheader("Stacking & Storage Conditions")

        col1, col2 = st.columns(2)
        with col1:
            Ns = st.number_input("Pallets stacked in storage (Ns)", min_value=1, value=2, step=1)
            Nd = st.number_input("Pallets stacked in transit (Nd)", min_value=1, value=1, step=1)
            stacking_type = st.selectbox("Stacking type", ["Column", "Interlocking"], index=1)

        with col2:
            rh_storage = st.select_slider("RH Storage %", options=[30,35,40,45,50,55,60,65,70,75,80,85,90], value=50)
            dwell_storage = st.selectbox("Storage dwell time", ["1h.","6h.","12h.","1d.","2d.","3d.","5d.","10d.","30d.","60d.","90d.","180d.","1yr."], index=5)

    # ── Risk Factors ────────────────────────────────
    with st.expander("Risk & Handling Factors (click to expand)"):
        col1, col2 = st.columns(2)
        with col1:
            overhang = st.selectbox("Pallet overhang", ["0in.", "0.4in.", "0.8in.", "1in.", ">1in."], index=2)
            gapped_pallet = st.radio("Gapped pallet?", ["No", "Yes"], horizontal=True)
        with col2:
            misalignment = st.selectbox("Misalignment", ["0in.", "0.5in.", "1in.", "1.5in."], index=0)
            rh_transit = st.select_slider("RH Transit %", options=[30,35,40,45,50,55,60,65,70,75,80,85,90], value=45)
            dwell_transit = st.selectbox("Transit dwell time", list(dwell_factor.keys()), index=8)

# ───────────────────────────────────────────────
# RIGHT COLUMN ── RESULTS + SUMMARY
# ───────────────────────────────────────────────
with right_col:
    st.header("📊 Results")

    # ── All calculations here (same as before) ───────
    # ... paste all your dictionaries and calculation code here ...

    # Example placeholder (replace with your real calculation)
    # ect = 49.78
    # CS_s = 599.72
    # CS_d = 910.19
    # SRF_s = 0.3264
    # SRF_d = 0.2966

    # ── Nice result cards ───────────────────────────
    if 'ect' in locals():   # only show after first calculation
        st.metric("**Recommended Minimum ECT**", f"{ect:.1f}", delta=None, delta_color="normal")

        st.markdown("---")

        col_a, col_b = st.columns(2)
        col_a.metric("Controlling Compression (CS)", f"{max(CS_s, CS_d):.0f} lb")
        col_b.metric("Limiting Condition", "Storage" if CS_s > CS_d else "Transit")

        with st.expander("Detailed breakdown"):
            st.markdown(f"**Storage**   CS = **{CS_s:.0f}** lb   |   SRF = **{SRF_s:.3f}**")
            st.markdown(f"**Transit**   CS = **{CS_d:.0f}** lb   |   SRF = **{SRF_d:.3f}**")
            st.markdown(f"Inside Perimeter = **{inside_perimeter:.2f}** in")
            st.markdown(f"Board Thickness = **{board_thickness:.4f}** in")

    else:
        st.info("Fill in the inputs on the left → results will appear here")
        st.write("Tip: values update **live** as you change them!")

# ───────────────────────────────────────────────
# Footer / info
# ───────────────────────────────────────────────
st.markdown("---")
st.caption("ECT Calculator v1.1  •  made with Streamlit  •  for educational / internal use")
