import csv
import os
import tkinter
from tkinter import *
from tkinter import ttk,filedialog,messagebox
import pymysql
import time
from tkcalendar import DateEntry


class DataEntryForm:
    def __init__(self,root):
        self.root=root
        self.root.title("Xalq Hayat Investment Payments")
        self.root.geometry("1200x500")
        self.root.config(background="gainsboro")

        Tarix=StringVar()
        QeydiyyatNo=StringVar()
        Emitent=StringVar()
        Aciqlama=StringVar()
        Mebleg=StringVar()
        ID=StringVar()
        Axtar=StringVar()
        l5=StringVar()


        MainFrame = Frame(self.root, bd=10, width=1360, height=700, relief=RIDGE)
        MainFrame.grid()

        TopFrame1 = Frame(MainFrame, bd=5, width=1350, height=200, relief=RIDGE, bg='cadet blue')
        TopFrame1.grid(row=0, column=0)
        TopFrame2 = Frame(MainFrame, bd=5, width=1350, height=200, relief=RIDGE, bg='cadet blue')
        TopFrame2.grid(row=1, column=0)
        TopFrame3 = Frame(MainFrame, bd=5, width=1340, height=300, relief=RIDGE, bg='cadet blue')
        TopFrame3.grid(row=2, column=0)

        InnerTopFrame1 = Frame(TopFrame1, bd=5, width=1350, height=220, relief=RIDGE)
        InnerTopFrame1.grid()
        InnerTopFrame2 = Frame(TopFrame2, bd=5, width=1350, height=48, relief=RIDGE)
        InnerTopFrame2.grid()
        InnerTopFrame3 = Frame(TopFrame3, bd=5, width=1350, height=280, relief=RIDGE)
        InnerTopFrame3.grid()

        Tarix.set(time.strftime("%Y-%m-%d"))

        l2 = tkinter.Label(root, font=('Times', 15, 'bold'), fg='red')
        l2.place(relx=0.78, rely=0.50, anchor="n")
        l2.grid()

        def Reset():
            Tarix.set("")
            QeydiyyatNo.set("")
            Emitent.set("")
            Aciqlama.set("")
            Mebleg.set("")
            ID.set("")
            Axtar.set("")
            Tarix.set(time.strftime("%d/%m/%Y"))
            l5.set("")

        def iExit():
            iExit=tkinter.messagebox.askyesno("Data Entry Form","Confirm if you want to exit.")
            if iExit>0:
                root.destroy()
                return


        def addData():
            if Tarix.get()=="" or QeydiyyatNo.get()=="" or Mebleg.get()=="":
                tkinter.messagebox.showerror("Data Entry Form","Melumatlar tam daxil edilmeyib.")
            else:
                sqlCon=pymysql.connect(host="localhost",user="root",password="Musfiq1989",database="gelirler")
                cur=sqlCon.cursor()
                cur.execute("insert into gelirler.invpayments values(%s,%s,%s,%s,%s,%s)",(
                            Tarix.get(),
                            QeydiyyatNo.get(),
                            Emitent.get(),
                            Aciqlama.get(),
                            Mebleg.get(),
                            ID.set("")))
                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Data Entry Form", "Record Entered Successfully")

        def DisplayData():
            sqlCon = pymysql.connect(host="localhost", user="root", password="Musfiq1989", database="gelirler")
            cur = sqlCon.cursor()
            cur.execute("select * from gelirler.invpayments")
            result=cur.fetchall()
            if len(result)!=0:
                global count
                count = 0
                total = 0
                tree_records.delete(*tree_records.get_children())
                for row in result:
                    tree_records.insert('',END,values=row)
                    count += 1
                    total =round(total +row[4],2)
                    l2.config(text="Toplam: " + str(total) + " AZN")
            sqlCon.commit()
            sqlCon.close()

        def LearnersInfo(ev):
            viewInfo=tree_records.focus()
            learnerData=tree_records.item(viewInfo)
            row=learnerData['values']
            Tarix.set(row[0])
            QeydiyyatNo.set(row[1])
            Emitent.set(row[2])
            Aciqlama.set(row[3])
            Mebleg.set(row[4])
            ID.set(row[5])

        def update():
            sqlCon = pymysql.connect(host="localhost", user="root", password="Musfiq1989", database="gelirler")
            cur = sqlCon.cursor()
            cur.execute("update invpayments set Tarix=%s,QeydiyyatNo=%s,Emitent=%s,Aciqlama=%s,Mebleg=%s where ID=%s",(
                Tarix.get(),
                QeydiyyatNo.get(),
                Emitent.get(),
                Aciqlama.get(),
                Mebleg.get(),
                ID.get()
            ))
            sqlCon.commit()
            DisplayData()
            sqlCon.close()
            tkinter.messagebox.showinfo("Data Entry Form", "Record Successfully Updated")


        def deleteDB():
            deleteDB = tkinter.messagebox.askyesno("Data Entry Form", "Melumatin silinecek.")
            if deleteDB>0:
                sqlCon = pymysql.connect(host="localhost", user="root", password="Musfiq1989", database="gelirler")
                cur = sqlCon.cursor()
                cur.execute("delete from invpayments where ID=%s",ID.get())

                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Data Entry Form", "Record Successfully Deleted")
                DisplayData()

        def searchDB():
            try:
                sqlCon = pymysql.connect(host="localhost", user="root", password="Musfiq1989", database="gelirler")
                cur = sqlCon.cursor()
                cur.execute("select * from invpayments where QeydiyyatNo='%s'" % Axtar.get())
                result=cur.fetchall()
                if len(result) != 0:
                    global count
                    count = 0
                    total = 0
                    tree_records.delete(*tree_records.get_children())
                    for row in result:
                        tree_records.insert('',END,values=row)
                        count += 1
                        total =round(total +row[4],2)
                        l2.config(text="Toplam: " + str(total) + " AZN")
                    sqlCon.commit()
            except:
                tkinter.messagebox.showinfo("Data Entry Form", "No Such Record Found")
                Reset()
            sqlCon.close()
            Axtar.set("")
#===========================================================================================================================================================================

        lblTarix = Label(InnerTopFrame1, font=('arial', 12, 'bold'), text="Tarix", bd=10)
        lblTarix.grid(row=0, column=0, sticky=W)
        txtAlinmaTarixi = Entry(InnerTopFrame1, font=('arial', 12, 'bold'), bd=5, width=28, justify='left',
                                textvariable=Tarix)
        txtAlinmaTarixi.grid(row=0, column=1)

        lblQeydiyyatNom = Label(InnerTopFrame1, font=('arial', 12, 'bold'), text="QK Qeydiyyat Nöm", bd=10)
        lblQeydiyyatNom.grid(row=1, column=0, sticky=W)
        txtQeydiyyatNom = Entry(InnerTopFrame1, font=('arial', 12, 'bold'), bd=5, width=28, justify='left',
                                textvariable=QeydiyyatNo)
        txtQeydiyyatNom.grid(row=1, column=1)

        lblEmitent= Label(InnerTopFrame1, font=('arial', 12, 'bold'), text="Emitentin Adi", bd=10)
        lblEmitent.grid(row=0, column=2, sticky=W)
        txtEmitent= Entry(InnerTopFrame1, font=('arial', 12, 'bold'), bd=5, width=28, justify='left',
                              textvariable=Emitent)
        txtEmitent.grid(row=0, column=3)

        lblAciqlama = Label(InnerTopFrame1, font=('arial', 12, 'bold'), text="Aciqlama", bd=10)
        lblAciqlama.grid(row=1, column=2, sticky=W)
        txtAciqlama = Entry(InnerTopFrame1, font=('arial', 12, 'bold'), bd=5, width=35, justify='left',
                           textvariable=Aciqlama)
        txtAciqlama.grid(row=1, column=3)

        lblMebleg = Label(InnerTopFrame1, font=('arial', 12, 'bold'), text="Mebleg", bd=10)
        lblMebleg.grid(row=2, column=2, sticky=W)
        txtMebleg = Entry(InnerTopFrame1, font=('arial', 12, 'bold'), bd=5, width=28, justify='left',
                            textvariable=Mebleg)
        txtMebleg.grid(row=2, column=3)

        lblID = Label(InnerTopFrame1, font=('arial', 12, 'bold'), text="ID", bd=10)
        lblID.grid(row=2, column=0, sticky=W)
        txtID = Label(InnerTopFrame1, font=('arial', 12, 'bold'), bd=5, width=28, justify='left',
                                textvariable=ID)
        txtID.grid(row=2, column=1)

        self.lblAxtarMedaxil = Label(InnerTopFrame2, font=('arial', 12, 'bold'), text="Axtar(Qeydiyyat No)", bd=10)
        self.lblAxtarMedaxil.grid(row=1, column=2, sticky=W)
        self.txtAxtarMedaxil = Entry(InnerTopFrame2, font=('arial', 12, 'bold'), width=28, textvariable=Axtar)
        self.txtAxtarMedaxil.grid(row=1, column=3)

        lblDateSearch = Label(InnerTopFrame2, font=('arial', 12, 'bold'), text="Tarix ile Axtar", bd=10)
        lblDateSearch.grid(row=6, column=2, sticky=W)




#==============================================================================================================================================================================
        scroll_x=Scrollbar(InnerTopFrame3,orient=HORIZONTAL)
        scroll_y=Scrollbar(InnerTopFrame3,orient=VERTICAL)

        tree_records=ttk.Treeview(InnerTopFrame3,height=17,columns=("Tarix","QeydiyyatNo","Emitent","Aciqlama","Mebleg","ID"),
                                  xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set,selectmode="extended")
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        tree_records.heading("Tarix", text="Tarix")
        tree_records.heading("QeydiyyatNo", text="Qeydiyyat No")
        tree_records.heading("Emitent", text="Emitent")
        tree_records.heading("Aciqlama", text="Aciqlama")
        tree_records.heading("Mebleg", text="Mebleg")
        tree_records.heading("ID", text="ID")

        tree_records['show'] = 'headings'
        tree_records.column("Tarix", width=80,anchor='c')
        tree_records.column("QeydiyyatNo", width=150,anchor='c')
        tree_records.column("Emitent", width=150,anchor='c')
        tree_records.column("Aciqlama",width=300,anchor='c')
        tree_records.column("Mebleg",width=150,anchor='c')
        tree_records.column("ID", width=80,anchor='c')

        tree_records.pack(fill=BOTH,expand=1)
        tree_records.bind("<ButtonRelease-1>", LearnersInfo)
        DisplayData()

        l5 = tkinter.Label(InnerTopFrame2, font=('Times', 15, 'bold'), fg='red')
        l5.grid(row=8,column=2)

        # ADDING SEARCH BY DATE
        # 1st Date Entry box
        sel = tkinter.StringVar()
        cal = DateEntry(InnerTopFrame2, selectmode='day', textvariable=sel, date_pattern="dd.mm.y")
        cal.grid(row=6, column=3, sticky=W)
        sel1 = tkinter.StringVar()
        cal1 = DateEntry(InnerTopFrame2, selectmode='day', textvariable=sel1, date_pattern="dd.mm.y")
        cal1.grid(row=7, column=3, sticky=W)

        def my_upd(*args):
            if (len(sel.get() and sel1.get()) > 3):
                dt = cal.get_date()
                dt3 = cal1.get_date()

                for record in tree_records.get_children():
                    tree_records.delete(record)

                sqlCon = pymysql.connect(host="localhost", user="root", password="Musfiq1989", database="gelirler")
                cur = sqlCon.cursor()
                cur.execute("SELECT * FROM invpayments WHERE Tarix BETWEEN '%s' AND '%s'"  % (dt, dt3))
                result = cur.fetchall()
                global count
                count = 0
                total = 0
                for row in result:
                    tree_records.insert('', END, values=row)
                    count += 1
                    total =round(total +row[4],2)
                    l5.config(text="Toplam: " + str(total) + " AZN")
                    sqlCon.commit()
                sqlCon.close()

        sel1.trace('w', my_upd)

#===================================================================================================================================================

        self.btnAddNew = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13,
                                text='Ödəniş Əlave et', fg='white', bg='DarkGreen', activebackground='DarkGreen',
                                command=addData)
        self.btnAddNew.grid(row=0, column=0, padx=3)

        self.btnDisplay = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13,
                                 text='Bütün Ödənişlər', fg='white', bg='cornflowerblue',
                                 activebackground='cornflowerblue', command=DisplayData)
        self.btnDisplay.grid(row=0, column=1, padx=3)

        self.btnUpdate = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13,
                                text='Düzəliş Et', fg='white', bg='cornflowerblue',
                                activebackground='cornflowerblue',
                                command=update)
        self.btnUpdate.grid(row=0, column=2, padx=3)

        self.btnReset = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13, text='Sıfırla',
                               fg='white', bg='cornflowerblue', activebackground='cornflowerblue', command=Reset)
        self.btnReset.grid(row=0, column=3, padx=3)

        self.btnSearch = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13,
                                text='Axtar(Qeyd.No)',
                                fg='white', bg='cornflowerblue', activebackground='cornflowerblue', command=searchDB)
        self.btnSearch.grid(row=0, column=5, padx=3)

        self.btnExit = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13, text='Çıxış',
                              fg='white', bg='darkred', activebackground='darkred', command=iExit)
        self.btnExit.grid(row=0, column=6, padx=3)

        self.btnDelete = Button(InnerTopFrame2, pady=1, bd=4, font=('Times', 14, 'bold'), width=13, text='Melumatı Sil',
                                fg='white', bg='darkred', activebackground='darkred', command=deleteDB)
        self.btnDelete.grid(row=0, column=7, padx=3)


if __name__=='__main__':
    root=Tk()
    application=DataEntryForm(root)
    root.mainloop()