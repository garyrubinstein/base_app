import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.title("🧮 Visual Base Converter")
st.write("See how the exact same value gets bundled differently depending on your base!")

# --- USER INPUTS ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    number = st.number_input("Enter a Base-10 Number:", min_value=1, max_value=200, value=75, step=1)
with col_in2:
    target_base = st.number_input("Enter Target Base to Change To:", min_value=2, max_value=10, value=6, step=1)

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

# --- NEW PERFECTLY SCALED DRAWING ENGINE ---
def draw_proportional_blocks(total_num, base, title_label, color_theme, is_base_10=False):
    # Determine bundling architecture
    if is_base_10:
        large_val = 100
        mid_val = 10
        
        num_large = total_num // large_val
        rem = total_num % large_val
        num_mid = rem // mid_val
        num_singles = rem % mid_val
        
        large_w, large_h = 10, 10
        mid_w, mid_h = 1, 10
    else:
        large_val = base * base
        mid_val = base
        
        num_large = total_num // large_val
        rem = total_num % large_val
        num_mid = rem // mid_val
        num_singles = rem % mid_val
        
        large_w, large_h = base, base
        mid_w, mid_h = 1, base

    # Set up Matplotlib Canvas 
    # Use a fixed 20x20 canvas to keep units perfectly proportional across both plots
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_aspect('equal') # FORCES 1:1 PIXEL RATIO (Squares stay squares!)
    ax.axis('off')
    
    current_x = 0.5
    current_y = 19.5 # Start drawing from top-left down
    
    # Helper to draw grid lines inside a block
    def draw_internal_grid(x, y, w, h):
        for i in range(1, w):
            ax.plot([x + i, x + i], [y, y - h], color='white', linewidth=0.8, zorder=3)
        for j in range(1, h):
            ax.plot([x, x + w], [y - j, y - j], color='white', linewidth=0.8, zorder=3)

    # 1. Draw Large Blocks (Flats: 10x10 or BxB)
    for _ in range(num_large):
        if current_x + large_w > 19.5: # Wrap line if hitting right edge
            current_x = 0.5
            current_y -= (large_h + 1.5)
            
        rect = patches.Rectangle((current_x, current_y - large_h), large_w, large_h, 
                                 edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
        ax.add_patch(rect)
        draw_internal_grid(current_x, current_y, large_w, large_h)
        current_x += large_w + 1.0

    # 2. Draw Mid Blocks (Rods: 1x10 or 1xB)
    for _ in range(num_mid):
        if current_x + mid_w > 19.5:
            current_x = 0.5
            current_y -= (mid_h + 1.5)
            
        rect = patches.Rectangle((current_x, current_y - mid_h), mid_w, mid_h, 
                                 edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
        ax.add_patch(rect)
        draw_internal_grid(current_x, current_y, mid_w, mid_h)
        current_x += mid_w + 0.8

    # 3. Draw Single Units (1x1 Squares)
    for _ in range(num_singles):
        if current_x + 1.0 > 19.5:
            current_x = 0.5
            current_y -= 2.0
            
        rect = patches.Rectangle((current_x, current_y - 1.0), 1.0, 1.0, 
                                 edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
        ax.add_patch(rect)
        current_x += 1.5

    st.subheader(title_label)
    if is_base_10:
        st.write(f"Bundles: **{num_large}** Hundreds | **{num_mid}** Tens | **{num_singles}** Ones")
    else:
        st.write(f"Bundles: **{num_large}** {large_val}s ({base}×{base}) | **{num_mid}** {mid_val}s (1×{base}) | **{num_singles}** Ones")
    st.pyplot(fig)

# Color configurations
blue_theme = {'edge': '#003366', 'face': '#3399FF'}
orange_theme = {'edge': '#CC5500', 'face': '#FF9933'}

# --- DISPLAY THE RESULT SIDE-BY-SIDE ---
st.markdown("---")
col_visual1, col_visual2 = st.columns(2)

with col_visual1:
    draw_proportional_blocks(number, 10, f"Base 10 View: {number}", blue_theme, is_base_10=True)

with col_visual2:
    draw_proportional_blocks(number, target_base, f"Base {target_base} View: {base_b_string} ({target_base})", orange_theme,
