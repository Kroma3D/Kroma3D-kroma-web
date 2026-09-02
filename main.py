import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import json
import base_datos
import calculos_interfaz

ARCHIVO_RESPALDO = "respaldo_formulario.json"

# --- Inicialización de Ventana Comercial ---
ventana = tk.Tk()
ventana.title("KROMA3D Revestimientos - Módulo Comercial")

ancho_ventana = 1200
alto_ventana = 620
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
pos_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
pos_y = int((alto_pantalla / 2) - (alto_ventana / 2))
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
def guardar_respaldo_temporal(*args):
    """Guarda de forma invisible el estado de cada celda por seguridad."""
    try:
        datos = {
            "cliente": var_cliente.get(), "dni": entrada_dni.get(), "telefono": entrada_telefono.get(), "email": var_email.get(),
            "domicilio": var_domicilio.get(), "dom_inst": var_dom_inst.get(), "observaciones": var_observaciones.get(),
            "modelo": var_modelo.get(), "ancho": entrada_ancho.get(), "alto": entrada_alto.get(), "destino": combo_destino.get(),
            "metros": entrada_metros.get(), "pintura": variable_pintura.get(), "colocacion": variable_colocacion.get(),
            "flete": variable_flete.get(), "flete_monto": entrada_flete.get(), "flete_gratis": variable_flete_gratis.get(),
            "molduras": variable_molduras.get(), "metros_lineales": entrada_metros_lineales.get(), "molduras_gratis": variable_sin_cargo.get(),
            "inmediata": variable_inmediata.get(), "descuento": entrada_descuento.get(), "clonar": variable_clonar.get(),
            "ya_px": entrada_ya_px.get(), "ya_ct": entrada_ya_ct.get(), "yq_px": entrada_yq_px.get(), "yq_ct": entrada_yq_ct.get(),
            "cb_px": entrada_cb_px.get(), "cb_ct": entrada_cb_ct.get(), "re_px": entrada_re_px.get(), "re_ct": entrada_re_ct.get(),
            "hi_px": entrada_hi_px.get(), "hi_ct": entrada_hi_ct.get(), "fi_px": entrada_fi_px.get(), "fi_ct": entrada_fi_ct.get(),
            "pi_px": entrada_pi_px.get(), "pi_ct": entrada_pi_ct.get(), "mo_m2": entrada_mo_m2.get(), "ins_m2": entrada_ins_m2.get(),
            "p_moldura": entrada_p_moldura.get(), "receta_activa": combo_receta_ext.get()
        }
        with open(ARCHIVO_RESPALDO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    except Exception: pass

def cargar_respaldo_temporal():
    """Recupera el respaldo temporal de celdas e inyecta de forma fija tus costos históricos de SQLite al arrancar."""
    try:
        costos = base_datos.obtener_costos_vigentes()
        if costos:
            entrada_ya_px.delete(0, tk.END); entrada_ya_px.insert(0, str(int(costos[0]) if costos[0].is_integer() else costos[0]))
            entrada_ya_ct.delete(0, tk.END); entrada_ya_ct.insert(0, str(int(costos[1]) if costos[1].is_integer() else costos[1]))
            entrada_yq_px.delete(0, tk.END); entrada_yq_px.insert(0, str(int(costos[2]) if costos[2].is_integer() else costos[2]))
            entrada_yq_ct.delete(0, tk.END); entrada_yq_ct.insert(0, str(int(costos[3]) if costos[3].is_integer() else costos[3]))
            entrada_cb_px.delete(0, tk.END); entrada_cb_px.insert(0, str(int(costos[4]) if costos[4].is_integer() else costos[4]))
            entrada_cb_ct.delete(0, tk.END); entrada_cb_ct.insert(0, str(int(costos[5]) if costos[5].is_integer() else costos[5]))
            entrada_re_px.delete(0, tk.END); entrada_re_px.insert(0, str(int(costos[6]) if costos[6].is_integer() else costos[6]))
            entrada_re_ct.delete(0, tk.END); entrada_re_ct.insert(0, str(int(costos[7]) if costos[7].is_integer() else costos[7]))
            entrada_hi_px.delete(0, tk.END); entrada_hi_px.insert(0, str(int(costos[8]) if costos[8].is_integer() else costos[8]))
            entrada_hi_ct.delete(0, tk.END); entrada_hi_ct.insert(0, str(int(costos[9]) if costos[9].is_integer() else costos[9]))
            entrada_fi_px.delete(0, tk.END); entrada_fi_px.insert(0, str(int(costos[10]) if costos[10].is_integer() else costos[10]))
            entrada_fi_ct.delete(0, tk.END); entrada_fi_ct.insert(0, str(int(costos[11]) if costos[11].is_integer() else costos[11]))
            entrada_pi_px.delete(0, tk.END); entrada_pi_px.insert(0, str(int(costos[12]) if costos[12].is_integer() else costos[12]))
            entrada_pi_ct.delete(0, tk.END); entrada_pi_ct.insert(0, str(int(costos[13]) if costos[13].is_integer() else costos[13]))
            combo_receta_ext.set(costos[14])
            entrada_mo_m2.delete(0, tk.END); entrada_mo_m2.insert(0, str(int(costos[15]) if costos[15].is_integer() else costos[15]))
            entrada_ins_m2.delete(0, tk.END); entrada_ins_m2.insert(0, str(int(costos[16]) if costos[16].is_integer() else costos[16]))
            entrada_p_moldura.delete(0, tk.END); entrada_p_moldura.insert(0, str(int(costos[17]) if costos[17].is_integer() else costos[17]))
    except Exception: pass

    if not os.path.exists(ARCHIVO_RESPALDO): return
    try:
        with open(ARCHIVO_RESPALDO, "r", encoding="utf-8") as f: datos = json.load(f)
        var_cliente.set(datos.get("cliente", ""))
        entrada_dni.delete(0, tk.END); entrada_dni.insert(0, datos.get("dni", ""))
        entrada_telefono.delete(0, tk.END); entrada_telefono.insert(0, datos.get("telefono", ""))
        var_email.set(datos.get("email", "")); var_domicilio.set(datos.get("domicilio", "")); var_dom_inst.set(datos.get("dom_inst", ""))
        var_observaciones.set(datos.get("observaciones", "")); var_modelo.set(datos.get("modelo", ""))
        entrada_ancho.delete(0, tk.END); entrada_ancho.insert(0, datos.get("ancho", ""))
        entrada_alto.delete(0, tk.END); entrada_alto.insert(0, datos.get("alto", ""))
        combo_destino.set(datos.get("destino", "Interior")); variable_pintura.set(datos.get("pintura", False))
        entrada_metros.delete(0, tk.END); entrada_metros.insert(0, datos.get("metros", ""))
        variable_colocacion.set(datos.get("colocacion", False)); variable_flete.set(datos.get("flete", False))
        variable_flete_gratis.set(datos.get("flete_gratis", False)); entrada_flete.delete(0, tk.END)
        entrada_flete.insert(0, datos.get("flete_monto", "12000")); variable_molduras.set(datos.get("molduras", False))
        entrada_metros_lineales.delete(0, tk.END); entrada_metros_lineales.insert(0, datos.get("metros_lineales", ""))
        variable_sin_cargo.set(datos.get("molduras_gratis", False)); variable_inmediata.set(datos.get("inmediata", False))
        entrada_descuento.delete(0, tk.END); entrada_descuento.insert(0, datos.get("descuento", "0"))
        variable_clonar.set(datos.get("clonar", False))
    except Exception: pass
def actualizar_tabla():
    for elemento in tabla.get_children(): tabla.delete(elemento)
    for p in base_datos.obtener_presupuestos(): tabla.insert("", tk.END, values=p)

def salir_sistema():
    if messagebox.askyesno("Salir", "¿Seguro que desea cerrar el panel comercial de KROMA3D?"): ventana.destroy()

def limpiar_formulario():
    var_cliente.set(""); entrada_dni.delete(0, tk.END); entrada_telefono.delete(0, tk.END)
    var_email.set(""); var_domicilio.set(""); var_dom_inst.set(""); var_observaciones.set("")
    entrada_metros.delete(0, tk.END); var_modelo.set(""); entrada_ancho.delete(0, tk.END); entrada_alto.delete(0, tk.END)
    combo_destino.set("Interior"); variable_pintura.set(False); variable_inmediata.set(False)
    variable_colocacion.set(False); variable_flete.set(False); variable_flete_gratis.set(False)
    entrada_flete.delete(0, tk.END); entrada_flete.insert(0, "12000")
    variable_molduras.set(False); variable_sin_cargo.set(False); entrada_metros_lineales.delete(0, tk.END)
    variable_clonar.set(False)
    calculos_interfaz.conmutar_colocacion(variable_colocacion, entrada_mo_m2, entrada_ins_m2, guardar_respaldo_temporal)
    calculos_interfaz.conmutar_flete(variable_flete, entrada_flete, check_flete_gratis, guardar_respaldo_temporal)
    calculos_interfaz.conmutar_molduras(variable_molduras, entrada_metros_lineales, check_sin_cargo, guardar_respaldo_temporal)
    if os.path.exists(ARCHIVO_RESPALDO):
        try: os.remove(ARCHIVO_RESPALDO)
        except Exception: pass

def forzar_mayusculas(*args):
    try:
        var_cliente.set(var_cliente.get().upper()); var_domicilio.set(var_domicilio.get().upper())
        var_dom_inst.set(var_dom_inst.get().upper()); var_observaciones.set(var_observaciones.get().upper())
        var_modelo.set(var_modelo.get().upper()); guardar_respaldo_temporal()
    except Exception: pass

def forzar_minusculas(*args):
    try: var_email.set(var_email.get().lower()); guardar_respaldo_temporal()
    except Exception: pass
def guardar_presupuesto_local():
    ui_map = {
        "var_cliente": var_cliente, "entrada_dni": entrada_dni, "entrada_telefono": entrada_telefono, "var_email": var_email,
        "var_domicilio": var_domicilio, "var_dom_inst": var_dom_inst, "var_observaciones": var_observaciones,
        "entrada_metros": entrada_metros, "var_modelo": var_modelo, "entrada_ancho": entrada_ancho, "entrada_alto": entrada_alto,
        "combo_destino": combo_destino, "variable_pintura": variable_pintura, "variable_colocacion": variable_colocacion,
        "variable_flete": variable_flete, "entrada_flete": entrada_flete, "variable_flete_gratis": variable_flete_gratis,
        "variable_molduras": variable_molduras, "entrada_metros_lineales": entrada_metros_lineales, "variable_sin_cargo": variable_sin_cargo,
        "entrada_descuento": entrada_descuento, "variable_inmediata": variable_inmediata, "entrada_mo_m2": entrada_mo_m2, "entrada_ins_m2": entrada_ins_m2
    }
    calculos_interfaz.guardar_presupuesto(ui_map, limpiar_formulario, actualizar_tabla)

def recuperar_local():
    ui_map = {
        "var_cliente": var_cliente, "entrada_dni": entrada_dni, "entrada_telefono": entrada_telefono, "var_email": var_email,
        "var_domicilio": var_domicilio, "var_dom_inst": var_dom_inst, "var_observaciones": var_observaciones,
        "entrada_metros": entrada_metros, "var_modelo": var_modelo, "entrada_ancho": entrada_ancho, "entrada_alto": entrada_alto,
        "combo_destino": combo_destino, "variable_pintura": variable_pintura, "variable_colocacion": variable_colocacion,
        "variable_flete": variable_flete, "variable_molduras": variable_molduras, "entrada_descuento": entrada_descuento,
        "conmutar_colocacion_fn": lambda: calculos_interfaz.conmutar_colocacion(variable_colocacion, entrada_mo_m2, entrada_ins_m2, guardar_respaldo_temporal),
        "conmutar_flete_fn": lambda: calculos_interfaz.conmutar_flete(variable_flete, entrada_flete, check_flete_gratis, guardar_respaldo_temporal),
        "conmutar_molduras_fn": lambda: calculos_interfaz.conmutar_molduras(variable_molduras, entrada_metros_lineales, check_sin_cargo, guardar_respaldo_temporal)
    }
    calculos_interfaz.recuperar_presupuesto_en_pantalla(tabla, ui_map)
    control_pestanas.select(pestana_carga)

def actualizar_costos_desde_panel():
    try:
        base_datos.actualizar_costos_fabrica(
            float(entrada_ya_px.get()), float(entrada_ya_ct.get()), float(entrada_yq_px.get()), float(entrada_yq_ct.get()),
            float(entrada_cb_px.get()), float(entrada_cb_ct.get()), float(entrada_re_px.get()), float(entrada_re_ct.get()),
            float(entrada_hi_px.get()), float(entrada_hi_ct.get()), float(entrada_fi_px.get()), float(entrada_fi_ct.get()),
            float(entrada_pi_px.get()), float(entrada_pi_ct.get()), combo_receta_ext.get(), float(entrada_mo_m2.get()),
            float(entrada_ins_m2.get()), float(entrada_p_moldura.get())
        )
        messagebox.showinfo("KROMA3D", "¡Calculadora de Insumos de Fábrica actualizada con éxito!")
        guardar_respaldo_temporal()
    except ValueError:
        messagebox.showerror("Error numérico", "Revisá las celdas del panel de insumos.")

# --- 🌟 ESTRUCTURA: Armado del Chasis de Solapas Superiores ---
control_pestanas = ttk.Notebook(ventana)
control_pestanas.pack(fill="both", expand=True, padx=5, pady=5)

pestana_carga = tk.Frame(control_pestanas)
pestana_historial = tk.Frame(control_pestanas)

control_pestanas.add(pestana_carga, text=" 📋 Panel de Cotización Actual ")
control_pestanas.add(pestana_historial, text=" 📊 Historial General de Ventas ")
# =========================================================================
# SOLAPA 1: CONTENIDO DEL PANEL DE COTIZACIÓN (Se monta en pestana_carga)
# =========================================================================
var_cliente, var_email, var_domicilio, var_dom_inst, var_observaciones, var_modelo = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
var_cliente.trace_add("write", forzar_mayusculas); var_domicilio.trace_add("write", forzar_mayusculas)
var_dom_inst.trace_add("write", forzar_mayusculas); var_observaciones.trace_add("write", forzar_mayusculas); var_modelo.trace_add("write", forzar_mayusculas)
var_email.trace_add("write", forzar_minusculas)

ficha_cliente = tk.LabelFrame(pestana_carga, text=" 👤 Ficha del Cliente y Proyecto ", font=("Arial", 10, "bold"), fg="#1A365D", padx=15, pady=8)
ficha_cliente.pack(fill="x", padx=15, pady=4)

tk.Label(ficha_cliente, text="Nombre Cliente:").grid(row=0, column=0, sticky="e", pady=4)
entrada_cliente = tk.Entry(ficha_cliente, textvariable=var_cliente, width=42); entrada_cliente.grid(row=0, column=1, sticky="w", padx=5, pady=4)
tk.Label(ficha_cliente, text="DNI / CUIT:").grid(row=0, column=2, sticky="e", pady=4)
entrada_dni = tk.Entry(ficha_cliente, width=16); entrada_dni.grid(row=0, column=3, sticky="w", padx=5, pady=4)
tk.Label(ficha_cliente, text="Teléfono Celular:").grid(row=0, column=4, sticky="e", pady=4)
entrada_telefono = tk.Entry(ficha_cliente, width=16); entrada_telefono.grid(row=0, column=5, sticky="w", padx=5, pady=4)

btn_buscar_h = tk.Button(ficha_cliente, text=" 🔍 Buscar Histórico ", command=lambda: calculos_interfaz.buscar_cliente_historico_modular({"entrada_dni": entrada_dni, "var_cliente": var_cliente, "entrada_telefono": entrada_telefono, "var_email": var_email, "var_domicilio": var_domicilio, "var_dom_inst": var_dom_inst, "var_observaciones": var_observaciones, "entrada_metros": entrada_metros, "var_modelo": var_modelo, "entrada_ancho": entrada_ancho, "entrada_alto": entrada_alto, "combo_destino": combo_destino}, guardar_respaldo_temporal, limpiar_formulario), bg="#1A365D", fg="white", font=("Arial", 9, "bold"), width=16)
btn_buscar_h.grid(row=0, column=6, padx=10, pady=4, sticky="w")

btn_limpiar_arriba = tk.Button(ficha_cliente, text=" 🧼 Limpiar Pantalla ", command=limpiar_formulario, bg="#78909C", fg="white", font=("Arial", 9, "bold"), width=16)
btn_limpiar_arriba.grid(row=1, column=6, padx=10, pady=4, sticky="w")


tk.Label(ficha_cliente, text="Correo Electrónico:").grid(row=1, column=0, sticky="e", pady=4)
entrada_email = tk.Entry(ficha_cliente, textvariable=var_email, width=42); entrada_email.grid(row=1, column=1, sticky="w", padx=5, pady=4)
tk.Label(ficha_cliente, text="Domicilio Particular:").grid(row=2, column=0, sticky="e", pady=4)
entrada_domicilio = tk.Entry(ficha_cliente, textvariable=var_domicilio, width=85); entrada_domicilio.grid(row=2, column=1, columnspan=5, sticky="w", padx=5, pady=4)
tk.Label(ficha_cliente, text="Domicilio Obra:").grid(row=3, column=0, sticky="e", pady=4)
entrada_dom_inst = tk.Entry(ficha_cliente, textvariable=var_dom_inst, width=85); entrada_dom_inst.grid(row=3, column=1, columnspan=5, sticky="w", padx=5, pady=4)

variable_clonar = tk.BooleanVar()
check_clonar = tk.Checkbutton(ficha_cliente, text="Copiar Domicilio Particular", variable=variable_clonar, command=lambda: calculos_interfaz.clonar_domicilio_particular(variable_clonar, var_domicilio, var_dom_inst, guardar_respaldo_temporal), font=("Arial", 9, "bold"), fg="#2B6CB0")
check_clonar.grid(row=3, column=6, sticky="w", padx=5)

btn_maps_obra = tk.Button(ficha_cliente, text="📍 Ver en Maps", command=lambda: calculos_interfaz.abrir_coordenadas_google_maps(var_dom_inst), bg="#008CBA", fg="white", font=("Arial", 9, "bold"), width=16)
btn_maps_obra.grid(row=4, column=6, sticky="w", padx=10, pady=4)


tk.Label(ficha_cliente, text="Observaciones Obra:").grid(row=4, column=0, sticky="e", pady=4)
entrada_observaciones = tk.Entry(ficha_cliente, textvariable=var_observaciones, width=85); entrada_observaciones.grid(row=4, column=1, columnspan=5, sticky="w", padx=5, pady=4)

formulario = tk.LabelFrame(pestana_carga, text=" 📐 Especificaciones del Material y Servicios de Obra ", font=("Arial", 10, "bold"), fg="#1A365D", padx=15, pady=8)
formulario.pack(fill="x", padx=15, pady=4)

tk.Label(formulario, text="Modelo Placa:").grid(row=0, column=0, sticky="e", pady=4)
entrada_modelo = tk.Entry(formulario, textvariable=var_modelo, width=16); entrada_modelo.grid(row=0, column=1, padx=5, pady=4, sticky="w")
tk.Label(formulario, text="Ancho (cm):").grid(row=0, column=2, sticky="e", pady=4)
entrada_ancho = tk.Entry(formulario, width=8); entrada_ancho.grid(row=0, column=3, padx=5, pady=4, sticky="w")
tk.Label(formulario, text="Alto (cm):").grid(row=0, column=4, sticky="e", pady=4)
entrada_alto = tk.Entry(formulario, width=8); entrada_alto.grid(row=0, column=5, padx=5, pady=4, sticky="w")
tk.Label(formulario, text="Línea Destino:").grid(row=0, column=6, sticky="e", pady=4)
combo_destino = ttk.Combobox(formulario, width=12, state="readonly", values=["Interior", "Exterior"]); combo_destino.grid(row=0, column=7, padx=5, pady=4, sticky="w")

tk.Label(formulario, text="Superficie (m²):").grid(row=1, column=0, sticky="e", pady=4)
entrada_metros = tk.Entry(formulario, width=16); entrada_metros.grid(row=1, column=1, padx=5, pady=4, sticky="w")

variable_pintura = tk.BooleanVar()
check_pintura = tk.Checkbutton(formulario, text="Lleva Tratamiento / Pintura Fábrica", variable=variable_pintura, command=guardar_respaldo_temporal, font=("Arial", 9, "bold"))
check_pintura.grid(row=1, column=2, columnspan=3, sticky="w", padx=5, pady=4)

variable_colocacion = tk.BooleanVar()
check_colocacion = tk.Checkbutton(formulario, text="Incluye Servicio Colocación", variable=variable_colocacion, command=lambda: calculos_interfaz.conmutar_colocacion(variable_colocacion, entrada_mo_m2, entrada_ins_m2, guardar_respaldo_temporal), font=("Arial", 9, "bold"))
check_colocacion.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=4)

variable_flete = tk.BooleanVar()
check_flete = tk.Checkbutton(formulario, text="Incluye Flete / Distribución:", variable=variable_flete, command=lambda: calculos_interfaz.conmutar_flete(variable_flete, entrada_flete, check_flete_gratis, guardar_respaldo_temporal), font=("Arial", 9, "bold"))
check_flete.grid(row=2, column=2, columnspan=2, sticky="w", padx=5, pady=4)
entrada_flete = tk.Entry(formulario, width=12, state="disabled"); entrada_flete.grid(row=2, column=4, padx=5, sticky="w", pady=4)

variable_flete_gratis = tk.BooleanVar()
check_flete_gratis = tk.Checkbutton(formulario, text="Envío SIN CARGO Logístico", variable=variable_flete_gratis, state="disabled", command=guardar_respaldo_temporal, font=("Arial", 9, "bold"), fg="#2B6CB0")
check_flete_gratis.grid(row=2, column=5, columnspan=2, sticky="w", padx=5, pady=4)

variable_molduras = tk.BooleanVar()
check_molduras = tk.Checkbutton(formulario, text="Lleva Molduras Terminación", variable=variable_molduras, command=lambda: calculos_interfaz.conmutar_molduras(variable_molduras, entrada_metros_lineales, check_sin_cargo, guardar_respaldo_temporal), font=("Arial", 9, "bold"))
check_molduras.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=4)
tk.Label(formulario, text="Metros Lineales:").grid(row=3, column=2, sticky="e", pady=4)
entrada_metros_lineales = tk.Entry(formulario, width=10, state="disabled"); entrada_metros_lineales.grid(row=3, column=3, padx=5, sticky="w", pady=4)

variable_sin_cargo = tk.BooleanVar()
check_sin_cargo = tk.Checkbutton(formulario, text="Molduras BASE GRATIS (Promoción -100%)", variable=variable_sin_cargo, state="disabled", command=guardar_respaldo_temporal, font=("Arial", 9, "bold"), fg="#2B6CB0")
check_sin_cargo.grid(row=3, column=4, columnspan=4, sticky="w", padx=5, pady=4)
ajustes_panel = tk.LabelFrame(pestana_carga, text=" 💾 Calculadora de Insumos Básicos y Ajustes de Costos Comerciales ", font=("Arial", 9, "bold"), fg="#2B6CB0", padx=12, pady=6)
ajustes_panel.pack(fill="x", padx=15, pady=4)

tk.Label(ajustes_panel, text="Bolsa Yeso Cerámico ($):").grid(row=0, column=0, sticky="e", pady=2)
entrada_ya_px = tk.Entry(ajustes_panel, width=9); entrada_ya_px.grid(row=0, column=1, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (KG):").grid(row=0, column=2, sticky="e", pady=2)
entrada_ya_ct = tk.Entry(ajustes_panel, width=6); entrada_ya_ct.grid(row=0, column=3, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Bolsa Yeso Químico ($):").grid(row=0, column=4, sticky="e", pady=2)
entrada_yq_px = tk.Entry(ajustes_panel, width=9); entrada_yq_px.grid(row=0, column=5, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (KG):").grid(row=0, column=6, sticky="e", pady=2)
entrada_yq_ct = tk.Entry(ajustes_panel, width=6); entrada_yq_ct.grid(row=0, column=7, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Balde Pintura Fáb. ($):").grid(row=0, column=8, sticky="e", pady=2)
entrada_pi_px = tk.Entry(ajustes_panel, width=9); entrada_pi_px.grid(row=0, column=9, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (Lts):").grid(row=0, column=10, sticky="e", pady=2)
entrada_pi_ct = tk.Entry(ajustes_panel, width=6); entrada_pi_ct.grid(row=0, column=11, padx=4, pady=2, sticky="w")

tk.Label(ajustes_panel, text="Bolsa Cem. Blanco ($):").grid(row=1, column=0, sticky="e", pady=2)
entrada_cb_px = tk.Entry(ajustes_panel, width=9); entrada_cb_px.grid(row=1, column=1, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (KG):").grid(row=1, column=2, sticky="e", pady=2)
entrada_cb_ct = tk.Entry(ajustes_panel, width=6); entrada_cb_ct.grid(row=1, column=3, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Bidón Resina ($):").grid(row=1, column=4, sticky="e", pady=2)
entrada_re_px = tk.Entry(ajustes_panel, width=9); entrada_re_px.grid(row=1, column=5, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (Lts):").grid(row=1, column=6, sticky="e", pady=2)
entrada_re_ct = tk.Entry(ajustes_panel, width=6); entrada_re_ct.grid(row=1, column=7, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="MO Colocador m² ($):").grid(row=1, column=8, sticky="e", pady=2)
entrada_mo_m2 = tk.Entry(ajustes_panel, width=9); entrada_mo_m2.grid(row=1, column=9, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Ins. Agarre m² ($):").grid(row=1, column=10, sticky="e", pady=2)
entrada_ins_m2 = tk.Entry(ajustes_panel, width=6); entrada_ins_m2.grid(row=1, column=11, padx=4, pady=2, sticky="w")

tk.Label(ajustes_panel, text="Bidón Hidrófugo ($):").grid(row=2, column=0, sticky="e", pady=2)
entrada_hi_px = tk.Entry(ajustes_panel, width=9); entrada_hi_px.grid(row=2, column=1, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (Lts):").grid(row=2, column=2, sticky="e", pady=2)
entrada_hi_ct = tk.Entry(ajustes_panel, width=6); entrada_hi_ct.grid(row=2, column=3, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Paq. Fibra Vidrio ($):").grid(row=2, column=4, sticky="e", pady=2)
entrada_fi_px = tk.Entry(ajustes_panel, width=9); entrada_fi_px.grid(row=2, column=5, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Contenido (KG):").grid(row=2, column=6, sticky="e", pady=2)
entrada_fi_ct = tk.Entry(ajustes_panel, width=6); entrada_fi_ct.grid(row=2, column=7, padx=4, pady=2, sticky="w")
tk.Label(ajustes_panel, text="Vta Moldura Lista ($):").grid(row=2, column=8, sticky="e", pady=2)
entrada_p_moldura = tk.Entry(ajustes_panel, width=9); entrada_p_moldura.grid(row=2, column=9, padx=4, pady=2, sticky="w")

tk.Label(ajustes_panel, text="Línea Ext. Activa:", font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="e", pady=4)
combo_receta_ext = ttk.Combobox(ajustes_panel, width=22, state="readonly", values=["Receta A (Híbrida Cemento)", "Receta B (Yeso Químico)"]); combo_receta_ext.grid(row=3, column=1, columnspan=3, padx=4, pady=4, sticky="w")
variable_inmediata = tk.BooleanVar()
check_inmediata = tk.Checkbutton(ajustes_panel, text="Entrega INMEDIATA (Stock)", variable=variable_inmediata, command=guardar_respaldo_temporal, font=("Arial", 9, "bold"))
check_inmediata.grid(row=3, column=4, columnspan=2, sticky="w", pady=4)
tk.Label(ajustes_panel, text="Descuento Gral (%):", font=("Arial", 9, "bold")).grid(row=3, column=6, sticky="e", pady=4)
entrada_descuento = tk.Entry(ajustes_panel, width=6); entrada_descuento.grid(row=3, column=7, padx=4, pady=4, sticky="w")

btn_actualizar_insumos = tk.Button(ajustes_panel, text=" 💾 Guardar Insumos Fábrica ", command=actualizar_costos_desde_panel, bg="#1A365D", fg="white", font=("Arial", 9, "bold"))
btn_actualizar_insumos.grid(row=3, column=8, columnspan=4, padx=10, pady=4, sticky="we")

panel_botones_carga = tk.Frame(pestana_carga)
panel_botones_carga.pack(pady=10)

btn_calcular = tk.Button(panel_botones_carga, text="Generar y Guardar Registro", command=guardar_presupuesto_local, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=28)
btn_calcular.grid(row=0, column=0, padx=20)

btn_cerrar_modulo = tk.Button(panel_botones_carga, text="🚪 Salir del Cotizador", command=salir_sistema, bg="#607D8B", fg="white", font=("Arial", 10, "bold"), width=22)
btn_cerrar_modulo.grid(row=0, column=1, padx=20)

# =========================================================================
# SOLAPA 2: HISTORIAL GENERAL DE VENTAS GIGANTE (Se monta en pestana_historial)
# =========================================================================
panel_tabla_gigante = tk.Frame(pestana_historial)
panel_tabla_gigante.pack(fill="both", expand=True, padx=15, pady=10)

columnas = ("N°", "Cliente", "m²", "Modelo", "Total Neto", "Monto Seña 50%", "Plazo Otorgado", "Fecha Emisión")
tabla = ttk.Treeview(panel_tabla_gigante, columns=columnas, show="headings")
for col in columnas: 
    tabla.heading(col, text=col)

tabla.column("N°", width=50, anchor="center")
tabla.column("Cliente", width=250)
tabla.column("m²", width=60, anchor="center")
tabla.column("Modelo", width=150)
tabla.column("Total Neto", width=120, anchor="e")
tabla.column("Monto Seña 50%", width=120, anchor="e")
tabla.column("Plazo Otorgado", width=260)
tabla.column("Fecha Emisión", width=110, anchor="center")

barra = ttk.Scrollbar(panel_tabla_gigante, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=barra.set)
tabla.pack(side="left", fill="both", expand=True)
barra.pack(side="right", fill="y")

panel_acciones_historial = tk.Frame(pestana_historial)
panel_acciones_historial.pack(pady=12)

btn_pdf_h = tk.Button(panel_acciones_historial, text="🖨️ Forzar Reimpresión PDF", command=lambda: calculos_interfaz.imprimir_pdf_presupuesto(tabla), bg="#FF9800", fg="white", font=("Arial", 10, "bold"), width=24)
btn_pdf_h.grid(row=0, column=0, padx=8)

btn_abrir_pdf_h = tk.Button(panel_acciones_historial, text="📄 Abrir PDF Seleccionado", command=lambda: calculos_interfaz.abrir_pdf_seleccionado(tabla), bg="#008CBA", fg="white", font=("Arial", 10, "bold"), width=24)
btn_abrir_pdf_h.grid(row=0, column=1, padx=8)

btn_recuperar_h = tk.Button(panel_acciones_historial, text="🔄 Recuperar en Pantalla", command=recuperar_local, bg="#2B6CB0", fg="white", font=("Arial", 10, "bold"), width=24)
btn_recuperar_h.grid(row=0, column=2, padx=8)

btn_borrar_h = tk.Button(panel_acciones_historial, text="❌ Eliminar Fila", command=lambda: calculos_interfaz.borrar_presupuesto(tabla, actualizar_tabla), bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=16)
btn_borrar_h.grid(row=0, column=3, padx=8)

entrada_ancho.bind("<KeyRelease>", guardar_respaldo_temporal)
entrada_alto.bind("<KeyRelease>", guardar_respaldo_temporal)
entrada_metros.bind("<KeyRelease>", guardar_respaldo_temporal)
entrada_flete.bind("<KeyRelease>", guardar_respaldo_temporal)
entrada_metros_lineales.bind("<KeyRelease>", guardar_respaldo_temporal)
entrada_descuento.bind("<KeyRelease>", guardar_respaldo_temporal)
combo_destino.bind("<<ComboboxSelected>>", guardar_respaldo_temporal)

limpiar_formulario()
cargar_respaldo_temporal()
actualizar_tabla()
ventana.mainloop()
