import re
import os
import tkinter as tk
from tkinter import messagebox
import base_datos
import pdf_manager
import webbrowser
import urllib.parse

def conmutar_colocacion(variable_colocacion, entrada_mo_m2, entrada_ins_m2, guardar_fn):
    estado = "normal" if variable_colocacion.get() else "disabled"
    entrada_mo_m2.config(state=estado)
    entrada_ins_m2.config(state=estado)
    guardar_fn()

def conmutar_flete(variable_flete, entrada_flete, check_flete_gratis, guardar_fn):
    estado = "normal" if variable_flete.get() else "disabled"
    entrada_flete.config(state=estado)
    check_flete_gratis.config(state=estado)
    guardar_fn()

def conmutar_flete(variable_flete, entrada_flete, check_flete_gratis, guardar_fn):
    estado = "normal" if variable_flete.get() else "disabled"
    entrada_flete.config(state=estado)
    check_flete_gratis.config(state=estado)
    guardar_fn()

def conmutar_molduras(variable_molduras, entrada_metros_lineales, check_sin_cargo, guardar_fn):
    estado = "normal" if variable_molduras.get() else "disabled"
    entrada_metros_lineales.config(state=estado)
    check_sin_cargo.config(state=estado)
    guardar_fn()

def clonar_domicilio_particular(variable_clonar, var_domicilio, var_dom_inst, guardar_fn):
    var_dom_inst.set(var_domicilio.get().strip() if variable_clonar.get() else "")
    guardar_fn()

def buscar_cliente_historico_modular(ui_map, guardar_fn, limpiar_fn):
    entrada_dni = ui_map["entrada_dni"]
    var_cliente = ui_map["var_cliente"]
    entrada_telefono = ui_map["entrada_telefono"]
    var_email = ui_map["var_email"]

    criterio = entrada_dni.get().strip()
    if not criterio: criterio = var_cliente.get().strip()
    if not criterio: criterio = entrada_telefono.get().strip()
    if not criterio: criterio = var_email.get().strip()
        
    if not criterio:
        messagebox.showwarning("Atención", "Por favor ingrese un Nombre, DNI, Teléfono o Correo para buscar.")
        return
        
    r = base_datos.buscar_presupuesto_completo(criterio)
    if r:
        limpiar_fn()
        ui_map["var_cliente"].set(str(r[1]))         
        entrada_dni.insert(0, str(r[2]))             
        entrada_telefono.insert(0, str(r[3]))         
        ui_map["var_email"].set(str(r[4]))           
        ui_map["var_domicilio"].set(str(r[5]))       
        ui_map["var_dom_inst"].set(str(r[6]))        
        ui_map["var_observaciones"].set(str(r[7]))   
        
        ui_map["entrada_metros"].insert(0, str(int(r[8]) if r[8].is_integer() else r[8]))
        ui_map["var_modelo"].set(str(r[9]))
        ui_map["entrada_ancho"].insert(0, str(int(r[10]) if r[10].is_integer() else r[10]))
        ui_map["entrada_alto"].insert(0, str(int(r[11]) if r[11].is_integer() else r[11]))
        ui_map["combo_destino"].set(str(r[12]))
        
        messagebox.showinfo("🔍 Buscador KROMA3D", f"¡Historial comercial de '{r[1]}' recuperado con éxito!")
        guardar_fn()
    else:
        messagebox.showinfo("🔍 Buscador KROMA3D", f"No se encontró ningún cliente registrado con el dato: '{criterio}'")
def guardar_presupuesto(ui, limpiar_fn, actualizar_tab_fn):
    try:
        cliente = ui["var_cliente"].get().strip()
        dni_sucio = ui["entrada_dni"].get().strip()
        tel_sucio = ui["entrada_telefono"].get().strip()
        email = ui["var_email"].get().strip()
        domicilio = ui["var_domicilio"].get().strip()
        dom_inst = ui["var_dom_inst"].get().strip()
        observaciones_obra = ui["var_observaciones"].get().strip()
        metros_str = ui["entrada_metros"].get().strip()
        modelo_placa = ui["var_modelo"].get().strip()
        ancho_str = ui["entrada_ancho"].get().strip()
        alto_str = ui["entrada_alto"].get().strip()
        destino_placa = ui["combo_destino"].get()
        lleva_pintura = ui["variable_pintura"].get()
        incluye_colocacion = ui["variable_colocacion"].get()
        incluye_flete = ui["variable_flete"].get()
        flete_str = ui["entrada_flete"].get().strip()
        flete_gratis = ui["variable_flete_gratis"].get()
        lleva_molduras = ui["variable_molduras"].get()
        metros_lineales_str = ui["entrada_metros_lineales"].get().strip()
        molduras_sin_cargo = ui["variable_sin_cargo"].get()
        descuento_str = ui["entrada_descuento"].get().strip()
        entrega_inmediata = ui["variable_inmediata"].get()

        if not cliente or not dni_sucio or not tel_sucio or not email or not domicilio or not dom_inst or not metros_str or not modelo_placa:
            messagebox.showerror("Faltan datos", "Por favor completa toda la ficha del cliente, los metros cuadrados y el modelo de la placa.")
            return

        dni = re.sub(r'\D', '', dni_sucio)
        telefono = re.sub(r'\D', '', tel_sucio)

        mano_obra = 0.0
        insumos_coloc = 0.0
        if incluye_colocacion:
            mano_obra = float(ui["entrada_mo_m2"].get().strip())
            insumos_coloc = float(ui["entrada_ins_m2"].get().strip())

        costo_flete = 0.0
        if incluye_flete and not flete_gratis:
            costo_flete = float(flete_str)

        metros_lineales = float(metros_lineales_str) if lleva_molduras else 0.0
        metros = float(metros_str)
        ancho_placa = float(ancho_str)
        alto_placa = float(alto_str)
        descuento_general = float(descuento_str) if descuento_str else 0.0

        base_datos.calcular_e_insertar(
            cliente, dni, telefono, email, domicilio, dom_inst, observaciones_obra, metros, modelo_placa, ancho_placa, alto_placa, destino_placa, lleva_pintura, 
            incluye_colocacion, mano_obra, insumos_coloc, incluye_flete, costo_flete, 
            lleva_molduras, metros_lineales, molduras_sin_cargo, descuento_general, entrega_inmediata
        )
        
        messagebox.showinfo("KROMA3D", "¡Presupuesto guardado con éxito!")
        limpiar_fn()
        actualizar_tab_fn()
        
    except ValueError:
        messagebox.showerror("Error de formato", "Revisá las celdas de producción. Ingresá números enteros redondos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un detalle inesperado: {str(e)}")

def imprimir_pdf_presupuesto(tabla):
    seleccion = tabla.focus()
    if not seleccion:
        messagebox.showwarning("Atención", "Por favor, selecciona un presupuesto del listado.")
        return
    valores_tabla = tabla.item(seleccion, 'values')
    id_presupuesto = valores_tabla[0]
    p = base_datos.buscar_presupuesto_completo(id_presupuesto)
    if p:
        pdf_manager.generar_pdf_presupuesto(p)
        messagebox.showinfo("KROMA3D", f"¡PDF del presupuesto N° {id_presupuesto} generado con éxito!")

# --- 🌟 REPARADO DEFINITIVO: Extractor indexado milimétricamente con limpiador de fecha ---
def abrir_pdf_seleccionado(tabla):
    seleccion = tabla.focus()
    if not seleccion:
        messagebox.showwarning("Atención", "Por favor, selecciona un presupuesto del listado.")
        return
    valores_tabla = tabla.item(seleccion, 'values')
    id_presupuesto = valores_tabla[0]
    p = base_datos.buscar_presupuesto_completo(id_presupuesto)
    if p:
        cliente_nombre = p[1]
        emision_fecha = p[28]
        fecha_limpia = emision_fecha.replace("/", "-")
        nombre_limpio_cliente = cliente_nombre.replace(" ", "_")
        
        base_nombre = f"Presupuesto_{nombre_limpio_cliente}_Nro_{id_presupuesto}_{fecha_limpia}"
        ruta_normal = os.path.join("presupuestos_emitidos", f"{base_nombre}.pdf")
        ruta_modificado = os.path.join("presupuestos_emitidos", f"{base_nombre}_MODIFICADO.pdf")
        ruta_final = ruta_modificado if os.path.exists(ruta_modificado) else ruta_normal
        
        if os.path.exists(ruta_final):
            os.startfile(ruta_final)
        else:
            messagebox.showerror("Archivo no encontrado", f"No se encontró el PDF físico del presupuesto N° {id_presupuesto}.\nSi es un registro viejo, volvé a crearlo presionando el botón naranja.")

def borrar_presupuesto(tabla, actualizar_tab_fn):
    seleccion = tabla.focus()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un presupuesto para eliminar.")
        return
    valores_tabla = tabla.item(seleccion, 'values')
    id_presupuesto = valores_tabla[0]
    if messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar el presupuesto N° {id_presupuesto}?"):
        base_datos.eliminar_presupuesto(id_presupuesto)
        messagebox.showinfo("KROMA3D", "¡Registro eliminado!")
        actualizar_tab_fn()

def recuperar_presupuesto_en_pantalla(tabla, ui):
    seleccion = tabla.focus()
    if not seleccion:
        messagebox.showwarning("Atención", "Por favor, selecciona un presupuesto.")
        return
    valores_tabla = tabla.item(seleccion, 'values')
    id_presupuesto = valores_tabla[0]
    p = base_datos.buscar_presupuesto_completo(id_presupuesto)
    if p:
        ui["var_cliente"].set(p[1])
        ui["entrada_dni"].delete(0, tk.END); ui["entrada_dni"].insert(0, str(p[2]))
        ui["entrada_telefono"].delete(0, tk.END); ui["entrada_telefono"].insert(0, str(p[3]))
        ui["var_email"].set(p[4]); ui["var_domicilio"].set(p[5]); ui["var_dom_inst"].set(p[6]); ui["var_observaciones"].set(p[7])
        ui["entrada_metros"].delete(0, tk.END); ui["entrada_metros"].insert(0, str(int(p[8]) if p[8].is_integer() else p[8]))
        ui["var_modelo"].set(p[9])
        ui["entrada_ancho"].delete(0, tk.END); ui["entrada_ancho"].insert(0, str(int(p[10]) if p[10].is_integer() else p[10]))
        ui["entrada_alto"].delete(0, tk.END); ui["entrada_alto"].insert(0, str(int(p[11]) if p[11].is_integer() else p[11]))
        ui["combo_destino"].set(p[12])
        ui["variable_pintura"].set(True if p[13] == 1 else False)
        
        ui["variable_colocacion"].set(True if p[14] == 1 else False)
        ui["variable_flete"].set(True if p[17] == 1 else False)
        ui["variable_molduras"].set(True if p[19] == 1 else False)
        
        ui["conmutar_colocacion_fn"]()
        ui["conmutar_flete_fn"]()
        ui["conmutar_molduras_fn"]()
        
        ui["entrada_descuento"].delete(0, tk.END); ui["entrada_descuento"].insert(0, str(int(p[25]) if p[25].is_integer() else p[25]))
        messagebox.showinfo("KROMA3D", f"¡Presupuesto N° {id_presupuesto} recuperado en pantalla con éxito!")

def abrir_coordenadas_google_maps(var_dom_inst):
    direccion_sucia = var_dom_inst.get().strip()
    if not direccion_sucia:
        messagebox.showwarning("Atención", "Por favor, ingrese un domicilio de obra para buscar en el mapa.")
        return
    texto_busqueda = f"{direccion_sucia}, Mendoza, Argentina"
    texto_codificado = urllib.parse.quote(texto_busqueda)
    dominio_base = "https://google.com"
    ruta_mapa = "/maps/search/?api=1&query="
    enlace_final_blindado = dominio_base + ruta_mapa + texto_codificado
    webbrowser.open(enlace_final_blindado, new=2)
