import tkinter
from tkinter import ttk  # 导入内部包

li = ['王记', '12', '男']
root = tkinter.Tk()
root.title('测试')
tree = ttk.Treeview(root, columns=['1', '2', '3'], show='headings')
tree.column('1', width=100, anchor='center')
tree.column('2', width=100, anchor='center')
tree.column('3', width=100, anchor='center')
tree.heading('1', text='姓名')
tree.heading('2', text='学号')
tree.heading('3', text='性别')

tree.grid()

for i in range(5):
    tree.insert('', 'end', values=li)


root.mainloop()