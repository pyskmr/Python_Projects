import time
import tkinter as t
import tkinter.messagebox as message
import sqlite3 as sq

conn=sq.connect('book_store' )
curr=conn.cursor()

# print(all)
def fetch_db():
    curr.execute("SELECT * from books")
    all=curr.fetchall()
    return all


def search_clicked():
    def search_db(event):
        where_value=var.get()
        search_value=to_search.get()
        search_value='%'+search_value+'%'
        curr.execute('SELECT * FROM books WHERE {} LIKE ?'.format(where_value),(search_value,))
        '''
        we have used where value as place holder because if we pass it 
        via tupple it was replacing where ___ with 'where_Value' i.e, with quotes which we don't want.
        And the same scenario with like ___ ,but here we fixed it by concatenating % in front and back of
        search_value
        '''
        rows_fetched=curr.fetchall()
        
        results.delete('0','end')
        for row in rows_fetched:
            row_to_show=(','.join(map(lambda i:str(i),row))).title()
            results.insert(t.END,row_to_show)
        
        
    pop_search=t.Tk()
    
    
    
    ''' for option selected '''
    drop_down_choice=t.Label(pop_search)
    to_search=t.Entry(pop_search)
    s_button=t.Button(pop_search,text='search')
    def option_selected(*args):
        drop_down_choice.configure(text=var.get())
        drop_down_choice.grid(row=1,column=5)
        to_search.grid(row=1,column=6)
        s_button.grid(row=2,column=6,columnspan=2)
        s_button.bind('<Button-1>',search_db)
    
    results =t.Listbox(pop_search,width=60)
    results.grid(row=0,columnspan=4,rowspan=5)
    
    s=t.StringVar(pop_search)
    s.set('Search By')
    dis=t.Label(pop_search,text=s.get())
    dis.grid(row=0,column=5)    
        
    choices=('title','authors','year','isbn')
    var=t.StringVar()  
    var.set(choices[0]) 
    var.trace('w',option_selected)
    options=t.OptionMenu(pop_search,var,*choices)
    options.grid(row=0,column=6)
    
    pop_search.mainloop()



def add_clicked():
    def insert_data():
        try:
            row=(t_val.get(),a_val.get(),int(y_val.get()),int(I_val.get()))
            curr.execute('INSERT INTO books VALUES (?,?,?,?)',row)
            conn.commit()
            message.showinfo('succesfull',"succesfully added")
        except:
            message.showinfo('error',"new book can't be added")
        finally:
            popinsert.destroy()
    
    popinsert=t.Tk()
    popinsert.title('Enter new details')
    
    title=t.Label(popinsert,text='Title')
    title.grid(row=0,column=0,sticky=t.W)

    year=t.Label(popinsert,text='Year')
    year.grid(row=1,column=0,sticky=t.W)
    
    t_val=t.Entry(popinsert)
    t_val.grid(row=0,column=1)
    
    y_val=t.Entry(popinsert)
    y_val.grid(row=1,column=1)
    
    author=t.Label(popinsert,text='Author')
    author.grid(row=0,column=2,sticky=t.W)
    
    ISBN=t.Label(popinsert,text='ISBN')
    ISBN.grid(row=1,column=2,sticky=t.W)
    
    a_val=t.Entry(popinsert)
    a_val.grid(row=0,column=3)
    
    I_val=t.Entry(popinsert)
    I_val.grid(row=1,column=3)
    
    final=t.Button(popinsert,text="ADD",command=insert_data)
    final.grid(row=3,columnspan=4)
    
    popinsert.mainloop()
 

def update_data(selected):
    def update_db():
        try:
            new_vals=(t_val.get(),a_val.get(),int(y_val.get()),int(i_val.get()),old_isbn)
            curr.execute('''UPDATE books
                    SET title = ?,
                    authors = ?,
                    year = ?,
                    isbn = ?
                    WHERE isbn = ?
                ''',new_vals)
            message.showinfo('succesfull',"succesfully updated")
        except:
            
            message.showinfo('error','UPDATE ERROR')
        finally:
            pop_update.destroy()
        
    old_isbn=selected[3]
    
    pop_update=t.Tk()
    pop_update.title('Edit your data')

    title=t.Label(pop_update,text='TITLE')
    title.grid(row = 0,column=0)
    
    author=t.Label(pop_update,text='AUTHOR')
    author.grid(row=0,column=1)
    
    year=t.Label(pop_update,text='YEAR')
    year.grid(row=0,column=2)
    
    isbn=t.Label(pop_update,text='ISBN')
    isbn.grid(row=0,column=3)
    
    t_val=t.Entry(pop_update)
    t_val.insert(t.END, selected[0])
    t_val.grid(row=1,column=0)
    
    
    a_val=t.Entry(pop_update)
    a_val.insert(t.END, selected[1])
    a_val.grid(row=1,column=1)
    
    y_val=t.Entry(pop_update)
    y_val.insert(t.END, selected[2])
    y_val.grid(row=1,column=2)
    
    i_val=t.Entry(pop_update)
    i_val.insert(t.END, selected[3])
    i_val.grid(row=1,column=3)
    
    update_val=t.Button(pop_update,text='UPDATE',command=update_db)
    update_val.grid(row=2,columnspan=4)
    
    
    pop_update.mainloop()
    conn.commit()


def delete_data(isbn):
    conn.execute('DELETE FROM books WHERE ISBN = ?',isbn)
    conn.commit()
