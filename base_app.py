import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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

# --- ISOMETRIC 3D CUBE DRAWING ENGINE ---
def draw_isometric_cube(ax, x0, y0, size, edge_color, face_color):
    """
    Draws a single 3D perspective cube at a given screen coordinate.
    """
    # 3D Depth offsets
    dx = size * 0.4
    dy = size * 0.4
    
    # Color Shading Factors for 3D realism
    def hex_to_rgb(hex_str):
        hex_str = hex_str.lstrip('#')
        return np.array([int(hex_str[i:i+2], 16)/255.0 for i in (0, 2, 4)])
    
    def rgb_to_hex(rgb):
        return '#' + ''.join([f"{int(max(0, min(1, c))*255):02x}" for c in rgb])

    base_rgb = hex_to_rgb(face_color)
    top_color = rgb_to_hex(base_rgb * 1.15)    # Lighter
    right_color = rgb_to_hex(base_rgb * 0.80)  # Darker
    
    # 1. Front Face
    front = patches.Polygon([
        [x0, y0], [x0 + size, y0], 
        [x0 + size, y0 + size], [x0, y0 + size]
    ], edgecolor=edge_color, facecolor=face_color, zorder=4, linewidth=1)
    ax.add_patch(front)
    
    # 2. Top Face
    top = patches.Polygon([
        [x0, y0 + size], [x0 + size, y0 + size],
        [x0 + size + dx, y0 + size + dy], [x0 + dx, y0 + size + dy]
    ], edgecolor=edge_color, facecolor=top_color, zorder=5, linewidth=1)
    ax.add_patch(top)
    
    # 3. Right Face
    right = patches.Polygon([
        [x0 + size, y0], [x0 + size + dx, y0 + dy],
        [x0 + size + dx, y0 + size + dy], [x0 + size, y0 + size]
    ], edgecolor=edge_color, facecolor=right_color, zorder=4, linewidth=1)
    ax.add_patch(right)
    
    # Internal grid-lines for the front face to make it look like small units
    for i in range(1, size):
        ax.plot([x0 + i, x0 + i], [y0, y0 + size], color='white', linewidth=0.5, alpha=0.6, zorder=6)
        ax.plot([x0, x0 + size], [y0 + i, y0 + i], color='white', linewidth=0.5, alpha=0.6, zorder=6)

# --- DYNAMIC CANVAS RENDERING ENGINE ---
def draw_proportional_blocks(total_num, base, title_label, color_theme, is_base_10=False):
    if is_base_10:
        base = 10
        
    digits = convert_from_base10(total_num, base)
    num_positions = len(digits)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1, 25)
    ax.set_ylim(-1, 27)
    ax.set_aspect('equal')
    ax.axis('off')
    
    current_x = 0.5
    current_y = 24.0
    
    def draw_2d_grid(x, y, w, h):
        for i in range(1, w):
            ax.plot([x + i, x + i], [y, y - h], color='white', linewidth=0.6, zorder=3)
        for j in range(1, h):
            ax.plot([x, x + w], [y - j, y - j], color='white', linewidth=0.6, zorder=3)

    summary_text = []
    
    for idx, count in enumerate(digits):
        power = num_positions - 1 - idx
        place_value = base ** power
        
        if count == 0:
            continue
            
        summary_text.append(f"**{count}** (${place_value}$s)")

        # Execution Logic based on structural dimension requirements
        for _ in range(count):
            
            # --- LEVEL 4: Super-Flats / Rows of Cubes (Base^4) ---
            if power >= 4:
                # Render as a massive row block structure composed of 3D cubes
                cube_size = base
                block_w = (cube_size * base) + (cube_size * 0.4)
                block_h = cube_size + (cube_size * 0.4)
                
                if current_x + block_w > 24.5:
                    current_x = 0.5
                    current_y -= (block_h + 2.0)
                    
                # Create a linear sequence of 3D isometric components
                for c in range(base):
                    sub_x = current_x + (c * cube_size)
                    draw_isometric_cube(ax, sub_x, current_y - cube_size, cube_size, color_theme['edge'], color_theme['face'])
                current_x += block_w + 1.5

            # --- LEVEL 3: Standard 3D Cubes (Base^3) ---
            elif power == 3:
                cube_size = base
                block_w = cube_size + (cube_size * 0.4)
                block_h = cube_size + (cube_size * 0.4)
                
                if current_x + block_w > 24.5:
                    current_x = 0.5
                    current_y -= (block_h + 2.0)
                    
                draw_isometric_cube(ax, current_x, current_y - cube_size, cube_size, color_theme['edge'], color_theme['face'])
                current_x += block_w + 1.5

            # --- LEVEL 2: 2D Flats (Base^2) ---
            elif power == 2:
                w, h = base, base
                if current_x + w > 24.5:
                    current_x = 0.5
                    current_y -= (h + 1.5)
                rect = patches.Rectangle((current_x, current_y - h), w, h, edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
                ax.add_patch(rect)
                draw_2d_grid(current_x, current_y, w, h)
                current_x += w + 1.0

            # --- LEVEL 1: 2D Rods (Base^1) ---
            elif power == 1:
                w, h = 1, base
                if current_x + w > 24.5:
                    current_x = 0.5
                    current_y -= (h + 1.5)
                rect = patches.Rectangle((current_x, current_y - h), w, h, edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
                ax.add_patch(rect)
                draw_2d_grid(current_x, current_y, w, h)
                current_x += w + 0.8

            # --- LEVEL 0: 2D Units (Base^0) ---
            else:
                w, h = 1, 1
                if current_x + w > 24.5:
                    current_x = 0.5
                    current_y -= 2.0
                rect = patches.Rectangle((current_x, current_y - h), w, h, edgecolor=color_theme['edge'], facecolor=color_theme['face'], zorder=2)
                ax.add_patch(rect)
                current_x += 1.4
                
        # Force a clear drop down to the next row layout level
        if power >= 3:
            current
