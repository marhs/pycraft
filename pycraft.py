
# TODO
#  - Implementar los parámetros en consola
#  - 
import gzip
import re

nombreLog = 'server_2012-10-06.log.gz'
log = ""
fileContent = b''

# Expresiones regulares

fechaEx = '^(\d{4})-(\d{2})-(\d{2})\s' # Formato 2012-11-31
horaEx = '(\d{2}):(\d{2}):(\d{2})\s'   # Formato 22:11:00
etiquetaEx = '\[([A-Z_]\w*)\]\s'      # Formato [INFO]

def abrir(nombreLog):
# Carga en memoria del log. 
    f = gzip.open(nombreLog)
    fileContent = f.read()
    f.close()
    return fileContent

fileContent = abrir(nombreLog)

# Recorrer la variable y almacenar en una lista las lineas. 
expresion = r'\n'
log = re.split(expresion, fileContent.decode())
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

def usersConnections(log):
    dict = {}
    aux = []
# Devuelve todas las lineas con una conexion 
    exp = '([a-zA-Z0-9]*)\[' # helmetk[/XXX.XXX.XXX.XXX:XXXXX] logged in 
    for l in log:
        if checkLine(l, exp):
            if checkConnection(l)[7] in dict:
                dict[checkConnection(l)[7]].add(checkConnection(l)[8])
            else:
                aux = {checkConnection(l)[8]}
                dict[checkConnection(l)[7]] = aux
    return dict
        
def checkConnection(line):
    exp = r'([a-zA-z0-9]*)\[.(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})'
    return re.match(fechaEx + horaEx + etiquetaEx + exp, line).groups()

def checkLine(linea, exp):
# Detecta si una linea empieza bien (fecha, hora, tipo) y si contiene la expresion exp
    ex = fechaEx + horaEx + etiquetaEx + exp
    return re.match(ex, linea) != None

# ZONA DE PRUEBAS 
def muestra(lista):
    for k, r in lista.items():
        print(k+"\n    "+str(r))

muestra(usersConnections(log))
# pec = eliminaIp(log, '74.86.158.10*') 
# save(pec, 'prueba.gz')
