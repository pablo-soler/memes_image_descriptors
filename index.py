from PIL import Image
import glob
import math
import numpy as np
import subprocess
import time





# EL ARCHIVO DE INPUT TIENE QUE DEJAR SUS CLS CSD.TXT EN LA CARPETA DEL PROGRAMA
# IMPUT DESCRIPTORS CREATE
args = "MPEG7Fex.exe CSD inputList.txt CSD.txt"
p = subprocess.Popen(args)
args = "MPEG7Fex.exe CLD 6 3 inputList.txt CLD.txt"
p = subprocess.Popen(args)
args = "MPEG7Fex.exe EHD inputList.txt EHD.txt"
p = subprocess.Popen(args)
time.sleep(0.5)



#NAMELIST
nameList =  [ "" for X in range(100)]


#CLD_MATIX
        # Solo 12 números, sin parámetros distintos a la descripción RGB.
def to_cld():
    CLD = open("default_descriptors_memes/CLD.txt").readlines()
    CLD_matrix = [["" for x in range(12)] for y in range(100)] 
    for index, img in enumerate(CLD): 
        cont = 0
        CLD[index] = img[13:]
        nameList[index] = img[:12]
        for carac in CLD[index]:
            if carac != "\n":
                if carac==" ": 
                        CLD_matrix[index][cont] = int(CLD_matrix[index][cont])
                        cont += 1
                else: 
                    CLD_matrix[index][cont] += carac
            else:
                CLD_matrix[index][cont] = int(CLD_matrix[index][cont])
    return CLD_matrix


#CSD_MATRIX
        # El primer numero indica… (??)
        # El resto son los colores principales como en el DCD (7) (??)
def to_csd():
    CSD = open("default_descriptors_memes/CSD.txt").readlines()
    CSD_matrix = [["" for x in range(64)] for y in range(100)] 
    for index, img in enumerate(CSD): 
        cont = 0
        CSD[index] = img[13:]
        for carac in CSD[index]:
            if carac != "\n":
                if carac==" ":
                        CSD_matrix[index][cont] = int(CSD_matrix[index][cont])
                        cont += 1
                else: 
                    CSD_matrix[index][cont]+= carac
            else:
                CSD_matrix[index][cont] = int(CSD_matrix[index][cont])
    return CSD_matrix



#EHD_MATRIX
def to_ehd():
    EHD = open("default_descriptors_memes/EHD.txt").readlines()
    EHD_matrix = [["" for x in range(80)] for y in range(100)] 
    for index, img in enumerate(EHD): 
        cont = 0
        EHD[index] = img[13:]
        for carac in EHD[index]:
            if carac != "\n":
                if carac==" ":
                        EHD_matrix[index][cont] = int(EHD_matrix[index][cont])
                        cont += 1
                else: 
                    EHD_matrix[index][cont]+= carac
            else:
                EHD_matrix[index][cont] = int(EHD_matrix[index][cont])
    return EHD_matrix






#IMPUT TO CLD
def input_to_cld():
    cld = open("CLD.txt").readline()
    cld = cld[13:] #habria que llamar al archivo input siempre 000.meme.jpg si no esto debe ser variable
    cld = cld.split(" ")
    for j in range(0, len(cld)):
        cld[j] = int(cld[j])
    return cld 

#IMPUT TO CSD
def input_to_csd():
    csd = open("CSD.txt").readline()
    csd = csd[13:] #habria que llamar al archivo input siempre 000.meme.jpg si no esto debe ser variable
    csd = csd.split(" ")
    for j in range(0, len(csd)):
        csd[j] = int(csd[j])
    return csd 

#IMPUT TO EHD
def input_to_ehd():
    ehd = open("EHD.txt").readline()
    ehd = ehd[13:] #habria que llamar al archivo input siempre 000.meme.jpg si no esto debe ser variable
    ehd = ehd.split(" ")
    for j in range(0, len(ehd)):
        ehd[j] = int(ehd[j])
    return ehd 


CLD_matrix = to_cld()
CSD_matrix = to_csd()
EHD_matrix = to_ehd()





#DISTANCIA DE CLD 
        #peso de 2 a los 3 primeros y de 1 a los siguientes
def cld_dist():
    cld_input = input_to_cld()
    dist = [0 for x in range(100)]
    for i in range(100):
        #para cada imagen
        for j in  range(12):
            if j<3:
                dist[i] += math.sqrt(math.pow(CLD_matrix[i][j] - cld_input[j], 2)*2)
            else: 
                dist[i] += math.sqrt(math.pow(CLD_matrix[i][j] - cld_input[j], 2))
    return dist


#DISTANCIA DE CSD 
def csd_dist():
    csd_input = input_to_csd()
    dist = [0 for x in range(100)]
    for i in range(100):
        #para cada imagen
        for j in  range(64):
            dist[i] += math.sqrt(math.pow(CSD_matrix[i][j] - csd_input[j], 2))            
    return dist


#DISTANCIA DE EHD 
def ehd_dist():
    ehd_input = input_to_ehd()
    dist = [0 for x in range(100)]
    cont = 0
    for i in range(100):
        suma_img = 0 
        suma_input = 0
        #para cada imagen
        for j in  range(80):
            dist[i] += math.sqrt(math.pow(EHD_matrix[i][j] - ehd_input[j], 2))  
            if cont < 15:
                suma_img += EHD_matrix[i][j]
                suma_input += ehd_input[j]
                cont +=1
            else: 
                dist[i] += 5*math.sqrt(math.pow(suma_img - suma_input, 2))
                cont = 0
    return dist



#DISTANCIA COMBINADA
def csd_cld_dists():
    cld_array = [0 for x in range(100)]
    csd_array = [0 for x in range(100)]
    ehd_array = [0 for x in range(100)]
    dist = [0 for x in range(100)]
    cld_array = cld_dist()
    csd_array = csd_dist()
    ehd_array = ehd_dist()
    cld_max = 0
    csd_max = 0
    ehd_max = 0
    for i in range(100):
        if cld_array[i] > cld_max:
            cld_max = cld_array[i]
        if csd_array[i] > csd_max:
            csd_max = csd_array[i]
        if ehd_array[i] > ehd_max:
            ehd_max = ehd_array[i]
        cld_array[i] *= 0.333 #PESOS PARA CADA DESCRIPTOR
        csd_array[i] *= 0.333
        ehd_array[i] *= 0.333
    for i in range(100):
        dist[i] = (csd_array[i]/csd_max)+(cld_array[i]/cld_max)+(ehd_array[i]/ehd_max)
    return dist



# ORDENAR LAS IMAGENES
cld_name = [x for _,x in sorted(zip(cld_dist(),nameList))]
csd_name = [x for _,x in sorted(zip(csd_dist(),nameList))]
ehd_name = [x for _,x in sorted(zip(ehd_dist(),nameList))]
csd_cld_name = [x for _,x in sorted(zip(csd_cld_dists(),nameList))]

cld_dist_sorted = sorted(cld_dist())
csd_dist_sorted = sorted(csd_dist())
ehd_dist_sorted = sorted(ehd_dist())
csd_cld_dist_sorted = sorted(csd_cld_dists())


#MENSAJE PROBABILIDAD
def media():
    media = (cld_dist_sorted[0] + cld_dist_sorted[1] + cld_dist_sorted[2] + cld_dist_sorted[3] + cld_dist_sorted[4]) / 5  
    if media<40:
        return "Es muy probable que sea un meme"
    if media<60:
        return "podría ser un meme"   
    if media<80:
        return "No es un meme"



f = open('showList.html','w')
message = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="css.css" >
    </head>
    <body>
    
    <div class="navbar"> 
    <h2 class="column" style="width:28%"> IMAGE DESCRIPTORS</h2>
    <h2  class="column" style="width:14.666%">CSD DIST</h2>
    <h2  class="column" style="width:14.666%">CLD DIST</h2>
    <h2  class="column" style="width:14.666%">EHD DIST</h2>
    <h2  class="column" style="width:28%">TOTAL</h2>
    </div>
    
    
    <div class = "sidenav">
    <h3 style="margin-left:30px"> INPUT </h3>
    <img style="width:100%" src="input/000.meme.jpg">
    <h3 style="margin-left:30px">""" +media()+ """</h3>
    </div>


    <div style="margin-top: 40px;">
    <div class="row">
    <div class="column" style="width:28%">
    </div>

    <div class="column" >
        <h2 style="margin-top: 15px;">CSD DIST</h2>"""
    
for j in range(0, len(csd_name)):
    message +="""<div class="polaroid">
      <img class="imgStyle" src="images/"""+csd_name[j]+"""">
      <div class="container">
      <p>"""+csd_name[j]+"""</p>
      <p>CSD: """+str(csd_dist_sorted[j])+""" </p>
      </div></div>"""

message +="""</div><div class="column">
     <h2 style="margin-top: 15px;">CLD DIST</h2>"""
    
for j in range(0, len(cld_name)):
    message +="""<div class="polaroid">
      <img class="imgStyle" src="images/"""+cld_name[j]+"""">
      <div class="container">
      <p>"""+cld_name[j]+"""</p>
      <p>CLD: """+str(cld_dist_sorted[j])+""" </p>
      </div></div>"""

message +="""</div><div class="column" >
     <h2 style="margin-top: 15px;">EHD DIST</h2>"""
    
for j in range(0, len(ehd_name)):
    message +="""<div class="polaroid">
      <img class="imgStyle" src="images/"""+ehd_name[j]+"""">
      <div class="container">
      <p>"""+ehd_name[j]+"""</p>
      <p>EHD: """+str(ehd_dist_sorted[j])+""" </p>
      </div></div>"""
          
message +="""</div><div class="column" style="width:28%">
        <h2 style="margin-top: 15px;">CSD & CLD</h2>"""
    
for j in range(0, len(csd_cld_name)):
    message +="""<div class="polaroid border">
      <img class="imgStyle" src="images/"""+csd_cld_name[j]+"""">
      <div class="container">
      <p>"""+csd_cld_name[j]+"""</p>
      <p>TOTAL: """+str(csd_cld_dist_sorted[j])+""" </p>
      </div></div>"""
message +="""</div>
    </div>

    </div>
    </div>
    </body>"""

f.write(message)
f.close()

