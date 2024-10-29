import socket
import tkinter as tk
from threading import Thread
import tkinter.messagebox as messagebox
import time

HOST = '192.168.1.84'
PORT = 8888

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Cliente")

        self.name = tk.StringVar()
        self.name.set('USUARIO1')

        self.received_messages = tk.Text(master, height=10, width=50)
        self.received_messages.pack()

        self.received_messages.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack()

        self.name_entry = tk.Entry(master, width=50, textvariable=self.name)
        self.name_entry.pack()

        self.send_button = tk.Button(master, text="Enviar", command=self.send_message)
        self.send_button.pack()

        self.connected = False
        self.connect_to_server()

    def connect_to_server(self):
        while True:
            try:
                #Creamos un socket para conectarnos al servidor
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                #Nos conectamos al servidor
                self.client_socket.connect((HOST, PORT))

                #Configuramos la variable de conexión
                self.connected = True

                #Enviamos el nombre del cliente al servidor
                self.client_socket.sendall(self.name.get().encode())

                #Inicializamos el hilo para recibir mensajes
                self.receive_thread = Thread(target=self.receive_message)
                self.receive_thread.start()

                print("Conectado al servidor")
                break #Salimos del bucle, si se conectó correctamente

            except Exception as e:
                print("Error de conexión: {e}")

                # Configurar la variable de conexión
                self.connected = False

                #Esperar 5 segundos para intentar conectarse de nuevo
                time.sleep(5)

    def receive_message(self):
        while self.connected:
            try:
                #Recibimos los datos del servidor
                data = self.client_socket.recv(1024)

                #Si no hay datos, cerramos la conexión
                if not data:
                    break

                #Insertamos el mensaje en la interfaz gráfica utilizando 'after'
                self.master.after(0, self.display_message, data.decode())

            except Exception as e:
                print(e)
                self.connected = False
                self.connect_to_server()
                break

    def display_message(self, message):
        self.received_messages.config(state=tk.NORMAL)
        self.received_messages.insert(tk.END, message + '\n')
        self.received_messages.config(state=tk.DISABLED)
        self.received_messages.see(tk.END)


    def send_message(self):
        #Obtener el mensaje del cuadro de texto
        message = self.message_entry.get()

        #Verificar si estamos conectados al servidor
        if not self.connected:
            messagebox.showerror('Error', 'No se pudo enviar el mensaje: no hay conexión')
            return
        
        print("Enviando mensaje: ", message)
        
        #Verificar si el socket está cerrado
        if not self.client_socket._closed:

            try:
                #Enviar el mensaje al servidor
                self.client_socket.sendall(message.encode())
                print("Mensaje enviado")

                #Limpiar el cuadro de texto
                self.message_entry.delete(0, tk.END)

            except Exception as e:
                print("Error al enviar el mensaje: ", e)
                messagebox.showerror('ERROR', f"No se pudo enviar el mensaje: {e}")

        else:
            messagebox.showerror('ERROR', 'No se pudo enviar el mensaje: la conexión con el servidor se ha perdido.')

if __name__ == '__main__':
    root = tk.Tk()
    gui = ClientGUI(root)
    root.mainloop()


