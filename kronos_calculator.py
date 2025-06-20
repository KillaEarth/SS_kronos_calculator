import streamlit as st
import math
import string

st.set_page_config(page_title="Kronos MP Calculator", layout="wide")
st.title("🌀 Kronos MP Calculator")

# Fixed values
BASE_MP = 3000
TRAINING_MP = 10000
ATTRIBUTE_PCT = 50
CHARLOTTE_PCT = 500

# Format MP to Alphabet Units
def format_letter_unit(value: float) -> str:
    if value < 1000:
        return f"{value:,.2f}"
    suffixes = list(string.ascii_uppercase)
    tier = int(math.log(value, 1000))
    if tier - 1 >= len(suffixes):
        return f"{value:,.2f}"
    suffix = suffixes[tier - 1]
    scaled = value / (1000 ** tier)
    return f"{scaled:.2f}{suffix} MP"

def format_percent_letter_unit(value: float) -> str:
    if value < 1000:
        return f"{value:.2f}%"
    suffixes = list(string.ascii_uppercase)
    tier = int(math.log(value, 1000))
    if tier - 1 >= len(suffixes):
        return f"{value:.2f}%"
    suffix = suffixes[tier - 1]
    scaled = value / (1000 ** tier)
    return f"{scaled:.2f}{suffix}%"

# Input Section in Expander
with st.expander("🔧 MP Inputs"):
    st.markdown("## 1. Base MP and Training MP")
    st.write("Base MP is the MP you start with, and Training MP is the MP you gain from training.")
    st.write("These are your flat values")
    st.write(f"**Base MP:** {BASE_MP} | **Training MP:** {TRAINING_MP}")
    
    st.markdown("---")
    st.markdown("## 2. Basic MP Multipliers")
    st.write("Next are the basic MP multipliers below.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Ability %")
        if "ability_inputs" not in st.session_state:
            st.session_state.ability_inputs = [0.0]
        ability_pct = 0
        for i in range(len(st.session_state.ability_inputs)):
            st.session_state.ability_inputs[i] = st.number_input(f"Ability Line {i+1} (%)", value=st.session_state.ability_inputs[i], step=10.0, key=f"ability_{i}")
            ability_pct += st.session_state.ability_inputs[i]
        b5, b6 = st.columns(2)
        with b5:
            if st.button("➕ Add Ability Line"):
                st.session_state.ability_inputs.append(0.0)
        with b6:
            if st.button("➖ Remove Ability Line") and len(st.session_state.ability_inputs) > 1:
                st.session_state.ability_inputs.pop()
        st.write(f"Total Ability: {ability_pct:.0f}%")
        

    with col2:
        has_attribute = st.checkbox("Attribute: Mana Expansion (+50%)", value=True)
        has_charlotte = st.checkbox("Charlotte Equipped (500%)", value=True)
        collection_pct = st.number_input("Collection (%)", value=55.0,step=5.0)

       
    
    st.markdown("---")
    st.markdown("## 3. Soul Parts: Gear MP% and Flat MP") # Gear % and Flat MP
    st.markdown("Configure your gear MP% and flat MP values below. You can add or remove lines as needed.")
    st.write("Make sure to input the **enhanced** values. If amount is too big (500A), just add zeroes for estimation.")

    # Gear MP% and Flat MP Inputs

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("#### Gear %")
        if "gear_pct_inputs" not in st.session_state:
            st.session_state.gear_pct_inputs = [0.0]
        gear_pct_total = 0
        for i in range(len(st.session_state.gear_pct_inputs)):
            st.session_state.gear_pct_inputs[i] = st.number_input(f"Line {i+1}", value=st.session_state.gear_pct_inputs[i], step=10.0, key=f"gear_pct_{i}")
            gear_pct_total += st.session_state.gear_pct_inputs[i]
        b1, b2 = st.columns(2)
        with b1:
            if st.button("➕ Add % Line"):
                st.session_state.gear_pct_inputs.append(0.0)
        with b2:
            if st.button("➖ Remove % Line") and len(st.session_state.gear_pct_inputs) > 1:
                st.session_state.gear_pct_inputs.pop()
                

    with g2:
        st.markdown("#### Gear Flat")
        if "gear_flat_inputs" not in st.session_state:
            st.session_state.gear_flat_inputs = [0]
        gear_flat_total = 0
        for i in range(len(st.session_state.gear_flat_inputs)):
            st.session_state.gear_flat_inputs[i] = st.number_input(f"Line {i+1}", value=st.session_state.gear_flat_inputs[i], step=1000, key=f"gear_flat_{i}")
            gear_flat_total += st.session_state.gear_flat_inputs[i]
        b3, b4 = st.columns(2)
        with b3:
            if st.button("➕ Add Flat Line"):
                st.session_state.gear_flat_inputs.append(0)
        with b4:
            if st.button("➖ Remove Flat Line") and len(st.session_state.gear_flat_inputs) > 1:
                st.session_state.gear_flat_inputs.pop()

    # Display total gear MP% and flat MP
    g3, g4 = st.columns(2)
    with g3:
        st.write(f"Total MP%: {gear_pct_total:.2f}%")    
    with g4:
        st.write(f"Total Flat MP: {gear_flat_total:,} MP")
    
    st.markdown("---")
    st.markdown("## 4. Kronos Exclusives, Face🎭, Clothing👘 & Possession")
    st.write("Select if you have Kronos Face and Clothing equipped, and input their multiplier value.")
    st.write("Both ultimates are independent multipliers, so having them both will multiply your MP by both values independently.")

    face_col, clothing_col = st.columns(2)
    with face_col:
        has_kronos_face = st.checkbox("🎭Kronos Face Equipped")
        kronos_face_pct = 0
        if has_kronos_face:
                kronos_face_pct = st.number_input("Ultimate: First God (300% - 500%)", value=500.0)

    with clothing_col:
        has_kronos_clothing = st.checkbox("👘Kronos Clothing Equipped")
        kronos_clothing_pct = 0
        if has_kronos_clothing:
            kronos_sockets = st.number_input("Jewel Sockets (1-12)", min_value=1, max_value=12, value=12)
            kronos_clothing = st.number_input("Ultimate: Twisted Destiny (30% - 50%)", min_value=30.0, max_value=50.0, value=50.0)
            kronos_clothing_pct = kronos_sockets * kronos_clothing
            st.write(f"Total: {kronos_clothing_pct:.0f}%")
 # Possession dropdown
    possession_options = {
        "No Possession": 0,
        "[2] Possession (+100%)": 100,
        "[4] Possession (+250%)": 250,
        "[8] Possession (+450%)": 450,
        "[10] Possession (+700%)": 700
        }
    selected_possession = st.selectbox("Possession Synergy Amount", list(possession_options.keys()), index=0)
    possession_pct = possession_options[selected_possession]


# --- Calculation Section ---
attribute = ATTRIBUTE_PCT if has_attribute else 0
charlotte = CHARLOTTE_PCT if has_charlotte else 0

attribute_mult = 1 + attribute / 100
collection_mult = 1 + collection_pct / 100
ability_mult = 1 + ability_pct / 100
charlotte_mult = 1 + charlotte / 100
gear_pct_mult = 1 + gear_pct_total / 100
possession_mult = 1 + possession_pct / 100
kronos_face_mult = 1 + kronos_face_pct / 100
kronos_clothing_mult = 1 + kronos_clothing_pct / 100

mp_multiplier = (
    attribute_mult *
    collection_mult *
    ability_mult *
    charlotte_mult *
    gear_pct_mult *
    possession_mult *
    kronos_face_mult *
    kronos_clothing_mult
)

base_total_mp = BASE_MP + TRAINING_MP + gear_flat_total
total_mp = base_total_mp * mp_multiplier

with st.expander("📊 Formula Breakdown"):
    st.write(f"(Base MP + Training MP + Gear Flat MP)")
    st.write("x Attribute x Collection x Ability x Charlotte x Gear MP% x Possession x Kronos Face x Kronos Clothing")
    st.write("= Total MP")
    st.write(f"= ({BASE_MP} + {TRAINING_MP} + {gear_flat_total}) x {attribute_mult:.2f} x {collection_mult:.2f} x {ability_mult:.2f} x {charlotte_mult:.0f} x {gear_pct_mult:.2f} x {possession_mult:.0f} x {kronos_face_mult:.0f} x {kronos_clothing_mult:.0f}")
    st.write(f"= {base_total_mp:,.2f} x {mp_multiplier:.4f}")
    st.write(f"= {total_mp:,.2f} MP")


st.header(f"💧 Final MP: {format_letter_unit(total_mp)}")
st.markdown(f"<p style='font-size:14px; color:gray;'>Raw MP: {total_mp:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:14px; color:gray;'>Calculated amount may deviate from your ingame value due to the ingame rounding offs.</p>", unsafe_allow_html=True)

# Conversion Check
st.markdown("---")
st.markdown("## 🧮 DMG Conversion")
st.write("Now, what is the point of all these MP without being able to convert them right?")
st.write("Kronos Weapon will give Final DMG, and Kronos Back will give ATK.")

col_conv1, col_conv2 = st.columns(2)
with col_conv1:
    has_fdmg_convert = st.checkbox("Using Kronos Weapon for Final DMG Conversion")
    fdmg_conversion_rate = 0
    if has_fdmg_convert:
        fdmg_conversion_rate = st.number_input("Ultimate: Chosen Destiny (1% - 2%)", min_value=0.0, max_value=2.0, value=1.5, step=0.1)
with col_conv2:
    has_atk_convert = st.checkbox("Using Kronos Back for ATK Conversion")
    atk_conversion_rate = 0
    if has_atk_convert:
        atk_conversion_rate = st.number_input("Ultimate: Messenger of Apocalypse (1% - 3%)", min_value=0.0, max_value=3.0, value=2.0, step=0.1)

mp_in_b = total_mp // 1_000_000
fdmg_bonus_pct = mp_in_b * fdmg_conversion_rate if has_fdmg_convert else 0
atk_bonus_pct = mp_in_b * atk_conversion_rate if has_atk_convert else 0
total_dmg_multiplier = (1 + atk_bonus_pct / 100) * (1 + fdmg_bonus_pct / 100)
total_dmg_bonus_pct = (total_dmg_multiplier - 1) * 100

st.subheader("🎯 Output")
st.write(f"🗡️ ATK Bonus: {atk_bonus_pct:.2f}% ({format_percent_letter_unit(atk_bonus_pct)})")
st.write(f"🔥 Final DMG Bonus: {fdmg_bonus_pct:.2f}% ({format_percent_letter_unit(fdmg_bonus_pct)})")
st.write(f"💥 Total DMG Increase: {total_dmg_bonus_pct:.0f}% ({format_percent_letter_unit(total_dmg_bonus_pct)})")


# --- Summary Panel ---
st.subheader("📋 Summary")
summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
with summary_col1:
    st.metric("Total MP", format_letter_unit(total_mp))
with summary_col2:
    st.metric("ATK Bonus", format_percent_letter_unit(atk_bonus_pct))
with summary_col3:
    st.metric("Final DMG Bonus", format_percent_letter_unit(fdmg_bonus_pct))
with summary_col4:
    st.metric("Total DMG Increase", format_percent_letter_unit(total_dmg_bonus_pct))

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ by KillaEarth")
st.markdown("For any issues or suggestions, feel free to reach out on Discord @KillaEarth")