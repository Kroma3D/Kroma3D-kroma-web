import sqlite3
import math
from datetime import datetime, timedelta

def conectar():
    return sqlite3.connect("kroma_comercial_sistema.db")

def crear_tablas_y_configuracion():
    """Crea la estructura de SQLite e inyecta la fila de insumos inicial de forma segura."""
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            dni TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            domicilio TEXT NOT NULL,
            domicilio_instalacion TEXT NOT NULL,
            observaciones_obra TEXT NOT NULL,
            metros_cuadrados REAL NOT NULL,
            modelo_placa TEXT NOT NULL,
            ancho_placa REAL NOT NULL,
            alto_placa REAL NOT NULL,
            destino_placa TEXT NOT NULL,
            lleva_pintura TEXT NOT NULL,
            cantidad_placas INTEGER NOT NULL,
            precio_por_placa REAL NOT NULL,
            incluye_colocacion TEXT NOT NULL,
            precio_colocacion REAL NOT NULL,
            incluye_flete TEXT NOT NULL,
            precio_flete REAL NOT NULL,
            lleva_molduras TEXT NOT NULL,
            cantidad_molduras INTEGER NOT NULL,
            precio_molduras REAL NOT NULL,
            molduras_gratis TEXT NOT NULL,
            descuento_general REAL NOT NULL,
            total_estimado REAL NOT NULL,
            monto_sena REAL NOT NULL,
            plazo_entrega TEXT NOT NULL,
            fecha_emision TEXT NOT NULL,
            fecha_validez TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY,
            px_yeso_alfa REAL NOT NULL, cant_yeso_alfa REAL NOT NULL,
            px_yeso_quimico REAL NOT NULL, cant_yeso_quimico REAL NOT NULL,
            px_cemento_blanco REAL NOT NULL, cant_cemento_blanco REAL NOT NULL,
            px_resina REAL NOT NULL, cant_resina REAL NOT NULL,
            px_hidrofugo REAL NOT NULL, cant_hidrofugo REAL NOT NULL,
            px_fibra REAL NOT NULL, cant_fibra REAL NOT NULL,
            px_pintura REAL NOT NULL, cant_pintura REAL NOT NULL,
            receta_ext_activa TEXT NOT NULL,
            costo_mano_obra_m2 REAL NOT NULL,
            costo_insumos_coloc_m2 REAL NOT NULL,
            precio_venta_moldura REAL NOT NULL
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    resultado = cursor.fetchone()
    if resultado is None or resultado[0] == 0:
        cursor.execute("""
            INSERT INTO configuracion (id, px_yeso_alfa, cant_yeso_alfa, px_yeso_quimico, cant_yeso_quimico, px_cemento_blanco, cant_cemento_blanco, px_resina, cant_resina, px_hidrofugo, cant_hidrofugo, px_fibra, cant_fibra, px_pintura, cant_pintura, receta_ext_activa, costo_mano_obra_m2, costo_insumos_coloc_m2, precio_venta_moldura)
            VALUES (1, 16000.0, 40.0, 18000.0, 30.0, 18000.0, 25.0, 20000.0, 5.0, 12000.0, 5.0, 3000.0, 1.0, 45000.0, 20.0, 'Receta B (Yeso Químico)', 15000.0, 3500.0, 450.0)
        """)
        
    conexion.commit()
    conexion.close()

def obtener_costos_vigentes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT px_yeso_alfa, cant_yeso_alfa, px_yeso_quimico, cant_yeso_quimico, 
               px_cemento_blanco, cant_cemento_blanco, px_resina, cant_resina, 
               px_hidrofugo, cant_hidrofugo, px_fibra, cant_fibra, px_pintura, cant_pintura, 
               receta_ext_activa, costo_mano_obra_m2, costo_insumos_coloc_m2, precio_venta_moldura 
        FROM configuracion WHERE id = 1
    """)
    valores = cursor.fetchone()
    conexion.close()
    return valores

def actualizar_costos_fabrica(ya_px, ya_ct, yq_px, yq_ct, cb_px, cb_ct, re_px, re_ct, hi_px, hi_ct, fi_px, fi_ct, pi_px, pi_ct, activa, mano_obra, insumos, moldura):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE configuracion 
        SET px_yeso_alfa = ?, cant_yeso_alfa = ?, px_yeso_quimico = ?, cant_yeso_quimico = ?, 
            px_cemento_blanco = ?, cant_cemento_blanco = ?, px_resina = ?, cant_resina = ?, 
            px_hidrofugo = ?, cant_hidrofugo = ?, px_fibra = ?, cant_fibra = ?, px_pintura = ?, cant_pintura = ?, 
            receta_ext_activa = ?, costo_mano_obra_m2 = ?, costo_insumos_coloc_m2 = ?, precio_venta_moldura = ?
        WHERE id = 1
    """, (ya_px, ya_ct, yq_px, yq_ct, cb_px, cb_ct, re_px, re_ct, hi_px, hi_ct, fi_px, fi_ct, pi_px, pi_ct, activa, mano_obra, insumos, moldura))
    conexion.commit()
    conexion.close()
    # 🌟 AUTOMATIZADO: Genera el PDF en el mismo milisegundo que el registro ingresa a SQLite
    try:
        import pdf_manager
        cursor_id = conexion.cursor()
        cursor_id.execute("SELECT max(id) FROM budgets")
        ultimo_id = cursor_id.fetchone()[0]
        
        p_completo = buscar_presupuesto_completo(ultimo_id)
        if p_completo:
            pdf_manager.generar_pdf_presupuesto(p_completo)
    except Exception:
        pass





def calcular_e_insertar(cliente, dni, telefono, email, domicilio, dom_inst, observaciones_obra, metros_cuadrados, modelo_placa, ancho_placa, alto_placa, destino_placa, lleva_pintura, 
                        incluye_colocacion, precio_mano_obra_m2, precio_insumos_coloc_m2, 
                        incluye_flete, costo_flete, lleva_molduras, metros_lineales, molduras_sin_cargo, 
                        descuento_general, entrega_inmediata):
    
    metros_con_recortes = metros_cuadrados * 1.10
    cobertura_m2 = (ancho_placa * alto_placa) / 10000.0
    cantidad_placas = math.ceil(metros_con_recortes / cobertura_m2)
    
    ya_px, ya_ct, yq_px, yq_ct, cb_px, cb_ct, re_px, re_ct, hi_px, hi_ct, fi_px, fi_ct, pi_px, pi_ct, receta_activa, c_mo, c_ins, p_moldura = obtener_costos_vigentes()
    
    px_yeso_a_kg = ya_px / (ya_ct if ya_ct > 0 else 1.0)
    px_yeso_q_kg = yq_px / (yq_ct if yq_ct > 0 else 1.0)
    px_cemento_kg = cb_px / (cb_ct if cb_ct > 0 else 1.0)
    px_resina_ml = re_px / ((re_ct * 1000.0) if re_ct > 0 else 1.0)
    px_hidro_ml = hi_px / ((hi_ct * 1000.0) if hi_ct > 0 else 1.0)
    px_fibra_gr = fi_px / ((fi_ct * 1000.0) if fi_ct > 0 else 1.0)
    px_pintura_unidad = pi_px / ((pi_ct * 150.0) if pi_ct > 0 else 1.0)
    
    amortizacion_fija = 120.0
    
    if destino_placa == "Interior":
        costo_materia_prima = (px_yeso_a_kg * 2.2) + (px_resina_ml * 45) + (px_fibra_gr * 5) + amortizacion_fija
    else:
        if receta_activa == 'Receta B (Yeso Químico)':
            costo_materia_prima = (px_yeso_q_kg * 3.3) + (px_hidro_ml * 40) + (px_fibra_gr * 10) + amortizacion_fija
        else:
            costo_materia_prima = (px_yeso_a_kg * 2.1) + (px_cemento_kg * 0.9) + (px_hidro_ml * 40) + (px_resina_ml * 60) + (px_fibra_gr * 10) + amortizacion_fija + 30.0
            
    if lleva_paint_estado := (lleva_pintura == "Sí" or lleva_pintura == True):
        costo_materia_prima += px_pintura_unidad
        
    precio_venta_por_placa = costo_materia_prima * 3
    subtotal_placas = cantidad_placas * precio_venta_por_placa
    
    subtotal_colocacion = metros_cuadrados * (precio_mano_obra_m2 + precio_insumos_coloc_m2) if incluye_colocacion else 0.0
    total_flete = costo_flete if incluye_flete else 0.0
    
    cantidad_molduras = 0
    subtotal_molduras = 0.0
    if lleva_molduras:
        cantidad_molduras = math.ceil(metros_lineales / 0.60)
        subtotal_molduras = cantidad_molduras * p_moldura

    total_bruto = subtotal_placas + subtotal_colocacion + total_flete
    if lleva_molduras and not molduras_sin_cargo:
        total_bruto += subtotal_molduras
        
    porcentaje_desc = descuento_general / 100.0
    total_neto = total_bruto * (1.0 - porcentaje_desc)
    monto_sena = total_neto * 0.50
    
       # --- REPARADO: Motor de Plazos Proporcional Basado en Cadencia Real de Taller (9 placas/día) ---
    if entrega_inmediata:
        plazo_entrega = "INMEDIATA (DISPONIBLE PARA RETIRO/ENTREGA DE 48 A 72 HS HÁBILES POSTERIORES A LA ACREDITACIÓN DE LA SEÑA)"
    elif cantidad_placas <= 100:
        # Plazo fijo seguro para pedidos chicos/medianos de mostrador
        plazo_entrega = "15 A 20 DÍAS HÁBILES ESTIMADOS DE FABRICACIÓN (INCLUYE PROCESO DE MOLDEO Y SEMANA DE SECADO OBLIGATORIA)"
    else:
        # 📈 CALCULO PROPORCIONAL DINÁMICO: Divide las placas por tu cadencia diaria de 9 unidades
        dias_batea_reales = math.ceil(cantidad_placas / 9.0)
        # Suma la semana de secado (7) y el colchón por viento zonda/contingencias (5)
        total_dias_habiles_margen = dias_batea_reales + 7 + 5
        
        # Arma un rango comercial prolijo de una semana de margen (ej: 32 a 39 días)
        plazo_entrega = f"{total_dias_habiles_margen} A {total_dias_habiles_margen + 7} DÍAS HÁBILES ESTIMADOS (CALCULADO PROPORCIONAL POR VOLUMEN DE OBRA)"

        
    fecha_hoy = datetime.now()
    fecha_emision_texto = fecha_hoy.strftime("%d/%m/%Y")
    fecha_validez_texto = (fecha_hoy + timedelta(days=15)).strftime("%d/%m/%Y")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO budgets 
        (cliente, dni, telefono, email, domicilio, domicilio_instalacion, observaciones_obra, metros_cuadrados, modelo_placa, ancho_placa, alto_placa, destino_placa, lleva_pintura, 
         cantidad_placas, precio_por_placa, incluye_colocacion, precio_colocacion, incluye_flete, precio_flete, 
         lleva_molduras, cantidad_molduras, precio_molduras, molduras_gratis, descuento_general, total_estimado, monto_sena, 
         plazo_entrega, fecha_emision, fecha_validez, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (cliente, dni, telefono, email, domicilio, dom_inst, observaciones_obra, metros_cuadrados, modelo_placa, ancho_placa, alto_placa, destino_placa, "Sí" if lleva_paint_estado else "No", 
          cantidad_placas, precio_venta_por_placa, "Sí" if incluye_colocacion else "No", subtotal_colocacion, "Sí" if incluye_flete else "No", total_flete, 
          "Sí" if lleva_molduras else "No", cantidad_molduras, subtotal_molduras, "Sí" if molduras_sin_cargo else "No", descuento_general, 
          total_neto, monto_sena, plazo_entrega, fecha_emision_texto, fecha_validez_texto, "Pendiente"))
    conexion.commit()
    conexion.close()

def obtener_presupuestos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, cliente, metros_cuadrados, modelo_placa, total_estimado, monto_sena, plazo_entrega, fecha_emision FROM budgets")
    filas = cursor.fetchall()
    conexion.close()
    return filas

def buscar_presupuesto_completo(criterio):
    """Escanea de forma inteligente por DNI, Teléfono, Correo o cualquier palabra del Nombre."""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Si el criterio es un número limpio (como el ID de operación en la grilla)
    if str(criterio).isdigit() and len(str(criterio)) <= 5:
        cursor.execute("SELECT * FROM budgets WHERE id = ?", (criterio,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado
        
    # Motor de búsqueda comercial por palabras sueltas para el mostrador
    palabras = str(criterio).strip().split()
    if not palabras:
        conexion.close()
        return None
        
    # Construye la consulta dinámica para revisar Nombre, DNI, Teléfono y Correo simultáneamente
    condiciones = []
    parametros = []
    for p in palabras:
        condiciones.append("(cliente LIKE ? OR dni LIKE ? OR telefono LIKE ? OR email LIKE ?)")
        termino = f"%{p}%"
        parametros.extend([termino, termino, termino, termino])
        
    consulta = f"SELECT * FROM budgets WHERE {' AND '.join(condiciones)} ORDER BY id DESC"
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchone() # Trae el último presupuesto histórico emitido de ese cliente
    conexion.close()
    return resultado


def eliminar_presupuesto(id_presupuesto):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM budgets WHERE id = ?", (id_presupuesto,))
    conexion.commit()
    conexion.close()

   

def actualizar_presupuesto_existente(id_presupuesto, cliente, dni, telefono, email, domicilio, dom_inst, observaciones_obra, metros_cuadrados, modelo_placa, ancho_placa, alto_placa, destino_placa, lleva_pintura, 
                                     incluye_colocacion, precio_mano_obra_m2, price_insumos_coloc_m2, 
                                     incluye_flete, costo_flete, lleva_molduras, metros_lineales, molduras_sin_cargo, 
                                     descuento_general, entrega_inmediata):
    """Modifica y actualiza por completo un registro existente en SQLite con alineación prolija."""
    metros_con_recortes = metros_cuadrados * 1.10
    cobertura_m2 = (ancho_placa * alto_placa) / 10000.0
    cantidad_placas = math.ceil(metros_con_recortes / cobertura_m2)
    
    ya_px, ya_ct, yq_px, yq_ct, cb_px, cb_ct, re_px, re_ct, hi_px, hi_ct, fi_px, fi_ct, pi_px, pi_ct, receta_activa, c_mo, c_ins, p_moldura = obtener_costos_vigentes()
    
    px_yeso_a_kg = ya_px / (ya_ct if ya_ct > 0 else 1.0)
    px_yeso_q_kg = yq_px / (yq_ct if yq_ct > 0 else 1.0)
    px_cemento_kg = cb_px / (cb_ct if cb_ct > 0 else 1.0)
    px_resina_ml = re_px / ((re_ct * 1000.0) if re_ct > 0 else 1.0)
    px_hidro_ml = hi_px / ((hi_ct * 1000.0) if hi_ct > 0 else 1.0)
    px_fibra_gr = fi_px / ((fi_ct * 1000.0) if fi_ct > 0 else 1.0)
    px_pintura_unidad = pi_px / ((pi_ct * 150.0) if pi_ct > 0 else 1.0)
    
    amortizacion_fija = 120.0
    
    if destino_placa == "Interior":
        costo_materia_prima = (px_yeso_a_kg * 2.2) + (px_resina_ml * 45) + (px_fibra_gr * 5) + amortizacion_fija
    else:
        if receta_activa == 'Receta B (Yeso Químico)':
            costo_materia_prima = (px_yeso_q_kg * 3.3) + (px_hidro_ml * 40) + (px_fibra_gr * 10) + amortizacion_fija
        else:
            costo_materia_prima = (px_yeso_a_kg * 2.1) + (px_cemento_kg * 0.9) + (px_hidro_ml * 40) + (px_resina_ml * 60) + (px_fibra_gr * 10) + amortizacion_fija + 30.0
            
    texto_pintura = "No"
    if lleva_pintura:
        costo_materia_prima += px_pintura_unidad
        texto_pintura = "Sí"
        
    precio_venta_por_placa = costo_materia_prima * 3
    subtotal_placas = cantidad_placas * precio_venta_por_placa
    subtotal_colocacion = metros_cuadrados * (precio_mano_obra_m2 + price_insumos_coloc_m2) if incluye_colocacion else 0.0
    total_flete = costo_flete if incluye_flete else 0.0
    
    cantidad_molduras = 0
    subtotal_molduras = 0.0
    if lleva_molduras:
        cantidad_molduras = math.ceil(metros_lineales / 0.60)
        subtotal_molduras = cantidad_molduras * p_moldura

    total_bruto = subtotal_placas + subtotal_colocacion + total_flete
    if lleva_molduras and not molduras_sin_cargo:
        total_bruto += subtotal_molduras
        
    total_neto = total_bruto * (1.0 - (descuento_general / 100.0))
    monto_sena = total_neto * 0.50
    plazo_entrega = "INMEDIATA" if entrega_inmediata else ("15 DÍAS HÁBILES" if cantidad_placas < 100 else "30 DÍAS HÁBILES")

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE budgets 
        SET cliente=?, dni=?, telefono=?, email=?, domicilio=?, domicilio_instalacion=?, observaciones_obra=?, metros_cuadrados=?, modelo_placa=?, ancho_placa=?, alto_placa=?, destino_placa=?, lleva_pintura=?, 
            cantidad_placas=?, precio_por_placa=?, incluye_colocacion=?, precio_colocacion=?, incluye_flete=?, precio_flete=?, 
            lleva_molduras=?, cantidad_molduras=?, precio_molduras=?, molduras_gratis=?, descuento_general=?, total_estimado=?, monto_sena=?, plazo_entrega=?
        WHERE id=?
    """, (cliente, dni, telefono, email, domicilio, dom_inst, observaciones_obra, metros_cuadrados, modelo_placa, ancho_placa, alto_placa, destino_placa, texto_pintura, 
          cantidad_placas, precio_venta_por_placa, "Sí" if incluye_colocacion else "No", subtotal_colocacion, "Sí" if incluye_flete else "No", total_flete, 
          "Sí" if lleva_molduras else "No", cantidad_molduras, subtotal_molduras, "Sí" if molduras_sin_cargo else "No", descuento_general, 
          total_neto, monto_sena, plazo_entrega, id_presupuesto))
    conexion.commit()
    conexion.close()

crear_tablas_y_configuracion()



