import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import bs4
import requests
import time

os.environ['PATH'] += r"C:\SeleniumDrivers"

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver del navegador adecuado instalado

# Navegar a la página web
driver.get("http://www.pregrado.unal.edu.co/programas-acred/")

# Encontrar todas las posibles opciones
sedes = driver.find_element(By.ID, "sel1")

dict_programas = dict()
nombres_programas = set()

select_sedes = Select(sedes)
select_sedes.select_by_visible_text('Bogotá')

print(f'Sede: Bogotá -----------------------\n')
# Encontrando las opciones
facultades = driver.find_element(By.ID, "facultad")
time.sleep(1)
#facultades_opt = facultades.text.splitlines()[1:] # obviamos la opcion facultades
facultades_opt = ['Medicina Veterinaria y de Zootecnia']
print(facultades_opt)

for facultad in facultades_opt:
    if facultad != "" and not facultad.isspace():
        # Arreglar el formato de facultad
        fac = facultad.lstrip()
        fac = fac.rstrip()

        # Seleccionando la facultad en el dropdown
        select_facultades = Select(facultades)
        select_facultades.select_by_visible_text(fac)
        #driver.implicitly_wait(1000)
        print(f'Facultad: {fac} -----------------------\n')

        # Encontrando las opciones
        programas = driver.find_element(By.ID, "programas")
        time.sleep(1)
        programas_opt = programas.text.splitlines()[2:] # obviamos la opcion programas
        for programa in programas_opt:
            
            # Arreglar el formato del programa
            prog = programa.rstrip()
            prog = prog.lstrip()
            
            print(prog)
            
            # Seleccionar el programa
            select_programas = Select(programas)
            select_programas.select_by_visible_text(prog)
            time.sleep(2)
            print('\n')

            # Extraer INFO
            info_prog = driver.find_element(By.ID, "info-prog")
            link_legal = info_prog.find_elements(By.TAG_NAME, 'a')[-1].get_attribute('href')

            #print(info_prog.text)
            print(link_legal)

            # Entrando a legal --------------------------------------------------------------------
            driver.get(link_legal)
            # Caja con todo el texto plano --------------------------------------------------------
            info_legal = driver.find_element(By.ID,'info_texto')
            legal_text = info_legal.text
            # -------------------------------------------------------------------------------------
            # Formatear las tablaZZZ --------------------------------------------------------------
            tablas = driver.find_elements(By.TAG_NAME,'table') # coger las tablas
            tablas = tablas[:len(tablas)-1]
            tabla_format = ''

            for tabla in tablas:
                filas = tabla.find_elements(By.TAG_NAME,'tr') # todas las filas
                celdas = tabla.find_elements(By.TAG_NAME,'td') # todas las celdas
                titulos = filas[0].text.split('\n') # titulos de las tablas
                try:
                    titulos += filas[1].text.split('\n') # los subtitulos
                    if len(titulos) == 8:
                        titulos[4:6] = 'ASIGNATURA PRERREQUISITO/ CORREQUISITO'
                except:
                    break

                i = len(titulos) # titulos
                j = len(titulos) # celdas
                while i < len(celdas):
                    if titulos[(i)%len(titulos)] == 'ASIGNATURA PRERREQUISITO/ CORREQUISITO':
                        try:
                            tabla_format += 'ASIGNATURA PRERREQUISITO/ CORREQUISITO'
                            tabla_format += f'{titulos[(i+1)%len(titulos)]}  {celdas[j].text}\n' 
                            print(f'{titulos[(i+1)%len(titulos)]}  {celdas[j+1].text}')
                            tabla_format += f'{titulos[(i+2)%len(titulos)]}  {celdas[j+1].text}\n' 
                            print(f'{titulos[(i+2)%len(titulos)]}  {celdas[j+1].text}')
                            i+=3
                            j+=2
                        except:
                            break
                    else:
                        try:
                            tabla_format += f'{titulos[(i)%len(titulos)]}  {celdas[j].text}\n' 
                            print(f'{titulos[(i)%len(titulos)]}  {celdas[j].text}')
                            i+=1
                            j+=1
                        except: 
                            break


                tabla_format += '\n'

            tabla_format += '\n'

            # ------------------------------------------------------------------------------------
            # print(legal_text)
            driver.back()
            print('\n')

            # Abrir el archivo y escribir
            with open('programas.txt','a',encoding='utf-8') as file_object:
                file_object.write(f'{prog}\n')
                file_object.write(f'{link_legal}\n')
                file_object.write(f'{legal_text}\n')
                file_object.write(f'{tabla_format}\n')

            #driver.implicitly_wait(1000)
            # Guardamos todos los programas
            if prog not in nombres_programas:
                nombres_programas.add(prog)
                # Guardamos en un diccionario con nombre como llave y la info como valor
                dict_programas[prog] = info_prog
        print('\n')




# for link in soup.find_all("a", href=True):
#     href = link['href']
#     href = href.replace("../", "")
#     print("http://www.legal.unal.edu.co/rlunal/home/" + href)

#facultades = driver.find_element(By.ID, "facultad")
#facultades_opt = facultades.text.split()[1:]
#print(facultades_opt)

#programas = driver.find_element(By.ID, "programas")
#programas_opt = programas.text.split()[1:]
#print(programas_opt)


# Find Element by tag name
# SEDES
#sedes_box = driver.find_element(By.ID, "sel1")
#select_sedes = Select(sedes_box)
#select_sedes.select_by_visible_text('Bogotá')

#facultades_box = driver.find_element(By.ID, "facultad")
#select_facultades = Select(facultades_box)
#select_facultades.select_by_visible_text('Medicina')

#programas_box = driver.find_element(By.ID, "programas")
#select_programas = Select(programas_box)
#select_programas.select_by_visible_text('Medicina-Bogotá')



# Cerrar el navegador
driver.quit()


