from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,filedialog
from tkinter.ttk import Combobox
import time
from PIL import Image,ImageTk
import autotable_creation
import random
import sqlite3
import gmail
from tkintertable import TableCanvas, TableModel
import re
import shutil
import os

win=Tk()
win.title('My Project')
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='powder blue')

header_title=Label(win,text="Banking Automation",font=('arial',50,'bold','underline'),bg='powder blue')
header_title.pack()

current_date=time.strftime('%d-%b-%Y')

header_date=Label(win,text=current_date,font=('arial',20,'bold'),bg='powder blue',fg='blue')
header_date.pack(pady=10)

footer_title=Label(win,text="By: Paras Nath\nEmail:paras@gmail.com",font=('arial',20,'bold'),bg='powder blue')
footer_title.pack(side='bottom')

#img=Image.open('logo.jpg').resize((287,139))  #it's giving error
img=Image.open(r"D:\Python_project\logo.jpg").resize((287,139))
bitmap_img=ImageTk.PhotoImage(img,master=win)

logo_label=Label(win,image=bitmap_img)
logo_label.place(relx=0,rely=0)

def main_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2,)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.75)

    global cap
    cap=''
    def generate_captcha():
        global cap
        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,90))
        cap=cap+ch
        
        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,90))
        cap=cap+ch
        
        return cap


    def reset():
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        acn_entry.focus()
    
    def login_click():
        global uacn
        uacn=acn_entry.get()
        upass=pass_entry.get() 
        urole=role_cb.get()

        if len(uacn)==0 or len(upass)==0:
            messagebox.showerror("login","ACN or Pass can't be empty")
            return
        if captcha_entry.get()!=cap:
            messagebox.showerror("login","Invalid captcha")
            return

        uacn=int(uacn)

        if uacn==0 and upass=='admin' and urole=='Admin':
            frm.destroy()
            welcome_admin_screen()
        elif urole=='User':
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
            tup=cur_obj.fetchone()
            if tup==None:
                messagebox.showerror('login','Invalid ACN/Pass')
            else:
                global uname
                uname=tup[2]
                frm.destroy()
                welcome_user_screen()
        else:
            messagebox.showerror('login','Invalid Role')

    acn_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="ACN")
    acn_label.place(relx=.3,rely=.1)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.4,rely=.1)
    acn_entry.focus()
 
    pass_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="Pass")
    pass_label.place(relx=.3,rely=.2)

    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    pass_entry.place(relx=.4,rely=.2) 

    role_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="Role")
    role_label.place(relx=.3,rely=.3)

    role_cb=Combobox(frm,font=('arial',20,'bold'),values=['User','Admin'])
    role_cb.current(0)
    role_cb.place(relx=.4,rely=.3)

    gen_captcha_label=Label(frm,font=('arial',20,'bold'),width=7,bg='white',fg='green',text=generate_captcha())
    gen_captcha_label.place(relx=.45,rely=.4)

    captcha_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="Captcha")
    captcha_label.place(relx=.3,rely=.5)

    captcha_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    captcha_entry.place(relx=.4,rely=.5) 
        


    login_btn=Button(frm,text='login',font=('arial',20,'bold'),bg='powder blue',bd=5,command=login_click)
    login_btn.place(relx=.43,rely=.65)

    reset_btn=Button(frm,command=reset,text='reset',font=('arial',20,'bold'),bg='powder blue',bd=5)
    reset_btn.place(relx=.52,rely=.65)

    forgot_btn=Button(frm,command=forgot_password_screen,width=18,text='forgot password',font=('arial',20,'bold'),bg='powder blue',bd=5)
    forgot_btn.place(relx=.4,rely=.8)


def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.75)


    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly comfirm?')
        if resp:
            frm.destroy()
            main_screen()

    def create_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.7)
        
        def open_acn():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            uadhar=adhar_entry.get()
            ubal=0
            upass=str(random.randint(100000,999999))

            if len(uname)==0 or len(umob)==0 or len(uemail)==0 or len(uadhar)==0:
                messagebox.showerror('create','Empty fields are not allowed')
                return
            
            if not re.fullmatch('[a-zA-Z ]+',uname):
                messagebox.showerror('create','Kindly enter valid name')
                return


            if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('create','Kindly enter valid mob no')
                return
                
            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
                messagebox.showerror('create','Kindly enter valid email')
                return   

            if not re.fullmatch('[0-9]{12}',uadhar):
                messagebox.showerror('create','Kindly enter valid adhar')
                return

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into users(users_pass,users_name,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)',(upass,uname,umob,uemail,ubal,uadhar,current_date)) 
            con_obj.commit()    
            con_obj.close()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select max(users_acno) from users')
            tup=cur_obj.fetchone()
            uacn=tup[0]
            con_obj.close()

            try:
                gmail_con=gmail.GMail('theparasnath2003@gmail.com','pgtf fmyb ktby kozq')
                umsg=f'''Hello,{uname}
                Welcome to ABC Bank
                Your ACN is: {uacn}
                Your Pass is: {upass}
                kindly change your password when you login first time

                Thanks
                '''
                msg=gmail.Message(to=uemail,subject='Account Opended',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open acn','account created and kindly check your email for acn/pass')
            except:
                messagebox.showerror('open acn','something went wrong')
       
        def reset(): #
            name_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            email_entry.delete(0,"end")
            adhar_entry.delete(0,"end")
            name_entry.focus() #

     
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is create user screen",fg='purple')
        title_ifrm.pack()

        name_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Name",fg='blue')
        name_label.place(relx=.1,rely=.2)

        name_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        name_entry.place(relx=.1,rely=.27)
        name_entry.focus()


        mob_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Mob",fg='blue')
        mob_label.place(relx=.1,rely=.4)

        mob_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        mob_entry.place(relx=.1,rely=.47)

        email_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Email",fg='blue')
        email_label.place(relx=.6,rely=.2)

        email_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        email_entry.place(relx=.6,rely=.27)

        adhar_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Adhar",fg='blue')
        adhar_label.place(relx=.6,rely=.4)

        adhar_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        adhar_entry.place(relx=.6,rely=.47)

        open_btn=Button(ifrm,command=open_acn,text='open',font=('arial',20,'bold'),bg='powder blue',bd=5)
        open_btn.place(relx=.3,rely=.7)

        reset_btn=Button(ifrm,command=reset,text='reset',font=('arial',20,'bold'),bg='powder blue',bd=5)
        reset_btn.place(relx=.6,rely=.7)



    def view_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.7)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is view user screen",fg='purple')
        title_ifrm.pack()

        
        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.19,rely=.15,relwidth=.65)

        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from users")

        for tup in cur_obj: 
            data[f"{i}"]= {"Acno":tup[0], "Balance":tup[5], "Adhar":tup[6],"Opendate":tup[7],"Email":tup[4],"Mob":tup[3]}
            i+=1
        
        con_obj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)   # Load data into the model

        table = TableCanvas(frame, model=model, editable=True)
        table.show()      
     
    def delete_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.7)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is delete user screen",fg='purple')
        title_ifrm.pack()

        def delete_db():
            uacn=acn_entry.get()
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute("delete from users where users_acno=?",(uacn,))
            cur_obj.execute("delete from txn where txn_acno=?",(uacn,))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo("delete",f"User with Acn {uacn} deleted")


        acn_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="ACN",fg='blue')
        acn_label.place(relx=.3,rely=.3)

        acn_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        acn_entry.place(relx=.3,rely=.37)
        acn_entry.focus()

        delete_btn=Button(ifrm,command=delete_db,text='delete',font=('arial',20,'bold'),bg='powder blue',bd=5)
        delete_btn.place(relx=.3,rely=.6)

        reset_btn=Button(ifrm,text='reset',font=('arial',20,'bold'),bg='powder blue',bd=5)
        reset_btn.place(relx=.5,rely=.6)


    wel_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="Welcome,Admin",fg='blue')
    wel_label.place(relx=0,rely=0)

    logout_btn=Button(frm,command=logout_click,text='logout',font=('arial',20,'bold'),bg='powder blue',bd=5)
    logout_btn.place(relx=.92,rely=0)

    create_btn=Button(frm,command=create_click,width=12,text='create user',font=('arial',20,'bold'),bg='green',bd=5,fg='white')
    create_btn.place(relx=0,rely=.1)

    view_btn=Button(frm,command=view_click,width=12,text='view users',font=('arial',20,'bold'),bg='powder blue',bd=5)
    view_btn.place(relx=0,rely=.3)

    delete_btn=Button(frm,command=delete_click,width=12,text='delete user',font=('arial',20,'bold'),bg='red',bd=5,fg='white')
    delete_btn.place(relx=0,rely=.5)

def forgot_password_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2,)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.75)
    
    def back_click():
        frm.destroy()
        main_screen()

    def get_password():
        uacn=acn_entry.get()
        umob=mob_entry.get()
        uemail=email_entry.get()

        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()      
        cur_obj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacn,uemail,umob))
        tup=cur_obj.fetchone()
        con_obj.close()

        if tup==None:
            messagebox.showerror('forgot pass','Invalid Details')
        else:
            try:
                gmail_con=gmail.GMail('theparasnath2003@gmail.com','pgtf fmyb ktby kozq')
                umsg=f'''Hello,{tup[0]}
                Welcome to ABC Bank
                Your Pass is: {tup[1]}
                
                Thanks
                '''
                msg=gmail.Message(to=uemail,subject='Password Recovery',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('forgot password','kindly check your email for pass')
            except Exception as e:
                messagebox.showerror('forgot password','something went wrong')
                print(e)



    back_btn=Button(frm,command=back_click,text='back',font=('arial',20,'bold'),bg='powder blue',bd=5)
    back_btn.place(relx=0,rely=0)

    acn_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="ACN")
    acn_label.place(relx=.3,rely=.1)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.4,rely=.1)
    acn_entry.focus()
 
    email_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="Email")
    email_label.place(relx=.3,rely=.2)

    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=.4,rely=.2) 

    mob_label=Label(frm,font=('arial',20,'bold'),bg='pink',text="Mob")
    mob_label.place(relx=.3,rely=.3)

    mob_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    mob_entry.place(relx=.4,rely=.3) 

    submit_btn=Button(frm,command=get_password,text='submit',font=('arial',20,'bold'),bg='powder blue',bd=5)
    submit_btn.place(relx=.5,rely=.4)


def welcome_user_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.75)

    if os.path.exists(f"{uacn}.png"):
        img=ImageTk.PhotoImage(Image.open(f'{uacn}.png').resize((200,120)),master=win)
    else:
        img=ImageTk.PhotoImage(Image.open('default.png').resize((200,120)),master=win)   
    pic_label=Label(frm,image=img)
    pic_label.image=img
    pic_label.place(relx=.01,rely=.06)

    def update_photo():
        path=filedialog.askopenfilename()
        shutil.copy(path,f"{uacn}.png")

        img=ImageTk.PhotoImage(Image.open(path).resize((200,120)),master=win)
        pic_label=Label(frm,image=img)
        pic_label.image=img
        pic_label.place(relx=.01,rely=.06)



    btn_update_pic=Button(frm,text="update pic",command=update_photo)
    btn_update_pic.place(relx=.1,rely=.28)

    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly comfirm?')
        if resp:
            frm.destroy()
            main_screen()
       
    def check_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.75)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is check balance screen",fg='purple')
        title_ifrm.pack()

        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()      
        cur_obj.execute('select users_bal,users_opendate,users_adhar from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

        lbl_bal=Label(ifrm,text=f'Available Balance:\t\t{tup[0]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_bal.place(relx=.2,rely=.2)

        lbl_opendate=Label(ifrm,text=f'Account opendate:\t{tup[1]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_opendate.place(relx=.2,rely=.4)

        lbl_adhar=Label(ifrm,text=f'User Adhar:\t\t{tup[2]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_adhar.place(relx=.2,rely=.6)


    def update_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.75)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is update screen",fg='purple')
        title_ifrm.pack()

        def update_details():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            upass=pass_entry.get()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_name=?,users_pass=?,users_email=?,users_mob=? where users_acno=?',(uname,upass,uemail,umob,uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('update','details updated')


        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()
        

        
        name_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Name",fg='blue')
        name_label.place(relx=.1,rely=.2)

        name_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        name_entry.place(relx=.1,rely=.27)
        name_entry.insert(0,tup[2])
        name_entry.focus()


        mob_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Mob",fg='blue')
        mob_label.place(relx=.1,rely=.4)

        mob_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        mob_entry.place(relx=.1,rely=.47)
        mob_entry.insert(0,tup[3])

        email_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Email",fg='blue')
        email_label.place(relx=.6,rely=.2)

        email_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        email_entry.place(relx=.6,rely=.27)
        email_entry.insert(0,tup[4])

        pass_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text="Pass",fg='blue')
        pass_label.place(relx=.6,rely=.4)

        pass_entry=Entry(ifrm,font=('arial',18),bd=5,bg='yellow')
        pass_entry.place(relx=.6,rely=.47)
        pass_entry.insert(0,tup[1])

        update_btn=Button(ifrm,command=update_details,text='update',font=('arial',20,'bold'),bg='powder blue',bd=5)
        update_btn.place(relx=.45,rely=.7)

 
    def deposit_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.75)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is deposit screen",fg='purple')
        title_ifrm.pack()
  
        def deposit_db():
            uamt=float(amt_entry.get())
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()



            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,uacn))
            con_obj.commit()
            con_obj.close()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo("deposit",f"Amount {uamt} deposited and updated bal {ubal+uamt}")

        amt_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text="Amount",fg='blue')
        amt_label.place(relx=.25,rely=.3)

        amt_entry=Entry(ifrm,font=('arial',20),bd=5,bg='yellow')
        amt_entry.place(relx=.4,rely=.3)

        deposit_btn=Button(ifrm,command=deposit_db,text='deposit',font=('arial',20,'bold'),bg='powder blue',bd=5)
        deposit_btn.place(relx=.6,rely=.5)


    def withdraw_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.75)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is withdraw screen",fg='purple')
        title_ifrm.pack()

        def withdraw_db():
            uamt=float(amt_entry.get())
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                con_obj.commit()
                con_obj.close()

                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                con_obj.commit()
                con_obj.close()

                messagebox.showinfo("withdraw",f"Amount {uamt} withdrawn and updated bal {ubal-uamt}")
            else:
                messagebox.showerror("withdraw",f"Insufficient Bal {ubal}")



        amt_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text="Amount",fg='blue')
        amt_label.place(relx=.25,rely=.3)

        amt_entry=Entry(ifrm,font=('arial',20),bd=5,bg='yellow')
        amt_entry.place(relx=.4,rely=.3)

        withdraw_btn=Button(ifrm,command=withdraw_db,text='withdraw',font=('arial',20,'bold'),bg='powder blue',bd=5)
        withdraw_btn.place(relx=.6,rely=.5)


    def transfer_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.75)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is transfer screen",fg='purple')
        title_ifrm.pack()


        def transfer_db():
            uamt=float(amt_entry.get())
            toacn=int(to_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal,users_email from users where users_acno=?',(uacn,))
            tup=cur_obj.fetchone()
            ubal=tup[0]
            uemail=tup[1]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute("select * from users where users_acno=?",(toacn,))
                tup=cur_obj.fetchone()
                con_obj.close()

                if tup==None:
                    messagebox.showerror("transfer","To ACN does not exist")
                else:
                    otp=random.randint(1000,9999) 
                    try:
                        gmail_con=gmail.GMail('theparasnath2003@gmail.com','pgtf fmyb ktby kozq')
                        umsg=f'''Hello,{uname}
                        Welcome to ABC Bank
                        Your OTP is: {otp}
                       
                        Kindly verify this otp to complete your txn

                        Thanks
                        '''
                        msg=gmail.Message(to=uemail,subject='Account Opended',text=umsg)
                        gmail_con.send(msg)
                        messagebox.showinfo('txn','we have send otp to your registered email')
                     
                        uotp=simpledialog.askinteger("OTP","Enter OTP")
                        if otp==uotp:
                              con_obj=sqlite3.connect(database='bank.sqlite')
                              cur_obj=con_obj.cursor()
                              cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                              cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,toacn))
                            
                              con_obj.commit()
                              con_obj.close()
                                
                              tobal=tup[5]

                              con_obj=sqlite3.connect(database='bank.sqlite')
                              cur_obj=con_obj.cursor()
                              cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                              cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(toacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
                                
                              con_obj.commit()
                              con_obj.close()

                              messagebox.showinfo("transfer",f"Amount {uamt} transfered and updated bal {ubal-uamt}")
                        else:
                            messagebox.showerror('otp','Invalid OTP')
                    except:
                        messagebox.showerror('txn','something went wrong')
            else:
                messagebox.showerror("transfer",f"Insufficient Bal {ubal}")




        to_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text="To ACN",fg='blue')
        to_label.place(relx=.25,rely=.3)

        to_entry=Entry(ifrm,font=('arial',20),bd=5,bg='yellow')
        to_entry.place(relx=.4,rely=.3)

        amt_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text="Amount",fg='blue')
        amt_label.place(relx=.25,rely=.44)

        amt_entry=Entry(ifrm,font=('arial',20),bd=5,bg='yellow')
        amt_entry.place(relx=.4,rely=.44)

        transfer_btn=Button(ifrm,command=transfer_db,text='transfer',font=('arial',20,'bold'),bg='powder blue',bd=5)
        transfer_btn.place(relx=.6,rely=.6)


    def history_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.75)
        
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text="This is history screen",fg='purple')
        title_ifrm.pack()
        
        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.19,rely=.15,relwidth=.65)

        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from txn where txn_acno=?",(uacn,))

        for tup in cur_obj: 
            data[f"{i}"]= {"Txn Id":tup[0], "Txn Amt":tup[4], "Txn Date":tup[3],"Txn Type":tup[2],"Updated Bal":tup[5]}
            i+=1
        
        con_obj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)   # Load data into the model

        table = TableCanvas(frame, model=model, editable=True)
        table.show()


    wel_label=Label(frm,font=('arial',20,'bold'),bg='pink',text=f"Welcome,{uname}",fg='blue')
    wel_label.place(relx=.01,rely=0)

    logout_btn=Button(frm,command=logout_click,text='logout',font=('arial',20,'bold'),bg='powder blue',bd=5)
    logout_btn.place(relx=.92,rely=0)

    check_btn=Button(frm,command=check_click,width=15,text='check balance',font=('arial',20,'bold'),bg='purple',bd=5,fg='white')
    check_btn.place(relx=0,rely=.33)

    update_btn=Button(frm,command=update_click,width=15,text='update details',font=('arial',20,'bold'),bg='powder blue',bd=5)
    update_btn.place(relx=0,rely=.44)

    deposit_btn=Button(frm,command=deposit_click,width=15,text='deposit amt',font=('arial',20,'bold'),bg='green',bd=5,fg='white')
    deposit_btn.place(relx=0,rely=.55)

    withdraw_btn=Button(frm,command=withdraw_click,width=15,text='withdraw amt',font=('arial',20,'bold'),bg='red',bd=5,fg='white')
    withdraw_btn.place(relx=0,rely=.66)

    transfer_btn=Button(frm,command=transfer_click,width=15,text='transfer amt',font=('arial',20,'bold'),bd=5,bg='orange')
    transfer_btn.place(relx=0,rely=.77)

    history_btn=Button(frm,command=history_click,width=15,text='txn history',font=('arial',20,'bold'),bg='green',bd=5,fg='white')
    history_btn.place(relx=0,rely=.88)


main_screen()
win.mainloop()
  