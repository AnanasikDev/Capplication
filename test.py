import tkinter as tk

root = tk.Tk()

# Create the first button and place it on the left side
button1 = tk.Button(root, text="Button 1")
button1.pack(side=tk.LEFT)

# Create the second button and place it on the right side
button2 = tk.Button(root, text="Button 2")
button2.pack(side=tk.RIGHT)

root.mainloop()