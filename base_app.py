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

# --- FUNCTION TO CONVERT AND EXTRACT DIGITS ---
def convert_from_base10(num, base):
    if num == 0:
        return [0]
    digits = []
    while num > 0:
        digits.append(num % base)
        num = num // base
    return digits[::-1]  # Reverse to get reading order (left-to-right)

base_b_digits = convert_from_base10(number, target_base)
base_b_string = "".join(map(str, base_b_digits))

# --- RENDERING THE VISUAL BLOCKS ---
def draw_blocks(total_num, base, title_label, is_base_10=False):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    x_offset = 0.5
    y_offset = 0.5
    
    if is_base_10:
        tens = total_num // 10
        ones = total_num % 10
        
        # Draw Tens (10x1 rectangles)
        for i in range(tens):
            if x_offset > 11: # Wrap to next row if too wide
                x_offset = 0.5
                y_offset += 2.5
            rect = patches.Rectangle((x_offset, y_offset), 1.0, 2.0, edgecolor='blue', facecolor='lightblue', alpha=0.7)
            ax.add_patch(rect)
            ax.text(x_offset + 0.5, y_offset + 1.0, "10", ha='center', va='center', fontsize=10, weight='bold')
            x_offset += 1.3
            
        # Draw Ones (1x1 squares)
        x_offset += 0.5
        for i in range(ones):
            if x_offset > 11:
                x_offset = 0.5
                y_offset += 1.5
            sq = patches.Rectangle((x_offset, y_offset), 0.6, 0.6, edgecolor='darkblue', facecolor='royalblue', alpha=0.5)
            ax.add_patch(sq)
            x_offset += 0.8
            
        st.subheader(title_label)
        st.write(f"Structure: **{tens}** bundles of ten, and **{ones}** single units.")
        st.pyplot(fig)
        
    else:
        # Dynamic calculation based on Target Base
        # We handle up to 3 positions: Base^2 (Grid), Base^1 (Rectangle), Base^0 (Square)
        b_squared = base * base
        
        num_grids = total_num // b_squared
        remainder = total_num % b_squared
        num_rects = remainder // base
        num_ones = remainder % base
        
        # Draw Grids (Base x Base)
        for i in range(num_grids):
            rect = patches.Rectangle((x_offset, y_offset), 2.0, 2.0, edgecolor='red', facecolor='salmon', alpha=0.7)
            ax.add_patch(rect)
            ax.text(x_offset + 1.0, y_offset + 1.0, f"{base}×{base}\n({b_squared})", ha='center', va='center', fontsize=9, weight='bold')
            x_offset += 2.4
            
        # Draw Rectangles (Base x 1)
        x_offset += 0.2
        for i in range(num_rects):
            rect = patches.Rectangle((x_offset, y_offset), 0.8, 1.8, edgecolor='darkorange', facecolor='orange', alpha=0.6)
            ax.add_patch(rect)
            ax.text(x_offset + 0.4, y_offset + 0.9, f"{base}", ha='center', va='center', fontsize=9, weight='bold')
            x_offset += 1.1
            
        # Draw Ones (1x1 squares)
        x_offset += 0.2
        for i in range(num_ones):
            sq = patches.Rectangle((x_offset, y_offset), 0.5, 0.5, edgecolor='brown', facecolor='wheat', alpha=0.8)
            ax.add_patch(sq)
            x_offset += 0.7
            
        st.subheader(title_label)
        st.write(f"Structure: **{num_grids}** grids of {b_squared}, **{num_rects}** columns of {base}, and **{num_ones}** single units.")
        st.pyplot(fig)

# --- DISPLAY THE RESULT SIDE-BY-SIDE ---
st.markdown("---")
col_visual1, col_visual2 = st.columns(2)

with col_visual1:
    draw_blocks(number, 10, f"Standard Base 10 View: {number}", is_base_10=True)

with col_visual2:
    draw_blocks(number, target_base, f"Base {target_base} View: {base_b_string}₂", is_base_10=False)

st.markdown("---")
st.info(f"💡 **Mathematical Proof:** In Base {target_base}, the digits represent positions from right to left.  \n"
        f"Therefore: {base_b_string} is calculated as: " + 
        " + ".join([f"({d} × {target_base}^{len(base_b_digits)-1-i})" for i, d in enumerate(base_b_digits)]) + 
        f" = **{number}** in Base 10.")
