import re
import tkinter as tk
import tkinter.ttk as ttk


class finder:
    def __init__(self):
        self.names = {}
        with open('abbr.txt') as f:
            for line in f:
                line = line[:-1]
                if line:
                    s = line.split('\t')
                    self.names[s[1]] = s[0]

    def find(self, keywords, limit=20):
        results = []
        words = keywords.split(' ')
        for item in self.names:
            if sum([1 for word in words if word.upper() in item.upper()]) == len(words):
                s_score = sum([item.upper().index(word.upper()) for word in words])
                results.append((s_score, item))
        if len(results) > limit:
            out = [x for _, x in sorted(results)][:limit]
        else:
            out = [x for _, x in sorted(results)]
        return [(full, self.names[full]) for full in out]


class win:
    def __init__(self):
        self.master = tk.Tk()
        self._setup_win()
        self.f = finder()

    def _setup_win(self):
        self.master.title('Jounal Abbreviations')
        self.master.resizable(width=False, height=False)

        self.table_header = ['full title', 'abbreviation']
        self.tree = ttk.Treeview(columns=self.table_header, show="headings")
        self.tree.grid(column=0, row=1, columnspan=2, sticky='nsew', in_=self.master)
        for col_title in self.table_header:
            self.tree.heading(col_title, text=col_title.title())

        # entries
        self.entry_var = tk.StringVar()
        self.entry_var.set('')
        self.input_entry = tk.Entry(self.master, textvariable=self.entry_var, width=80)
        self.input_entry.grid(row=0, column=1)
        self.entry_var.trace('w', lambda a, b, c: self._set_tree())

        # #  button
        # self.solve_btn = tk.Button(self.master, text="search", command=self.test)
        # self.solve_btn.grid(row=0, column=9)

        # label
        self.input_label = tk.Label(self.master, text='Enter title:')
        self.input_label.grid(row=0, column=0)


    def _set_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not self.entry_var.get():
            return
        item_list = self.f.find(self.entry_var.get(), 200)
        for item in item_list:
            self.tree.insert('', 'end', values=item)


    def run(self):
        self.master.mainloop()


w = win()
w.run()
