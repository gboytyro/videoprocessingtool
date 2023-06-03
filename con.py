import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

def select_video():
    video_file = filedialog.askopenfilename(title="Select Video File")
    video_entry.delete(0, tk.END)
    video_entry.insert(tk.END, video_file)

def select_png_sequence_folder():
    folder_path = filedialog.askdirectory(title="Select PNG Sequence Folder")
    png_sequence_entry.delete(0, tk.END)
    png_sequence_entry.insert(tk.END, folder_path)

def process_video():
    video_file = video_entry.get()
    png_sequence_folder = png_sequence_entry.get()
    output_name = output_entry.get()

    if not video_file or not png_sequence_folder or not output_name:
        messagebox.showerror("Error", "Please provide all required inputs.")
        return

    output_dir = os.path.dirname(video_file)
    output_file = os.path.join(output_dir, f"{output_name}.mp4")

    create_video(png_sequence_folder, video_file, output_file)
    add_audio(video_file, output_file)

    messagebox.showinfo("Success", f"Video processing complete. Output file saved as:\n\n{output_file}")

def create_video(png_sequence_folder, video_file, output_file):
    try:
        cmd = [
            'ffmpeg', '-framerate', str(get_frame_rate(video_file)), '-i', os.path.join(png_sequence_folder, 'frame_%04d.png'),
            '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p',
            '-s', get_video_resolution(video_file),
            output_file
        ]
        subprocess.run(cmd)
    except Exception as e:
        print("Error:", e)

def add_audio(video_file, output_file):
    try:
        cmd = [
            'ffmpeg', '-i', output_file,
            '-i', video_file, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
            '-shortest', '-y', output_file
        ]
        subprocess.run(cmd)
    except Exception as e:
        print("Error:", e)

def get_frame_rate(video_file):
    try:
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', video_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        fps = eval(result.stdout)
        return fps
    except Exception as e:
        print("Error:", e)
        return None

def get_video_resolution(video_file):
    try:
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', video_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        resolution = result.stdout.strip()
        return resolution
    except Exception as e:
        print("Error:", e)
        return None

# Create the main window
window = tk.Tk()
window.title("Video Processing")

# Create and place the input fields
video_label = tk.Label(window, text="Select Video File:")
video_label.pack()
video_entry = tk.Entry(window, width=50)
video_entry.pack()
video_button = tk.Button(window, text="Browse", command=select_video)
video_button.pack()

png_sequence_label = tk.Label(window, text="Select PNG Sequence Folder:")
png_sequence_label.pack()
png_sequence_entry = tk.Entry(window, width=50)
png_sequence_entry.pack()
png_sequence_button = tk.Button(window, text="Browse", command=select_png_sequence_folder)
png_sequence_button.pack()

output_label = tk.Label(window, text="Output Name:")
output_label.pack()
output_entry = tk.Entry(window, width=50)
output_entry.pack()

# Create and place the process button
process_button = tk.Button(window, text="Start Processing", command=process_video)
process_button.pack()

# Start the GUI event loop
window.mainloop()
