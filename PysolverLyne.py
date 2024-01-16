import tkinter as tk
from pulp import *
import tkinter.messagebox as messagebox

def guardar_num_variables():
    num_variables_text = num_variables_entry.get()
    if num_variables_text.strip() != "":
        num_variables_value = int(num_variables_text)
        num_variables = num_variables_value
        num_variables_mostrado_label.config(text=str(num_variables))
        num_variables_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Por favor ingresa un valor válido para el número de variables.")

def guardar_num_restricciones():
    num_restricciones_text = num_restricciones_entry.get()
    if num_restricciones_text.strip() != "":
        num_restricciones_value = int(num_restricciones_text)
        num_restricciones = num_restricciones_value
        num_restricciones_mostrado_label.config(text=str(num_restricciones))
        num_restricciones_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Por favor ingresa un valor válido para el número de restricciones.")

def verificar_campos_variables(coeficientes_vars, ventana_variables):
    for coeficiente in coeficientes_vars:
        if coeficiente.get().strip() == "":
            messagebox.showerror("Error", "Por favor ingresa un valor válido para todos los coeficientes de variables.")
            return
        else:
            ventana_variables.destroy()
            mostrar_variables()

def verificar_campos_restricciones(coeficientes_restricciones, coef_limites, ventana_restricciones):
    for i in range(len(coeficientes_restricciones)):
        for j in range(len(coeficientes_restricciones[i])):
            if coeficientes_restricciones[i][j].get().strip() == "":
                messagebox.showerror("Error", "Por favor ingresa un valor válido para todos los coeficientes de restricciones.")
                return
        if coef_limites[i].get().strip() == "":
            messagebox.showerror("Error", "Por favor ingresa un valor válido para todos los límites de restricciones.")
            return
    
    ventana_restricciones.destroy()
    mostrar_restricciones()

def abrir_ventana_variables():
    if num_variables_mostrado_label.cget("text") == "":
        messagebox.showerror("Error", "Por favor ingresa un valor válido para el número de variables antes de agregar variables.")
        return

    ventana_variables = tk.Toplevel(root)
    ventana_variables.title("Ingresar Coeficientes de Variables")
    ventana_variables.resizable(False, False)

    rango = obtener_num_variables()

    coeficientes_vars.clear()
    for i in range(rango):
        coeficientes_vars.append(tk.StringVar())
        tk.Label(ventana_variables, text="Coeficiente X" + str(i+1)).pack()
        tk.Entry(ventana_variables, textvariable=coeficientes_vars[i]).pack()

    tk.Button(ventana_variables, text="Continuar", command=lambda: verificar_campos_variables(coeficientes_vars,ventana_variables)).pack()

def abrir_ventana_restricciones():
    if num_variables_mostrado_label.cget("text") == "":
        messagebox.showerror("Error", "Por favor agrega variables antes de agregar restricciones.")
        return

    if num_restricciones_mostrado_label.cget("text") == "":
        messagebox.showerror("Error", "Por favor ingresa un valor válido para el número de restricciones antes de agregar restricciones.")
        return
    
    ventana_restricciones = tk.Toplevel(root)
    ventana_restricciones.title("Ingresar Coeficientes de Restricciones")
    ventana_restricciones.resizable(False, False)

    num_restricciones = obtener_num_restricciones()

    coeficientes_restricciones.clear()
    coef_limites.clear()
    condiciones.clear()

    for i in range(num_restricciones):
        coeficientes_restricciones.append([])
        tk.Label(ventana_restricciones, text="Restricción #" + str(i+1), font=("Arial", 14, "bold")).grid(row=i*2, column=0, columnspan=2)
        for j in range(len(coeficientes_vars)):
            coeficientes_restricciones[i].append(tk.StringVar())
            tk.Label(ventana_restricciones, text="Coeficiente X" + str(j+1)).grid(row=i*2+1, column=j*2)
            tk.Entry(ventana_restricciones, textvariable=coeficientes_restricciones[i][j]).grid(row=i*2+1, column=j*2+1)
    
        condiciones.append(tk.StringVar())
        condiciones[i].set("<=")
        tk.OptionMenu(ventana_restricciones, condiciones[i], "<=", ">=", "=").grid(row=i*2+1, column=len(coeficientes_vars)*2)

        coef_limites.append(tk.StringVar())
        tk.Label(ventana_restricciones, text="Límite").grid(row=i*2+1, column=len(coeficientes_vars)*2+1)
        tk.Entry(ventana_restricciones, textvariable=coef_limites[i]).grid(row=i*2+1, column=len(coeficientes_vars)*2+2)

    tk.Button(ventana_restricciones, text="Continuar", command=lambda: verificar_campos_restricciones(coeficientes_restricciones, coef_limites, ventana_restricciones)).grid(row=num_restricciones*2+2, column=0, columnspan=len(coeficientes_vars)*2+3)

def mostrar_variables():
    funcion_objetivo = "Función objetivo:\n"
    for i in range(len(coeficientes_vars)):
        funcion_objetivo += "(" + coeficientes_vars[i].get() + "*x" + str(i+1) + ")"
        if i < len(coeficientes_vars) - 1:
            funcion_objetivo += " + "
    
    variables_label.config(text=funcion_objetivo)

def mostrar_restricciones():
    restricciones_text = "Restricciones:\n"
    for i in range(len(coeficientes_restricciones)):
        restriccion = ""
        for j in range(len(coeficientes_vars)):
            coef = coeficientes_restricciones[i][j].get()
            var = "x" + str(j + 1)
            restriccion += "(" + coef + "*" + var + ")"
            if j < len(coeficientes_vars) - 1:
                restriccion += "+"
        condicion = condiciones[i].get()
        limite = coef_limites[i].get()
        restricciones_text += restriccion + condicion + limite + "\n"
    restricciones_label.config(text=restricciones_text)

def obtener_num_variables():
    texto = num_variables_mostrado_label.cget("text")
    num_variablesInterno = int(texto) 
    return num_variablesInterno

def obtener_num_restricciones():
    texto = num_restricciones_mostrado_label.cget("text")
    num_variablesInterno = int(texto) 
    return num_variablesInterno

def resolver_lp():
    # Crear el problema de maximización o minimización
    if maximizar.get():
        prob = LpProblem("MinimizarZ", LpMinimize)
    else:
        prob = LpProblem("MaximizarZ", LpMaximize)

    # Definir las variables de decisión
    variables = []
    for i in range(len(coeficientes_vars)):
        var = LpVariable("X" + str(i+1), lowBound=0, cat='Integer')
        variables.append(var)

    # Definir la función objetivo
    prob += lpSum(variables[i] * int(coeficientes_vars[i].get()) for i in range(len(coeficientes_vars))), "Z"

    # Definir las restricciones
    for i in range(len(coeficientes_restricciones)):
        restriccion = lpSum(variables[j] * int(coeficientes_restricciones[i][j].get()) for j in range(len(coeficientes_vars)))
        coef = int(coef_limites[i].get())
        condicion = condiciones[i].get()
        if condicion == "<=":
            prob += restriccion <= coef
        elif condicion == ">=":
            prob += restriccion >= coef
        else:
            prob += restriccion == coef

    # Resolver el problema
    prob.solve()

    # Obtener los valores óptimos de las variables
    valores_variables = [int(value(var)) for var in variables]  # Convertir a enteros

    # Obtener el valor óptimo de la función objetivo
    valor_objetivo = int(value(prob.objective))  # Convertir a entero

    # Mostrar los resultados en una ventana aparte
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("PySolverLine")
    ventana_resultados.resizable(False, False)

    label_resultados = tk.Label(ventana_resultados, text="Resultados", font=label_font)
    label_resultados.pack()

    # Etiquetas de valores óptimos de las variables
    for i, var in enumerate(variables):
        etiqueta_variable = tk.Label(ventana_resultados, text=f"Valor de {var.name}: {valores_variables[i]}", font=Rest_font)
        etiqueta_variable.pack()

    # Etiqueta de valor óptimo de la función objetivo
    resultado_objetivo = tk.Label(ventana_resultados, text="Valor óptimo de Z: " + str(valor_objetivo), font=Rest_font)
    resultado_objetivo.pack()

# Ventana principal
root = tk.Tk()
root.title("PySolverLine")
root.resizable(False, False)

# Variables de entrada
num_variables = tk.StringVar()
num_restricciones = tk.StringVar()
coeficientes_vars = []
coeficientes_restricciones = []
condiciones = []
coef_limites = []
maximizar = tk.BooleanVar()

# Configuración de la fuente para los elementos de la interfaz
title_font = ("Arial", 30, "bold")
label_font = ("Arial", 14, "bold")
Rest_font  = ("Arial", 12)
credits_font = ("Arial", 12)

# Título
titulo_label = tk.Label(root, text="PySolverLine", font=title_font, pady=10)
titulo_label.grid(row=0, column=0, columnspan=5, pady=10)

# Créditos
credits_label = tk.Label(root, text="By JsDev02", font=credits_font)
credits_label.grid(row=1, column=0, columnspan=5, pady=10)

# Selección de maximizar o minimizar
maximizar_label = tk.Label(root, text="¿Desea Maximizar o Minimizar?", font=label_font)
maximizar_label.grid(row=2, column=0, columnspan=5, pady=10)

maximizar_option = tk.Radiobutton(root, text="Maximizar", variable=maximizar, value=False, font=Rest_font)
maximizar_option.grid(row=3, column=0, padx=10, columnspan=2,sticky=tk.E)

minimizar_option = tk.Radiobutton(root, text="Minimizar", variable=maximizar, value=True, font=Rest_font)
minimizar_option.grid(row=3, column=1, padx=10, columnspan=2)

# Número de variables y botón para agregar variables
num_variables_label = tk.Label(root, text="Número de variables:", font=label_font)
num_variables_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

num_variables_entry = tk.Entry(root, textvariable=num_variables, font=label_font)
num_variables_entry.grid(row=5, column=0, padx=(0, 5), pady=5, sticky=tk.E)

guardar_variables_button = tk.Button(root, text="Guardar", command=guardar_num_variables,font=("Arial", 12, "bold"), bg="lightblue")
guardar_variables_button.grid(row=5, column=1, padx=(0, 10), pady=5, sticky=tk.W)

num_variables_guardado_label = tk.Label(root, text="Número de variables guardado:", font=label_font)
num_variables_guardado_label.grid(row=4, column=2, sticky=tk.W, padx=10, pady=5)

num_variables_mostrado_label = tk.Label(root, text="",font=label_font)
num_variables_mostrado_label.grid(row=5, column=2, rowspan=1, padx=10, pady=5)

agregar_variables_button = tk.Button(root, text="Agregar variables", command=abrir_ventana_variables,font=("Arial", 12, "bold"), bg="lightblue")
agregar_variables_button.grid(row=6, column=0, columnspan=2, pady=0)

# Etiqueta de variables
variables_label = tk.Label(root, text="Función objetivo:", font=label_font)
variables_label.grid(row=6, column=2, sticky=tk.W, padx=10, pady=5)

# Número de restricciones y botón para agregar restricciones
num_restricciones_label = tk.Label(root, text="Número de restricciones:", font=label_font)
num_restricciones_label.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

num_restricciones_entry = tk.Entry(root, textvariable=num_restricciones, font=label_font)
num_restricciones_entry.grid(row=8, column=0, padx=(0, 5), pady=5, sticky=tk.E)

guardar_restricciones_button = tk.Button(root, text="Guardar", command=guardar_num_restricciones,font=("Arial", 12, "bold"), bg="lightblue")
guardar_restricciones_button.grid(row=8, column=1, padx=(0, 10), pady=5, sticky=tk.W)

agregar_restricciones_button = tk.Button(root, text="Agregar restricciones", command=abrir_ventana_restricciones,font=("Arial", 12, "bold"), bg="lightblue")
agregar_restricciones_button.grid(row=9, column=0, columnspan=2, pady=0)

restricciones_label = tk.Label(root, text="Restricciones:", font=label_font)
restricciones_label.grid(row=9, column=2, sticky=tk.W, padx=10, pady=5)

num_restricciones_guardado_label = tk.Label(root, text="Número de restricciones guardado:", font=label_font)
num_restricciones_guardado_label.grid(row=7, column=2, sticky=tk.W, padx=10, pady=5)

num_restricciones_mostrado_label = tk.Label(root, text="", font=label_font)
num_restricciones_mostrado_label.grid(row=8, column=2, rowspan=1, padx=10, pady=5)

def limpiar():
    num_variables.set("")
    num_restricciones.set("")
    num_variables_mostrado_label.config(text="")
    num_restricciones_mostrado_label.config(text="")
    coeficientes_vars.clear()
    coeficientes_restricciones.clear()
    condiciones.clear()
    coef_limites.clear()
    maximizar.set(False)
    variables_label.config(text="Variables:")
    restricciones_label.config(text="Restricciones:")

# Resolver y Limpiar
resolver_button = tk.Button(root, text="Resolver", command=resolver_lp, font=("Arial", 20, "bold"), bg="green", fg="white")
resolver_button.grid(row=10, column=0, columnspan=2, pady=20, sticky=tk.E)

limpiar_button = tk.Button(root, text="Limpiar", command=limpiar, font=("Arial", 20, "bold"), bg="red", fg="white")
limpiar_button.grid(row=10, column=1, columnspan=10, pady=2)

# Ejecutar ventana principal
root.mainloop()
