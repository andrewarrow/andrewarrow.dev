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
    total_frames = 180
    
    # Store the trail points
    trail_x = []
    trail_y = []
    
    # Create the glowing dot
    dot = plt.Circle((0, 0), 0.08, color='cyan', alpha=1.0, zorder=10)
    ax.add_patch(dot)
    
    # Create glow effect with multiple circles
    glow_circles = []
    glow_colors = ['cyan', 'lightcyan', 'white']
    glow_sizes = [0.15, 0.25, 0.35]
    glow_alphas = [0.6, 0.3, 0.1]
    
    for i in range(len(glow_colors)):
        glow = plt.Circle((0, 0), glow_sizes[i], color=glow_colors[i], 
                         alpha=glow_alphas[i], zorder=9-i)
        ax.add_patch(glow)
        glow_circles.append(glow)
    
    def animate(frame):
        # Parameter t goes from 0 to 8*pi for complete figure eight
        # Complete four loops in 60 seconds (faster)
        t = (frame / total_frames) * 16 * np.pi
        
        # Figure eight parametric equations
        x = scale * np.cos(t)
        y = scale * np.sin(t) * np.cos(t)
        
        # Update dot position
        dot.center = (x, y)
        
        # Update glow positions
        for glow in glow_circles:
            glow.center = (x, y)
        
        # Add to trail
        trail_x.append(x)
        trail_y.append(y)
        
        # Keep trail length longer so it doesn't disappear quickly
        max_trail = 900
        if len(trail_x) > max_trail:
            trail_x.pop(0)
            trail_y.pop(0)
        
        # Clear previous trail and redraw
        ax.clear()
        ax.set_xlim(-3, 3)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        # Draw trail with fading effect
        if len(trail_x) > 1:
            for i in range(1, len(trail_x)):
                alpha = i / len(trail_x) * 0.8  # Fading trail
                ax.plot([trail_x[i-1], trail_x[i]], [trail_y[i-1], trail_y[i]], 
                       color='cyan', alpha=alpha, linewidth=2)
        
        # Re-add glow circles
        for i, glow in enumerate(glow_circles):
            glow.center = (x, y)
            ax.add_patch(glow)
        
        # Re-add main dot
        dot.center = (x, y)
        ax.add_patch(dot)
        
        # Add numbers on the sides
        # Right side: 1, 2, 4
        ax.text(2.8, 1.5, '4', color='white', fontsize=20, ha='center', va='center')
        ax.text(2.8, 0, '2', color='white', fontsize=20, ha='center', va='center')
        ax.text(2.8, -1.5, '1', color='white', fontsize=20, ha='center', va='center')
        
        # Left side: 8, 16, 32
        ax.text(-2.8, 1.5, '32', color='white', fontsize=20, ha='center', va='center')
        ax.text(-2.8, 0, '16', color='white', fontsize=20, ha='center', va='center')
        ax.text(-2.8, -1.5, '8', color='white', fontsize=20, ha='center', va='center')
        
        return [dot] + glow_circles
    
    # Create animation
    anim = FuncAnimation(fig, animate, frames=total_frames, interval=33.33, 
                        blit=False, repeat=True)
    
    # Save as MP4 video
    print("Saving animation... This may take a few minutes.")
    anim.save('figure_eight_animation.mp4', writer='ffmpeg', fps=30, 
              bitrate=1800, extra_args=['-vcodec', 'libx264'])
    print("Animation saved as 'figure_eight_animation.mp4'")
    
    # Optionally show the animation
    # plt.show()
    
    return anim

if __name__ == "__main__":
    create_figure_eight_animation()
