import os,time #para eliminar elementos en carpeta
import zipfile   #para descomprimir el archivo ZIP
from shutil import rmtree
import shutil

from tqdm import tqdm #libreria para barra de descarga
import requests

def descargar_file(link_descarga, name):
    # Streaming, so we can iterate over the response.
    r = requests.get(link_descarga, stream=True)
    
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    t=tqdm(total=total_size, unit='iB', unit_scale=True)
    
    with open(name, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()

    if total_size != 0 and t.n != total_size:
        print("ERROR, algo salio mal")

def descomprimir_zip_files(zip_files):
    print("iniciando descompresion...")
    for folder in zip_files:
        fantasy_zip = zipfile.ZipFile(folder)
        fantasy_zip.extractall(os.getcwd()) 
        fantasy_zip.close()
    
    print("Descomprension exitosa...")







##links de descarga

link_descarga=("http://www2.sunat.gob.pe/padron_reducido_ruc.zip",
               "http://www.sunat.gob.pe/descargaPRR/padron_reducido_local_anexo.zip")


if __name__ == "__main__":
    try:
        print("Inicializando descarga de archivos")
        for link in link_descarga:
            name_file=link.split('/')[-1]
            descargar_file(link,name_file)
        
        
        #descomprimiendo
        files=os.listdir()
        zip_files= [file for file in files if '.zip' in file]
        descomprimir_zip_files(zip_files)

        print("[SUCESS]Proceso acabo exitosamente!!")
    except Exception as e:
        print("[ERROR]Proceso fallo")
        print(e)