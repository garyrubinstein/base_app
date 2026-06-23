import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.title("🧮 Visual Base Converter")
st.write("See how the exact same value gets bundled differently depending on your base!")

# --- USER INPUTS ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    number = st.number_input("Enter a Base-10 Number:", min_value=1, max_value=200, value=146, step=1)
with col_in2:
    target_base = st.number_input("Enter Target Base to Change To:", min_value=2, max_value=10, value=3, step=1)

# --- FUNCTION TO CONVERT BASE ---
def convert_from_base10(num, base):
    if num == 0:
        return [0]
    digits = []
    while num > 0:
        digits.append(num % base)
        num = num // base
    return digits[::-1]

base_b_digits = convert_from_base10(number, target_base)
base_b_string = "".join(map(str, base_b_digits))

# --- DYNAMIC MULTI-POWER DRAWING ENGINE ---
def draw_proportional_blocks(total_num, base, title_label, color_theme, is_base_10=False):
    # Calculate digits/counts for all positions from largest power down to 0
    if is_base_10:
        base = 10
        
    digits = convert_from_base10(total_num, base)
    num_positions = len(digits)
    
    # Dynamic canvas sizing based on complexity
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 26)
    ax.set_aspect('equal')
    ax.axis('off')
    
    current_x = 0.5
    current_y = 25.5
    
    def draw_internal_grid(x, y, w, h):
        if w > 1:
            for i in range(1, w):
                ax.plot([x + i, x + i], [y, y - h], color='white', linewidth=0.5, zorder=3)
        if h > 1:
            for j in range(1, h):
                ax.plot([x, x + w], [y - j, y - j], color='white', linewidth=0.5, zorder=3)

    # We iterate from the highest power down to the ones place
    summary_text = []
    
    for idx, count in enumerate(digits):
        power = num_positions - 1 - idx
        place_value = base ** power
        
        if count == 0:
            continue
            
        # Determine visual block dimensions based on the power level
        if power == 0:    # Ones
            w, h = 1, 1
        elif power == 1:  # Base^1 (Rods)
            w, h = 1, base
        elif power == 2:  # Base^2 (Flats)
            w, h = base, base
        elif power == 3:  # Base^3 (Cubes / Super-Rods)
            w, h = base * base, base
        else:             # Base^4 and above (Super-Flats)
            w, h = base * base, base * base
            
        summary_text.append(f"**{count}** (${place_value}$s)")

        # Draw the required amount of this block type
        for _ in range(count):
            # Line wrap protection
            if current_x + w > 23.5:
                current_x = 0.5
                current_y -= (max_h + 1.0)
                max_h = h
            else:
                if _ == 0: # track max height of the current structural row
                    max_h = h
                    
            rect = patches.Rectangle((current_x, current_y - h), w, h, 
                                     edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
            ax.add_patch(rect)
            draw_internal_grid(current_x, current_y, w, h)
            current_x += w + 1.0
            
        # Clean jump down to a fresh row for the next lower power level
        current_x = 0.5
        current_y -= (max_h + 1.5)

    st.markdown(title_label)
    st.write("Bundles: " + " | ".join(summary_text))
    st.pyplot(fig)

# Color configurations
blue_theme = {'edge': '#003366', 'face': '#3399FF'}
orange_theme = {'edge': '#CC5500', 'face': '#FF9933'}

# --- DISPLAY THE RESULT SIDE-BY-SIDE ---
st.markdown("---")
col_visual1, col_visual2 = st.columns(2)

with col_visual1:
    draw_proportional_blocks(number, 10, f"### **Base 10 View:** ${number}_{{10}}$", blue_theme, is_base_10=True)

with col_visual2:
    draw_proportional_blocks(number, target_base, f"### **Base {target_base} View:** ${base_b_string}_{{{target_base}}}$", orange_theme, is_base_10=False)

st.markdown("---")
st.info(f"💡 **Mathematical Proof:** \n"
        f"The configuration on the right evaluates to: " + 
        " + ".join([f"({d} × {target_base}^{len(base_b_digits)-1-i})" for i, d in enumerate(base_b_digits)]) + 
        f" = **{number}** in Base 10.")
