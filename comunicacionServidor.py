import socket
import threading
import tkinter as tk
import tkinter.messagebox as messagebox

HOST = '' #Significa que escucha en todas las interfaces de red
PORT = 8888 #Puerto de escucha
MAX_CONNECTIONS = 2 #Numero maximo de conexiones simultaneas
Server_Socket = None
connections = [] #Lista para almacenar conexiones
is_running = False
# stop_event = threading.Event()
lock = threading.Lock()
dummy_socket = None

def iniciar_Servidor():
    global Server_Socket, dummy_socket, is_running
    if not is_running:
        #Crear un objeto de socket TCP
        Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Vincular el socket a una direccion y puertos específicos
        Server_Socket.bind((HOST, PORT))
        Server_Socket.listen(MAX_CONNECTIONS)
    
        Server_Socket.settimeout(1)

        # dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # dummy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # dummy_socket.bind((HOST, 0))
    
        is_running = True
        threading.Thread(target=aceptar_conexiones, daemon=True).start()
        log(f'Servidor corriendo en el puerto {PORT}')


    Start_Button.config(state=tk.DISABLED)
    Stop_Button.config(state=tk.NORMAL)
    mensaje_Text.config(state=tk.NORMAL)
    Enviar_Button.config(state=tk.NORMAL)

    EstadoLabel.config(text="Servidor iniciado")

def detener_servidor():
    global Server_Socket, connections, is_running
    if is_running:
        is_running = False

        #Cerrar todas las conexiones
        with lock:
            for conn in connections:
                try:
                    conn.close()
                except OSError:
                    pass


        try:
            Server_Socket.close()
        except OSError:
            pass

    messagebox.showinfo("Servidor", "Servidor detenido")

    Start_Button.config(state=tk.NORMAL)
    Stop_Button.config(state=tk.DISABLED)
    mensaje_Text.config(state=tk.DISABLED)
    Enviar_Button.config(state=tk.DISABLED)
    EstadoLabel.config(text="Servidor detenido")

def Manejar_Conexion(conn, addr, name):
    log(f'{name} conectado por {addr}')

    while is_running:
        try:
            #Recibimos los datos del cliente
            data = conn.recv(1024)
            if not data:
                continue
            mensaje = data.decode().strip()
            log(f'Datos recibidos de {name}: {mensaje}')
    
            #Procesamos el mensaje del cliente
            respuesta = f'Recibido: "{mensaje}" en el servidor'.encode()
            conn.sendall(respuesta)
        except OSError:
            break

    #cerrar la conexión
    conn.close()
    log(f'conexión cerrada con {name}')
    with lock:
        connections.remove(conn)

def aceptar_conexiones():
    global connections
    while is_running:
        try:
            conn,addr = Server_Socket.accept()
            with lock:
                if not is_running:
                    conn.close()
                    break
                connections.append(conn)
            
            #Recibimos el nombre del cliente
            data = conn.recv(1024)
            name = data.decode().strip()

            if not name:
                name = f"Cliente {addr}"

            log(f'{name} conectado desde {addr}')

            #Creamos un hilo para manejar la conexión
            t = threading.Thread(target=Manejar_Conexion, args=(conn, addr, name), daemon=True)
            t.start()
        except socket.timeout:
            continue
        except OSError as e:
            if not is_running:
                break

    #Escuchar informacion de los clientes


    # #Ciclo para manejar las conexiones
    # while True:
    #     conn, addr = Server_Socket.accept()
    #     connections.append(conn)

    #     #Recibimos el nombre del cliente
    #     data = conn.recv(1024)
    #     name = data.decode().strip()
    #     names.append(name)

    #     #Creamos un hilo para manejar las conexiones
    #     t = threading.Thread(target=Manejar_Conexion, args=(conn, addr, name))
    #     t.start()

def enviar_mensaje():
    mensaje = mensaje_Text.get(1.0, tk.END).strip()
    mensaje_Text.delete(1.0, tk.END)
    log(f'Mensaje enviado a todos los clientes: {mensaje}')
    with lock:
        for conn in connections:
            try:
                conn.sendall(mensaje.encode())
            except OSError:    
                pass

def log(mensaje):
    Log_text.insert(tk.END, mensaje + "\n")
    Log_text.see(tk.END)

#Crear ventana
ventana = tk.Tk()
ventana.title("Servidor")

#Label
EstadoLabel = tk.Label(ventana, text="Servidor detenido")
EstadoLabel.pack()

#Text
Log_text = tk.Text(ventana, height=10, width=50)
Log_text.pack()

#Botones
Start_Button = tk.Button(ventana, text="Iniciar servidor", command=iniciar_Servidor)
Start_Button.pack()

Stop_Button = tk.Button(ventana, text="Detener servidor", command=detener_servidor, state=tk.DISABLED)
Stop_Button.pack()

#Text
mensaje_Text = tk.Text(ventana, height=3, width=50)
mensaje_Text.pack()

#Boton
Enviar_Button = tk.Button(ventana, text="Enviar", command=enviar_mensaje, state=tk.DISABLED)
Enviar_Button.pack()

ventana.mainloop()
