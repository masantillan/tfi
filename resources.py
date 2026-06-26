#Se importa el modulo sqlite3 y colorama e inicializamos
import sqlite3
from colorama import init, Fore, Back
init()

def startdb():
    '''Conexión a la base de datos y creación en caso de no existir'''
    #Se conecta y crea el cursor para la DB
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()

    #Se crea la tabla de no existir
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventario (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        categoria TEXT
                )
    ''')

    #Guardamos los cambios y cerramos la conexion
    conexion.commit()
    conexion.close()

def mainmenu():
    '''Creación del menú principal'''
    #Mostramos el menu principal
    print(Fore.GREEN + "-"*23)
    print(Fore.GREEN + " Sistema de Inventario ")
    print(Fore.GREEN + "-"*23)
    print(Fore.WHITE + "1. Ingreso de Productos")
    print(Fore.WHITE + "2. Productos en Stock")
    print(Fore.WHITE + "3. Actualización de Productos")
    print(Fore.WHITE + "4. Eliminación de Productos")
    print(Fore.WHITE + "5. Búsqueda de Productos")
    print(Fore.WHITE + "6. Stock Bajo")
    print(Fore.WHITE + "7. Salir")

def add(nombre, desc, cantidad, precio, cate):
    '''Agregamos nuevos productos con Nombre, Descripción (opcional), Cantidad, Precio y Categoria (opcional)'''
    #Se conecta y crea el cursor para la DB
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()

    #Ingresamos los datos cargados a la DB y ordenamos en la tabla
    try:
        cursor.execute('''BEGIN TRANSACTION''')

        cursor.execute('''
                    INSERT INTO inventario (nombre, 
                       descripcion, 
                       cantidad, 
                       precio, 
                       categoria)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (nombre, desc, cantidad, precio, cate))
    
        conexion.commit()
        print(f"Producto '{nombre}' cargado exitosamente")
    #En caso de haber algun dato erroneo o invalido, se deshacen los cambios realizados
    except sqlite3.Error as e:
        conexion.rollback()
        print("Error en la carga")
    #Cerramos la conexion al terminar la transaccion
    finally:
        conexion.close()

def stock():
    '''Revisa la base de datos y muestra todos los productos en existencia junto a su stock'''
    #Se conecta y crea el cursor para la DB
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()

    #Seleccionamos todos los datos del inventario
    try:
        cursor.execute('''BEGIN TRANSACTION''')

        cursor.execute('''
                       SELECT * FROM inventario
                       ''')
        invprod = cursor.fetchall()
        if not invprod:
                print(Fore.RED + "No hay productos cargados.")
                return
        #Mostramos el stock
        print("\n---Listado de Productos---")
        for producto in invprod:
            print("="*25)
            print(f"ID: {producto[0]}") 
            print("="*25)
            print(f"| Nombre: {producto[1]}\n| Cantidad: {producto[3]}\n| Descripción: {producto[2]}\n| Precio: {producto[4]}\n| Categoria: {producto[5]}")
        conexion.commit()
    #En caso de error, se deshace cualquier cambio
    except sqlite3.Error as e:
        conexion.rollback()
        print("Error al buscar productos")
    #Se cierra la conexion
    finally:
        conexion.close()

def act(prodid, nameact=None, descact=None, cantact=None, precioact=None, catact=None):
    '''Actualizamos el precio del producto en base a su ID'''
    #Se conecta y crea el cursor para la DB
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()
# Buscar producto actual
    cursor.execute(
        "SELECT nombre, descripcion, cantidad, precio, categoria FROM inventario WHERE id = ?",
            (prodid,)
        )

    producto = cursor.fetchone()

    if producto is None:
        print(f"No existe un producto con ID {prodid}")
        return

    # Mantener valor actual si viene vacío
    nombre = nameact if nameact not in ("", None) else producto[0]
    descripcion = descact if descact not in ("", None) else producto[1]
    cantidad = cantact if cantact not in ("", None) else producto[2]
    precio = precioact if precioact not in ("", None) else producto[3]
    categoria = catact if catact not in ("", None) else producto[4]    

    #Ingresamos los nuevos datos a la tabla
    try:
        cursor.execute('''BEGIN TRANSACTION''')

        cursor.execute('''UPDATE inventario SET nombre = ?, 
                       descripcion = ?, 
                       cantidad = ?, 
                       precio = ?, 
                       categoria = ? 
                       WHERE id = ?''', (nombre, descripcion, cantidad, precio, categoria, prodid))
        conexion.commit()

        print(f"Producto ID: {prodid} actualizado correctamente")

        #Realizamos la verificación para ver si se actualizó
        cursor.execute('''SELECT * FROM inventario WHERE id = ?''', (prodid,))
        prodact = cursor.fetchone()

        print("\n Producto actualizado")
        print("="*25)
        print(f"ID: {producto[0]}") 
        print("="*25)
        print(f"| Nombre: {producto[1]}\n| Cantidad: {producto[3]}\n| Descripción: {producto[2]}\n| Precio: {producto[4]}\n| Categoria: {producto[5]}")
    #En caso de error, se deshace cualquier cambio
    except sqlite3.Error as e:
        conexion.rollback()
        print("Error al buscar productos")
    #Se cierra la conexion
    finally:
        conexion.close()

def wipe(prodid):
    '''Borramos un producto y toda su información, buscando el mismo mediante su ID'''
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()

    try:
        cursor.execute('''BEGIN TRANSACTION''')

        cursor.execute('''
                       DELETE FROM inventario WHERE id = ?
                       ''', (prodid,))
        conexion.commit()
        print(f"Se eliminó el producto: {prodid} de la base de datos")
    except sqlite3.Error as e:
        conexion.rollback()
        print("Error al actualizar")
    finally:
        conexion.close()

def look(prodid):
    '''Busqueda de productos en relación a su ID'''
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()

    try:
        cursor.execute('''BEGIN TRANSACTION''')

        cursor.execute('''
                       SELECT * FROM inventario WHERE id = ?
                       ''', (prodid,))
        prodact = cursor.fetchone()

        if prodact is None:
            print(Fore.RED + f"No existe producto con el ID: {prodid}")
            return
        else:
                    print("\n Producto actualizado")
        print("="*25)
        print(f"ID: {prodact[0]}") 
        print("="*25)
        print(f"|Nombre: {prodact[1]}\n| Cantidad: {prodact[3]}\n| Descripción: {prodact[2]}\n| Precio: {prodact[4]}\n| Categoria: {prodact[5]}")
    except sqlite3.Error as e:
        conexion.rollback()
        print(f"Error en la búsqueda {e}")
    finally:
        conexion.close()

def lowstock():
    '''Mostramos los productos que tengan stock menor a 3 unidades al momento'''
    conexion = sqlite3.connect("inventario.db")

    cursor = conexion.cursor()

    try:
        cursor.execute('''BEGIN TRANSACTION''')

        cursor.execute('''
                       SELECT * FROM inventario WHERE cantidad < ?
                       ''', (3,))
        bajostock = cursor.fetchall()
        if not bajostock:
                print(Fore.RED + "No hay productos con stock bajo.")
                return
        print("\nProductos con Stock Bajo")
        for producto in bajostock:
            print("\n Producto actualizado")
            print("="*25)
            print(f"ID: {producto[0]}") 
            print("="*25)
            print(f"| Nombre: {producto[1]}\n| Cantidad: {producto[3]}\n| Descripción: {producto[2]}\n| Precio: {producto[4]}\n| Categoria: {producto[5]}")
    except sqlite3.Error as e:
        conexion.rollback()
        print("Error al mostrar la opción seleccionada")
    finally:
        conexion.close()
