#Importamos las funciones requeridas para que el programa tenga todas sus funciones
import resources as r

#Importamos colorama
from colorama import init, Fore, Back
init()

#Inicializamos la DB y creamos la tabla
r.startdb()

while True: 
    #Mostramos el menu y elegimos la opción
    r.mainmenu()

    seleccion = input("Elije una opción: ").strip()

    if seleccion.isdigit(): #Verificación para la opción
        seleccion = int(seleccion)
        match seleccion:
            case 1: #Se ingresan los datos para la carga del producto
                nombre = input("Ingrese el nombre del producto: ")
                if nombre != "":
                    descripcion = input("Ingrese la descripción: ")
                    cantidad = input("Ingrese la cantidad actual: ")
                    precio = input("Ingrese el precio: ")
                    categoria = input("Ingrese la categoria: ")
                    r.add(nombre, descripcion, cantidad, precio, categoria)
                else:
                    print(Fore.RED + "\n'Nombre' no puede estar vacío")
                    continue
            case 2: #Mostramos todos los productos disponibles
                r.stock()
            case 3: #Actualizamos el producto en base a su ID
                prodid = int(input("Ingrese el ID del producto a actualizar: "))
                print(Fore.RED + "Para mantener un valor, dejar vacío el campo" + Fore.WHITE)
                nameact = input("Ingrese el nuevo nombre: ").strip() or None
                descact = input("Ingrese nueva descripción: ").strip() or None
                while True:
                    cantact = input("Ingrese nueva cantidad: ").strip() or None
                    precioact = input("Ingrese el nuevo precio: ").strip() or None
                catact = input("Ingrese nueva categoría: ").strip() or None
                r.act(prodid, nameact, descact, cantact, precioact,catact)
            case 4: #Se elimina el producto en base a su ID
                prodid = int(input("Ingrese el ID del producto a eliminar: "))
                r.wipe(prodid)
            case 5: #Buscamos un producto en base a su ID
                prodid = int(input("Ingrese el ID del producto a buscar: "))
                r.look(prodid)
            case 6: #Traemos los productos, en este caso con stock menor a 3
                r.lowstock()
            case 7: #Salimos del programa
                input("\nEl programa se cerrará...\n")
                break
            case _: #Mensaje de error en caso de que el numero no corresponda
                print(Fore.RED + "\nOpción invalida")
    else: #Mensaje de error en caso de que no sea un numero
        print(Fore.RED + "\nOpción invalida, seleccione un número")