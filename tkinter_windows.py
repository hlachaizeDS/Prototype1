from tkinter import *

class Plate_plan_window:

    def __init__(self, well_list,is384):

        self.plate_plan_window = Tk()
        self.plate_plan_window.title("Plate Plan")

        self.cancel_flag=0

        if is384:
            rows = 16
            columns = 24
        else:
            rows = 8
            columns = 12

        cell_width=2
        cell_height=1

        for row in range(rows):
            row_name = Label(self.plate_plan_window, text=chr(65+row), borderwidth=1, width=cell_width, height=cell_height)
            row_name.grid(row=row+1, column=0, padx=1, pady=1)
        for col in range(columns):
            col_name = Label(self.plate_plan_window, text=col+1, borderwidth=1, width=cell_width, height=cell_height)
            col_name.grid(row=0, column=col+1, padx=1, pady=1)

        for row in range(1,rows+1):
            for col in range(1,columns+1):
                cellule = Label(self.plate_plan_window, text='', borderwidth=1, relief="solid", width=cell_width, height=cell_height)
                if (col-1) * rows + row in well_list:
                    cellule.config(bg='blue')
                cellule.grid(row=row, column=col, padx=1, pady=1)

        button_ok = Button(self.plate_plan_window, text="OK", command=self.plate_plan_window.quit, width = 5)
        button_ok.grid(row = rows + 1, column = int(columns*1/4)-1, padx = 10, pady = 10, columnspan=4)

        button_cancel = Button(self.plate_plan_window, text="Cancel", command= lambda:self.throw_cancel_error() , width = 5)
        button_cancel.grid(row = rows + 1, column = int(columns*3/4)-1, padx = 10, pady = 10, columnspan=4)

        self.plate_plan_window.mainloop()
        self.plate_plan_window.destroy()

        if self.cancel_flag:
            raise ValueError('Plate plan problem')


    def throw_cancel_error(self):
        self.cancel_flag = 1
        self.plate_plan_window.quit()
