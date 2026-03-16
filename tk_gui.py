import tkinter as tk
root = tk.Tk()
frm = tk.Frame(root, padx =10, pady =10,background = 'grey')
frm.grid()
"""
tk.Entry(frm).grid(column=1, row=0)
tk.Label(frm, text="Hello World!").grid(column=0, row=0)
tk.Button(frm, text="Quit", command=root.destroy).grid(column=3, row=0)
"""
cell_size =10
for y in range(9):
    for x in range(9):
        entry = tk.Entry(frm, width=2, font=("Arial", 18), justify='center')
        entry.grid(row=y, column=x, padx=((3,1) if x % 3 == 0 else 1), pady=((3,1) if y % 3 == 0 else 1), ipadx=2,ipady=2)

root.mainloop()