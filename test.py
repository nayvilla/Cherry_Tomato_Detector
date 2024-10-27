import psutil
import subprocess

def find_process_using_com_port(port):
    # Ejecuta el comando para obtener información sobre los puertos seriales abiertos
    try:
        # Usamos powershell para verificar el estado del puerto COM
        output = subprocess.check_output(
            f'powershell -Command "Get-WmiObject Win32_SerialPort | Where-Object {{$_.DeviceID -eq \'{port}\'}}"',
            shell=True
        )
        # Si el puerto está libre, no habrá salida
        if not output:
            print(f"No se encontraron procesos usando {port}.")
            return

        print(f"{port} está en uso. Aquí están los procesos en ejecución:")
        # Itera sobre todos los procesos en ejecución
        for process in psutil.process_iter(['pid', 'name']):
            try:
                # Intenta obtener el nombre y el ID del proceso
                process_info = process.as_dict(attrs=['pid', 'name', 'open_files'])
                open_files = process_info.get('open_files')
                
                # Comprueba si el proceso tiene archivos abiertos
                if open_files:
                    for file in open_files:
                        # Si uno de los archivos abiertos es el puerto COM, muestra la información
                        if port in file.path:
                            print(f"Proceso: {process_info['name']} (PID: {process_info['pid']}) está usando {port}")
                            return
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                # Ignora los procesos a los que no se puede acceder
                continue

        print(f"No se pudo identificar el proceso exacto usando {port}.")
    
    except subprocess.CalledProcessError as e:
        print(f"No se pudo ejecutar el comando PowerShell: {e}")

# Llama a la función con el puerto COM que deseas verificar
find_process_using_com_port("COM3")
