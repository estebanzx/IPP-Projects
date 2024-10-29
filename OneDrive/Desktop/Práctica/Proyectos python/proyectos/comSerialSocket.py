import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import serial
import time

serialPort1 = serial.Serial()

ventana = tk.Tk()
ventana.resizable(0,0)

textEstado = tk.Text(ventana, state="normal")
textEstado.insert(tk.END, "Desconectado")
textEstado.config(state="disabled")
textEstado.align = "center"

TextEnviar = tk.Text(ventana, state="disabled")
TextEnviar.pack()

TextRecibidos = tk.Text(ventana, state="disabled")
TextRecibidos.pack()


ventana.title("Comunicación Serial")
ventana.geometry("485x390")

comboBox1 = ttk.Combobox(ventana, state="readonly", values=["COM1","COM2","COM3","COM4","COM5","COM6","COM7"])
comboBox1.set("COM1")
comboBox1.place(x=160, y=40, width=140, height=22)
comboBox1.set("Seleccionar puerto")

comboBox2 = ttk.Combobox(ventana, state="readonly", values=[0,1,2,3,4,5,6,7,8,9])
comboBox2.set("0")
comboBox2.place(x=160, y=60, width=140, height=22)

def click_pcplc():
    try:
        if serialPort1.isOpen():
            serialPort1.write(b"Run PCPLC"+b"\r")
            time.sleep(2)
            TextEnviar.delete(1.0, tk.END)
            TextRecibidos.delete(1.0, tk.END)
            Recibir = serialPort1.read_all()
            TextRecibidos.insert(tk.END, Recibir.decode("utf-8"))
            messagebox.showinfo(message="Mensaje enviado", title="Resultado")
        else:
            messagebox.showerror("Error", "El puerto serial no está abierto.")
    except serial.SerialException as e:
            messagebox.showerror("Error", f"Error al enviar el mensaje: {e}")

def click_a():
    serialPort1.write(b"Run A"+b"\r")
    time.sleep(2)
    TextEnviar.delete(1.0, tk.END)
    TextRecibidos.delete(1.0, tk.END)
    Recibir = serialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

def click_ttsib():
    serialPort1.write(b"Run ppnb"+b"\r")
    time.sleep(2)
    TextEnviar.delete(1.0, tk.END)
    TextRecibidos.delete(1.0, tk.END)
    Recibir = serialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

def click_click_off():
    serialPort1.write(b"coff"+b"\r")
    time.sleep(2)
    TextEnviar.delete(1.0, tk.END)
    TextRecibidos.delete(1.0, tk.END)
    Recibir = serialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

def click_move():
    serialPort1.write(b"Move 0"+b"\r")
    time.sleep(2)
    TextEnviar.delete(1.0, tk.END)
    TextRecibidos.delete(1.0, tk.END)
    Recibir = serialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

def click_open():
    serialPort1.write(b"Open"+b"\r")
    time.sleep(2)
    TextEnviar.delete(1.0, tk.END)
    TextRecibidos.delete(1.0, tk.END)
    Recibir = serialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

def click_close():
    serialPort1.write(b"Close"+b"\r")
    time.sleep(2)
    TextEnviar.delete(1.0, tk.END)
    TextRecibidos.delete(1.0, tk.END)
    Recibir = serialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

def click_conectar():
    try:
        if not serialPort1.isOpen() == False:
            serialPort1.baudrate = 9600
            serialPort1.bytesize = 8
            serialPort1.parity = 'N'
            serialPort1.stopbits = serial.STOPBITS_ONE
            serialPort1.port = comboBox1.get()
            serialPort1.open()
            textEstado["state"] = "normal"
            textEstado.configure(background="LIME")
            messagebox.showinfo(message="Puerto Conectado ")
            textEstado["state"] = "disable"
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error al conectar el puerto: {e}")
        textEstado["state"] = "normal"
        textEstado.delete(1.0, tk.END)
        textEstado.insert(tk.END, "Error de conexión")
        textEstado.configure(background="RED")
        textEstado["state"] = "disabled"


def click_desconectar():
    if serialPort1.isOpen() == True:
        serialPort1.close()
        textEstado["state"] = "normal"
        textEstado.delete(1.0, tk.END)
        textEstado.insert(tk.END, "Desconectado")
        textEstado.configure(background="RED")
        messagebox.showinfo(message="Puerto Desconectado")
        textEstado["state"] = "disabled"

# def click_enviar():
#     try:
#         serialPort1.write(TextEnviar.get().encode()+b"\r")
#         time.sleep(2)
#         messagebox.showinfo(message="Mensaje enviado", title="Resultado")
#         aux = serialPort1.read_all()
#         if b"Done." in aux:
#             TextRecibidos.insert(1.0, b"Done.\n")
#     except serial.SerialException as e:
#         messagebox.showerror("Error", f"Error al enviar el mensaje: {e}")

def click_enviar():
    msj = TextEnviar.get(1.0, tk.END)
    lista = msj.split("\n")
    for x in lista:
        a = 0 
        if x == "":
            pass
        elif x.__contains__("Run"):
            serialPort1.write(x.encode()+b"\r")
            while(a==0):
                aux = serialPort1.read_all()
                if b"ok" in aux:
                    a = 1
                    TextRecibidos.insert(1.0, b"Done.\n")
                    messagebox.showinfo(message="Mensaje enviado", title="Resultado")
                time.sleep(1)
        else:
            serialPort1.write(x.encode()+b"\r")
            time.sleep(2+int(comboBox2.get()))
            TextRecibidos.delete(1.0, tk.END)
            aux = serialPort1.read_all()
            if b"Done." in aux:
                TextRecibidos.insert(1.0, b"Done.\n")

    messagebox.showinfo(message="Mensaje enviado", title="Resultado")

        
def click_guardar():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = TextRecibidos.get(1.0, tk.END)
        output_file.write(text)

#Crear y agregar botones a la ventana
botonConectar = tk.Button(ventana, text="Conectar", command=click_conectar)
botonConectar.place(x=40, y=40, width=100, height=22)
botonDesconectar = tk.Button(ventana, text="Desconectar", command=click_desconectar)
botonDesconectar.place(x=320, y=40, width=100, height=22)
botonEnviar = tk.Button(ventana, text="Enviar", command=click_enviar)
botonEnviar.place(x=20, y=100, width=100, height=22)
botonGuardar = tk.Button(ventana, text="Guardar", command=click_guardar)
botonGuardar.place(x=20, y=130, width=100, height=22)
botonPCPLC = tk.Button(ventana, text="Run PCPLC", command=click_pcplc)
botonPCPLC.place(x=20, y=160, width=100, height=22)
botonAbortar = tk.Button(ventana, text="Abortar", command=click_a)
botonAbortar.place(x=20, y=190, width=100, height=22)
botonTTSIB = tk.Button(ventana, text="Run ttsib", command=click_ttsib)
botonTTSIB.place(x=20, y=220, width=100, height=22)
botonCOFF = tk.Button(ventana, text="coff", command=click_click_off)
botonCOFF.place(x=20, y=250, width=100, height=22)
botonMove = tk.Button(ventana, text="Move 0", command=click_move)
botonMove.place(x=20, y=280, width=100, height=22)
botonOpen = tk.Button(ventana, text="Open", command=click_open)
botonClose = tk.Button(ventana, text="Close", command=click_close)
botonClose.place(x=20, y=340, width=100, height=22)
botonOpen.place(x=20, y=310, width=100, height=22)

ventana.mainloop()