import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

os.environ['PATH'] += r"C:\SeleniumDrivers"

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver del navegador adecuado instalado

# Navegar a la página web
driver.get("http://www.pregrado.unal.edu.co/programas-acred/")

# Encontrar todas las posibles opciones
sedes = driver.find_element(By.ID, "sel1")
sedes_opt=sedes.text.split()[:] # obviamos la opcion sedes
print(sedes_opt)

dict_programas = dict()
nombres_programas = set()

for sede in sedes_opt:
    # Seleccionando la sede en el dropdown
    select_sedes = Select(sedes)
    select_sedes.select_by_visible_text(sede)
    driver.implicitly_wait(10)
    
    print(f'Sede: {sede} -----------------------\n')
    # Encontrando las opciones
    facultades = driver.find_element(By.ID, "facultad")
    facultades_opt = facultades.text.splitlines()[2:] # obviamos la opcion facultades
    print(facultades_opt)

    for facultad in facultades_opt:
        if facultad != "" and not facultad.isspace():
            # Seleccionando la sede en el dropdown
            fac = facultad.lstrip()
            fac = fac.rstrip()

            select_facultades = Select(facultades)
            select_facultades.select_by_visible_text(fac)
            driver.implicitly_wait(10)
            print(f'Facultad: {fac} -----------------------\n')

            # Encontrando las opciones
            programas = driver.find_element(By.ID, "programas")
            programas_opt = programas.text.splitlines()[2:] # obviamos la opcion programas
            for programa in programas_opt:
                prog = programa.rstrip()
                prog = prog.lstrip()

                print(prog)
                select_programas = Select(programas)
                select_programas.select_by_visible_text(prog)
                print('\n')
                # Extraer INFO
                info_prog = driver.find_element(By.ID, "info-prog")
                print(info_prog.text)
                print('\n')

                # Guardamos todos los programas
                if prog not in nombres_programas:
                    nombres_programas.add(prog)
                    # Guardamos en un diccionario con nombre como llave y la info como valor
                    dict_programas[prog] = info_prog
            print('\n')

    


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




