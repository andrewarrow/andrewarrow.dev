import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

def create_figure_eight_animation():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Parameters for figure eight (lemniscate)
    # Parametric equations: x = a*cos(t), y = a*sin(t)*cos(t) = a*sin(2t)/2
    # Using scale factor for better visibility
    scale = 2.5
    
    # Total animation time: 60 seconds at 30 fps = 1800 frames
    total_frames = 1800
    
    # Store the trail points with colors
    trail_points = []  # Each element will be (x, y, color)
    
    # Color state tracking
    is_blue = True  # Start with blue
    previous_cos_t = 1.0  # Track previous cos(t) value to detect sign changes
    center_crossings = 0  # Count how many times we've crossed center
    
    # V color state tracking
    is_yellow = True  # Start with yellow
    previous_v_segment = -1  # Track which segment we were in to detect changes
    v_trail_points = []  # Store V trail points with colors
    
    # Create the glowing dot (starting blue)
    dot = plt.Circle((0, 0), 0.08, color='blue', alpha=1.0, zorder=10)
    ax.add_patch(dot)
    
    # Create glow effect with multiple circles
    glow_circles = []
    glow_colors = ['blue', 'lightblue', 'white']  # Start with blue glow
    glow_sizes = [0.15, 0.25, 0.35]
    glow_alphas = [0.6, 0.3, 0.1]
    
    for i in range(len(glow_colors)):
        glow = plt.Circle((0, 0), glow_sizes[i], color=glow_colors[i], 
                         alpha=glow_alphas[i], zorder=9-i)
        ax.add_patch(glow)
        glow_circles.append(glow)
    
    # Create yellow V dot and glow
    yellow_dot = plt.Circle((0, 0), 0.08, color='yellow', alpha=1.0, zorder=10)
    ax.add_patch(yellow_dot)
    
    # Create yellow glow effect
    yellow_glow_circles = []
    yellow_glow_colors = ['yellow', 'gold', 'white']
    yellow_glow_sizes = [0.15, 0.25, 0.35]
    yellow_glow_alphas = [0.6, 0.3, 0.1]
    
    for i in range(len(yellow_glow_colors)):
        yellow_glow = plt.Circle((0, 0), yellow_glow_sizes[i], color=yellow_glow_colors[i], 
                                alpha=yellow_glow_alphas[i], zorder=9-i)
        ax.add_patch(yellow_glow)
        yellow_glow_circles.append(yellow_glow)
    
    def animate(frame):
        nonlocal is_blue, previous_cos_t, center_crossings, is_yellow, previous_v_segment
        
        # Parameter t goes from 0 to 8*pi for complete figure eight
        # Complete four loops in 60 seconds (faster)
        t = (frame / total_frames) * 16 * np.pi
        
        # Figure eight parametric equations
        x = scale * np.cos(t)
        y = scale * np.sin(t) * np.cos(t)
        
        # Calculate distance from exact center (0, 0)
        distance_from_center = np.sqrt(x**2 + y**2)
        
        # For figure-eight, center crossing occurs when cos(t) = 0
        # Detect this by checking when cos(t) changes sign
        current_cos_t = np.cos(t)
        
        # Check if cos(t) crossed zero (sign change)
        if (previous_cos_t > 0 and current_cos_t < 0) or (previous_cos_t < 0 and current_cos_t > 0):
            # Increment crossing counter
            center_crossings += 1
            
            # Only toggle color every other crossing (every 2nd time)
            if center_crossings % 2 == 0:
                is_blue = not is_blue
        
        # Update previous cos(t) for next frame
        previous_cos_t = current_cos_t
        
        # Calculate current number based on total position in doubling sequence
        # Each complete loop (2*pi) goes through all 6 positions
        loop_progress = (t % (2 * np.pi)) / (2 * np.pi)
        
        # Determine position in sequence (0-5 for the 6 positions within current loop)
        position_in_loop = int(loop_progress * 6) % 6
        
        # Calculate how many complete loops we've done
        complete_loops = int(t / (2 * np.pi))
        
        # Calculate total position in the infinite doubling sequence
        # Each loop has 6 positions, so total position = complete_loops * 6 + position_in_loop
        total_position = complete_loops * 6 + position_in_loop
        
        # Calculate current number: starts at 1 and doubles for each position
        current_number = 1 * (2 ** total_position)
        
        # Update dot position
        dot.center = (x, y)
        
        # Yellow V animation - independent timeline
        # V coordinates: lower left (-2, -1.5), apex (0, 1.5), lower right (2, -1.5)
        v_t = (frame / total_frames) * 32 * np.pi  # 4x faster speed for V dot
        
        # Create path segments: 0-1 (left to apex), 1-2 (apex to right), 2-3 (right to apex), 3-4 (apex to left)
        v_progress = (v_t % (4 * np.pi)) / (4 * np.pi)  # 0 to 1 for full cycle
        
        # Determine current segment
        if v_progress < 0.25:  # Lower left to apex (segment 0)
            current_v_segment = 0
            segment_progress = v_progress / 0.25
            v_x = -2 + segment_progress * 2  # -2 to 0
            v_y = -1.5 + segment_progress * 3  # -1.5 to 1.5
        elif v_progress < 0.5:  # Apex to lower right (segment 1)
            current_v_segment = 1
            segment_progress = (v_progress - 0.25) / 0.25
            v_x = 0 + segment_progress * 2  # 0 to 2
            v_y = 1.5 - segment_progress * 3  # 1.5 to -1.5
        elif v_progress < 0.75:  # Lower right to apex (segment 2)
            current_v_segment = 2
            segment_progress = (v_progress - 0.5) / 0.25
            v_x = 2 - segment_progress * 2  # 2 to 0
            v_y = -1.5 + segment_progress * 3  # -1.5 to 1.5
        else:  # Apex to lower left (segment 3)
            current_v_segment = 3
            segment_progress = (v_progress - 0.75) / 0.25
            v_x = 0 - segment_progress * 2  # 0 to -2
            v_y = 1.5 - segment_progress * 3  # 1.5 to -1.5
        
        # Check for segment transitions to detect when we reach bottom corners
        if previous_v_segment != current_v_segment:
            # Color changes when reaching bottom left (start of segment 0) or bottom right (start of segment 2)
            if current_v_segment == 0 or current_v_segment == 2:
                is_yellow = not is_yellow
        
        # Update previous segment for next frame
        previous_v_segment = current_v_segment
        
        # Update yellow dot position
        yellow_dot.center = (v_x, v_y)
        
        # Determine current V color for new trail segments
        current_v_color = 'yellow' if is_yellow else 'lime'
        
        # Add to V trail with current color
        v_trail_points.append((v_x, v_y, current_v_color))
        
        # Keep V trail forever - don't remove any points
        # max_v_trail = 450  # Removed to keep trail forever
        # if len(v_trail_points) > max_v_trail:
        #     v_trail_points.pop(0)
        
        # Determine current color for new trail segments
        current_color = 'blue' if is_blue else 'magenta'
        
        # Add to trail with current color
        trail_points.append((x, y, current_color))
        
        # Keep trail length longer so it doesn't disappear quickly
        max_trail = 900
        if len(trail_points) > max_trail:
            trail_points.pop(0)
        
        # Clear previous trail and redraw
        ax.clear()
        ax.set_xlim(-3, 3)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        # Draw V trail with fading effect preserving each segment's color
        if len(v_trail_points) > 1:
            for i in range(1, len(v_trail_points)):
                alpha = i / len(v_trail_points) * 0.8  # Fading trail
                # Use the color that was active when this segment was drawn
                v_segment_color = v_trail_points[i][2]  # Color stored with each point
                ax.plot([v_trail_points[i-1][0], v_trail_points[i][0]], 
                       [v_trail_points[i-1][1], v_trail_points[i][1]], 
                       color=v_segment_color, alpha=alpha, linewidth=3)
        
        # Draw figure-eight trail with fading effect preserving each segment's color
        if len(trail_points) > 1:
            for i in range(1, len(trail_points)):
                alpha = i / len(trail_points) * 0.8  # Fading trail
                # Use the color that was active when this segment was drawn
                segment_color = trail_points[i][2]  # Color stored with each point
                ax.plot([trail_points[i-1][0], trail_points[i][0]], 
                       [trail_points[i-1][1], trail_points[i][1]], 
                       color=segment_color, alpha=alpha, linewidth=2)
        
        # Update dot and glow colors based on current state
        if is_blue:
            dot.set_color('blue')
            current_glow_colors = ['blue', 'lightblue', 'white']
        else:
            dot.set_color('magenta')
            current_glow_colors = ['magenta', 'pink', 'white']
        
        # Re-add glow circles with current colors
        for i, glow in enumerate(glow_circles):
            glow.center = (x, y)
            glow.set_color(current_glow_colors[i])
            ax.add_patch(glow)
        
        # Re-add main dot with current color
        dot.center = (x, y)
        ax.add_patch(dot)
        
        # Update yellow dot and glow colors based on current state
        if is_yellow:
            yellow_dot.set_color('yellow')
            current_yellow_glow_colors = ['yellow', 'gold', 'white']
        else:
            yellow_dot.set_color('lime')
            current_yellow_glow_colors = ['lime', 'green', 'white']
        
        # Re-add yellow glow circles with current colors
        for i, yellow_glow in enumerate(yellow_glow_circles):
            yellow_glow.center = (v_x, v_y)
            yellow_glow.set_color(current_yellow_glow_colors[i])
            ax.add_patch(yellow_glow)
        
        # Re-add yellow dot with current color
        yellow_dot.center = (v_x, v_y)
        ax.add_patch(yellow_dot)
        
        # Add debug text showing coordinates, distance, and cos(t)
        debug_text = f"x: {x:.3f}, y: {y:.3f}\ndist: {distance_from_center:.3f}\ncos(t): {current_cos_t:.3f}"
        #ax.text(-2.8, 1.7, debug_text, color='white', fontsize=10, 
        #        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
        
        return [dot] + glow_circles + [yellow_dot] + yellow_glow_circles
    
    # Create animation
    anim = FuncAnimation(fig, animate, frames=total_frames, interval=33.33, 
                        blit=False, repeat=True)
    
    # Save as MP4 video
    print("Saving animation... This may take a few minutes.")
    anim.save('2.mp4', writer='ffmpeg', fps=30, 
              bitrate=1800, extra_args=['-vcodec', 'libx264'])
    print("Animation saved as '2.mp4'")
    
    # Optionally show the animation
    # plt.show()
    
    return anim

if __name__ == "__main__":
    create_figure_eight_animation()
