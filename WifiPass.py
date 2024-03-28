import os
import glob
import threading
import subprocess

'''
Los creditos recervados por @GatoArtStudio, no se hace responsable de uso inadecuado del codigo, se creo con fines educativos
'''

class Wifi():
    '''
    Esta clase tiene toda la configuracion para obtener las constraseñas de las redes wifi de un usuario de windows
    '''
    def __init__(self) -> None:
        self.path = ''
        self.bucle_thread = None
        self.temp = ''
    
    def bucle (self):
        '''
        Esta funcion lo que hace es que recorre el directorio de trabajo buscando archivos .xml y guarda todo en MyPassword.tx en el mismo directorio de trabajo
        '''
        os.chdir(self.path)
        pass_text = ["<name>", "<keyMaterial>"]
        with open("MyPassword.txt", "a") as filtered_file:
            for file_path in glob.glob("*.xml"):
                with open(file_path) as file:
                    filtered_lines = [line for line in file if any(keyword in line for keyword in pass_text)]
                    for line in filtered_lines:
                        line = line.replace('/','').strip() # .strip() elimina todos los espacios
                        if '<name>' in line:
                            line = line.replace('<name>','')
                            if line != self.temp:
                                self.temp = line
                                line = f'Nombre Wifi: {line}\n'
                            else:
                                continue
                        line = line.replace('<', ' ').replace('>', ' ')
                        if 'keyMaterial' in line:
                            line = line.replace('keyMaterial','').strip()
                            if line != self.temp:
                                self.temp = line
                                line = f'Contraseña: {line}\n'
                            else:
                                continue
                        filtered_file.write(line)
                        
    def movePath(self) -> None:
        '''
        Esta funcion mueve de directorio de trabajo al directorio establecido en el contructor self.path
        ```
        def move_path(self) -> None:
            os.chdir(self.path)
        ```
        '''
        os.chdir(self.path)
                        
    def run(self, path: str) -> None:
        '''
        Esta funcion arranca el programa en si debes pasarle un direcotiro de trabajo para que funcione correctamente
        ejemplo:
        ```
        if __name__ == '__main__':
            app = Wifi()
            app.run(path=r'C:\Temp') # En este directorio que se le pasa se creara los archivos con los datos de las keys
        ```
        '''
        self.path = path
        self.movePath()
        promt = subprocess.run(f"netsh wlan export profile folder={self.path} key=clear", check=True)
        self.bucle_thread = threading.Thread(target=self.bucle)
        self.bucle_thread.start()
        self.bucle_thread.join() # Espera a que termine el hilo para continuar con el codigo
        ext = ".xml"
        for filename in os.listdir():
            if filename.endswith(ext):
                os.remove(filename)
                
if __name__ == '__main__':
    app = Wifi()
    app.run(path=r'C:\Temp') # recuerda coloca en 'C:\Temp' la ruta donde quieres que trabaje el script. hay se guarda el archivo MyPassword.txt con las claves y nombre de las redes
