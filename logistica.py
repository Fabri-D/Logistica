import sqlite3
from tkinter import *
from tkinter import messagebox,ttk,simpledialog


#estado: en preparacion, en camino, entregado, anulado

ven=Tk()
ven.title("Logística")
ven.config(width=500,height=500)

def cierrevenin():
    en1.delete(0,END)
    en2.delete(0,END)
    en3.delete(0,END)
    en4.delete(0,END)
    en5.delete(0,END)
    en6.delete(0,END)
    en7.delete(0,END)
    venin.withdraw()

def verenpr():
    global x,z
    lista.delete(0,END)
    x=0
    cur.execute("select * from envios where estado='en preparación'")
    y=cur.fetchall()
    z=0
    for x in y:            
        ne=str(x[1])
        apynom=x[5]
        loc=x[7]
        lista.insert(z,ne+" - "+apynom+" - "+loc)
        z=z+1

def verenca():
    global x,z
    lista.delete(0,END)
    x=0
    cur.execute("select * from envios where estado='en camino'")
    y=cur.fetchall()
    z=0
    for x in y:            
        ne=str(x[1])
        apynom=x[5]
        loc=x[7]
        lista.insert(z,ne+" - "+apynom+" - "+loc)
        z=z+1

def vercomp():
    global x,z
    lista.delete(0,END)
    x=0
    cur.execute("select * from envios where estado='entregado'")
    y=cur.fetchall()
    z=0
    for x in y:            
        ne=str(x[1])
        apynom=x[5]
        loc=x[7]
        lista.insert(z,ne+" - "+apynom+" - "+loc)
        z=z+1

def veranu():
    global x,z
    lista.delete(0,END)
    x=0
    cur.execute("select * from envios where estado='anulado'")
    y=cur.fetchall()
    z=0
    for x in y:            
        ne=str(x[1])
        apynom=x[5]
        loc=x[7]
        lista.insert(z,ne+" - "+apynom+" - "+loc)
        z=z+1
        
        
    

def neporid(ne):
    cur.execute("select id from envios where nenvio=?",(ne, ))
    a=cur.fetchone()
    if a:
        return a
    else:
        return -1

def completar():
    y=simpledialog.askstring(title="Completar Pedido",prompt="Ingrese el número de pedido:")
    if y:
        m=str(neporid(y))
        if m=="-1":
            
            messagebox.showerror(title="Error",message="No hay ningún registro con el número de envío ingresado",parent=ven)
        
        n=m[1:2]
        
        cur.execute("update envios set estado='entregado' where id=?",(n, ))
        con.commit()

def anular():
    y=simpledialog.askstring(title="Anular Pedido",prompt="Ingrese el número de pedido:")
    if y:
        m=str(neporid(y))
        if m=="-1":
            
            messagebox.showerror(title="Error",message="No hay ningún registro con el número de envío ingresado",parent=ven)
            
        n=m[1:2]
        
        cur.execute("update envios set estado='anulado' where id=?",(n, ))
        con.commit()

def encamino():
    y=simpledialog.askstring(title="En Camino",prompt="Ingrese el número de pedido:")
    if y: #cuando no es cancel ni sale con la x
        m=str(neporid(y))
        if m=="-1":
            
            messagebox.showerror(title="Error",message="No hay ningún registro con el número de envío ingresado",parent=ven)
            
        n=m[1:2]
        
        cur.execute("update envios set estado='en camino' where id=?",(n, ))
        con.commit()
    

con=sqlite3.connect("logistica.db")
cur=con.cursor()
cur.execute("select * from envios")
l=cur.fetchall()
for y in l:
    print (y)

def salir():
    s=messagebox.askyesno(title="Salir",message="¿Está seguro que desea salir?")
    if s==True:
        ven.destroy()
    if s==False:
        None


datos=[]

def guarped():
    ne=en1.get()
    suc=en2.get()
    cos=en3.get()
    dni=en4.get()
    apynom=en5.get()
    dir=en6.get()
    loc=en7.get()
    datos=[ne,suc,cos,dni,apynom,dir,loc]
    
    cur.execute("insert into envios(nenvio,sucursal,costo,dni,apellidoynombres,direccion,localidad,estado) values (?,?,?,?,?,?,?,'en preparación')",(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6]))
    con.commit()

    en1.delete(0,END)
    en2.delete(0,END)
    en3.delete(0,END)
    en4.delete(0,END)
    en5.delete(0,END)
    en6.delete(0,END)
    en7.delete(0,END)

def cancnuevo():
    en1.delete(0,END)
    en2.delete(0,END)
    en3.delete(0,END)
    en4.delete(0,END)
    en5.delete(0,END)
    en6.delete(0,END)
    en7.delete(0,END)
    venin.withdraw()

def pedido():
   venin.deiconify()


menu=Menu(ven)
menupedidos=Menu(menu, tearoff=0)
menupedidos.add_command(label="Nuevo Pedido",command=pedido)
menupedidos.add_command(label="Establecer envío en camino",command=encamino)
menupedidos.add_command(label="Completar",command=completar)
menupedidos.add_command(label="Anular",command=anular)
menupedidos.add_separator()
menupedidos.add_command(label="Salir",command=salir)
menu.add_cascade(label="Pedidos",menu=menupedidos)

menuver=Menu(menu,tearoff=0)
menuver.add_command(label="Ver pedidos en preparación",command=verenpr)
menuver.add_command(label="Ver pedidos en camino",command=verenca)
menuver.add_command(label="Ver pedidos completados",command=vercomp)
menuver.add_command(label="Ver pedidos anulados",command=veranu)
menu.add_cascade(label="Ver",menu=menuver)

consultas=Menu(menu, tearoff=0)
consultas.add_command(label="")

venin=Toplevel()
venin.title("Nuevo Pedido")
venin.config(width=320,height=300)
lbl1=Label(venin,text="Nº de envío:")
lbl1.place(x=10,y=10)
lbl2=Label(venin,text="Sucursal:")
lbl2.place(x=10,y=35)
lbl3=Label(venin,text="Costo:")
lbl3.place(x=10,y=60)
lbl4=Label(venin,text="DNI:")
lbl4.place(x=10,y=85)
lbl5=Label(venin,text="Apellido y nombre:")
lbl5.place(x=10,y=110)
lbl6=Label(venin,text="Direccion:")
lbl6.place(x=10,y=135)
lbl7=Label(venin,text="Localidad:")
lbl7.place(x=10,y=160)
en1=Entry(venin)
en1.place(x=82,y=10)
en2=Entry(venin)
en2.place(x=65,y=35)
en3=Entry(venin)
en3.place(x=52,y=60)
en4=Entry(venin)
en4.place(x=41,y=85)
en5=Entry(venin)
en5.place(x=119,y=110)
en6=Entry(venin)
en6.place(x=72,y=135)
en7=Entry(venin)
en7.place(x=73,y=160)
btn1=Button(venin,text="Guardar",command=guarped)
btn1.place(x=85,y=230)
btn2=Button(venin,text="Cancelar",command=cancnuevo)
btn2.place(x=170,y=230)
venin.protocol("WM_DELETE_WINDOW", cierrevenin)
venin.withdraw()

lista=Listbox(ven)
lista.config(width=70,height=14)
lista.place(x=30,y=150)


ven.config(menu=menu)
ven.mainloop()