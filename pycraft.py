
# TODO
#  - Implementar los parámetros en consola
#  - 
import gzip
import re
import os
import argparse

nombreDir = 'logs'
logs = os.listdir(nombreDir)
fileContent = b''
dict = {}
lis = []

# Expresiones regulares

fechaEx = '^(\d{4})-(\d{2})-(\d{2})\s' # Formato 2012-11-31
horaEx = '(\d{2}):(\d{2}):(\d{2})\s'   # Formato 22:11:00
etiquetaEx = '\[([A-Z_]\w*)\]\s'      # Formato [INFO]

def main():
# Función principal. 
# TODO Diferenciar cuando devolvemos un diccionario y cuando una lista
#      Hacer que ip funcione poniendo solo -i, sin tener que poner -i whatever

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="Muestra las ips de los usuarios")
    parser.add_argument("-u", "--user", help="Filtra por usuario")
    parser.add_argument("-c", "--connections", help="Muestra los intentos de conexion de un usuario")
    parser.add_argument("-x", "--xon", help="Muestra los usuarios que se han conectado con cada ip")
    args = parser.parse_args()
    
    if args.xon:
        for l in logs:
            log = abrir(nombreDir + '/' + l)
            if args.user == None:
                ipUsers(log)
            else:
                ipUsers(log, args.user)
        muestra(dict)
    elif args.ip:
        for l in logs:
            log = abrir(nombreDir + '/' + l)
            if args.user == None:
                usersConnections(log)
            else:
                usersConnections(log, args.user)       
        muestra(dict)

    elif args.connections:
        for l in logs:
            log = abrir(nombreDir + '/' + l)
            muestraLista(userConnections(log, args.connections))
    else:
# TODO Muestra la ayuda si se ejecuta sin argumentos/muestra un resumen de los logs cargados
        print("AYUDAME")


def abrir(nombre):
# Carga en memoria del log. 
    f = gzip.open(nombre)
    fileContent = f.read()
    f.close()
    expresion = r'\n'
    log = re.split(expresion, fileContent.decode())
    return log

# Recorrer la variable y almacenar en una lista las lineas. 
def eliminaIp(listaLog, ip):
# Elimina las lines donde aparezcan la ip, asi como las Connection reset.
    expIp = '.*/' + ip
    expCon = '.*Connection.reset'
    res = []
    for e in listaLog:
        if (re.match(expIp, e) == None) and (re.match(expCon, e) == None):
            res.append(e)
    return res

def listaABytes(lista):
# Pasa la lista a bytes (con encode())
    res = ""
    for a in lista:
        res = res + a + "\n"
    bres = res.encode()
    return bres

def save(lista, nombre):
# Guarda la lista de lineas (lista) en el fichero de nombre (TODO añadir .gz)
    listaB = listaABytes(lista)
    with gzip.open(nombre, 'wb') as e:
        e.write(listaB)
    return True

def userIP(lista, user):
# Devuelve una relacion de los intentos de conexion de un usuario: IP, fecha. 
    # Expresion regular para sacar la linea de conexion
    exp = '.*' + user  
    res = []
    for e in lista:
        # Busca la linea de conexion con la expresion regular de antes
        if checkLine(e, exp):
            res.append(e)

    return res 

def usersConnections(log, user=""):
    aux = []
# Devuelve todas las lineas con una conexion 
    exp = r'([a-zA-z0-9]*)\[.(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})' # helmetk[/XXX.XXX.XXX.XXX:XXXXX] logged in 
    for l in log:
        if checkLine(l, exp):
            aux = {checkConnection(l)[8]}
            if checkConnection(l)[7] in dict:
                dict[checkConnection(l)[7]].add(checkConnection(l)[8])
            elif user == "":
                dict[checkConnection(l)[7]] = aux 
            else:
                if checkConnection(l)[7] == user:
                    dict[checkConnection(l)[7]] = aux
    return True

def userConnections(log, user):
    exp = r'([a-zA-z0-9]*)\[.(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})'
    auxi = []
    for l in log:
        if checkLine(l, exp) and checkConnection(l)[7] == user:
            a = checkConnection(l)
            auxi.append(a[8]+" - "+a[2]+"-"+a[1]+"-"+a[0]+" "+a[3]+":"+a[4]+":"+a[5])
    return auxi
         

def checkConnection(line):
# Devuelve los diferentes parametros de una linea de conexion. Lanza excepcion si no es una linea de conexion.
    exp = r'([a-zA-z0-9]*)\[.(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})'
    if checkLine(line, exp):
        return re.match(fechaEx + horaEx + etiquetaEx + exp, line).groups()
    else:
        return False

def checkLine(linea, exp):
# Detecta si una linea empieza bien (fecha, hora, tipo) y si contiene la expresion exp
    ex = fechaEx + horaEx + etiquetaEx + exp
    return re.match(ex, linea) != None

def ipUsers(log, ip=""):
    exp = r'([a-zA-z0-9]*)\[.(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})'
    for l in log:
        if checkLine(l, exp):
            a = checkConnection(l)
            aux = {a[7]}
            if a[8] in dict:
                dict[a[8]].add(a[7])
            elif ip == "":
                dict[a[8]] = aux 
            else:
                if a[8] == ip:
                    dict[a[8]] = aux
    return True

       

# ZONA DE PRUEBAS 
def muestra(lista):
    for k, r in lista.items():
        print(k+": "+str(r))

def muestraLista(lista):
    for l in lista:
        print(l)
main()
# pec = eliminaIp(log, '74.86.158.10*') 
# save(pec, 'prueba.gz')
