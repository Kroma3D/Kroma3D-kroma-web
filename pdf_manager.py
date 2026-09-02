import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf_presupuesto(p):
    """Construye el presupuesto imprimible membretado en base al paquete de datos de SQLite."""
    id_presupuesto = p[0]
    cliente_nombre = p[1]
    dni_val = p[2]
    tel_val = p[3]
    email_val = p[4]
    dom_particular = p[5]
    dom_obra = p[6]
    observaciones_val = p[7]
    metros_cuadrados = p[8]
    modelo_nombre = p[9]
    ancho_val = p[10]
    alto_val = p[11]
    destino_val = p[12]
    pintura_estado = p[13]
    placas_cant = p[14]
    placas_precio_vta = p[15]
    colocac_estado = p[16]
    colocac_total = p[17]
    flete_estado = p[18]
    flete_total = p[19]
    molduras_estado = p[20]
    molduras_cant = p[21]
    molduras_total = p[22]
    molduras_bonif = p[23]
    desc_gral_porc = p[24]
    total_neto = p[25]
    sena_monto = p[26]
    plazo_entrega_texto = p[27]
    emision_fecha = p[28]
    validez_fecha = p[29]

    os.makedirs("presupuestos_emitidos", exist_ok=True)
    fecha_limpia = emision_fecha.replace("/", "-")
    nombre_limpio_cliente = cliente_nombre.replace(" ", "_")
    base_nombre = f"Presupuesto_{nombre_limpio_cliente}_Nro_{id_presupuesto}_{fecha_limpia}"
    nombre_archivo = os.path.join("presupuestos_emitidos", f"{base_nombre}.pdf")
    
    if os.path.exists(nombre_archivo):
        nombre_archivo = os.path.join("presupuestos_emitidos", f"{base_nombre}_MODIFICADO.pdf")
    
    documento = SimpleDocTemplate(nombre_archivo, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elementos = []
    
    estilos = getSampleStyleSheet()
    estilo_titulo_empresa = ParagraphStyle('EmpresaStyle', fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor("#1A365D"))
    estilo_subtitulos = ParagraphStyle('SubStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#2B6CB0"), spaceAfter=6)
    estilo_cuerpo = ParagraphStyle('CuerpoStyle', fontName='Helvetica', fontSize=10, leading=14)
    estilo_legales = ParagraphStyle('LegalStyle', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#2D3748"))
    
    datos_encabezado = []
    if os.path.exists("logo.png"):
        img_logo = Image("logo.png", width=140, height=50)
        datos_encabezado.append(img_logo)
    else:
        datos_encabezado.append(Paragraph("<b>KROMA3D</b><br/>REVESTIMIENTOS", estilo_titulo_empresa))
    
    tipo_op = "PI" if destino_val == "Interior" else "PE"
    info_contacto_texto = f"<b>KROMA3D REVESTIMIENTOS</b> | OP N° {tipo_op} 000-{id_presupuesto}<br/>Mendoza, Argentina<br/>Email: kroma3d.info@gmail.com | WhatsApp: 261 33 44 222<br/><b>Fecha de emisión:</b> {emision_fecha}<br/><b>Válido hasta el:</b> {validez_fecha}"
    datos_encabezado.append(Paragraph(info_contacto_texto, estilo_cuerpo))
    
    tabla_encabezado = Table([datos_encabezado], colWidths=[200, 350])
    tabla_encabezado.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, 15))
    
    elementos.append(Paragraph("<b>FICHA DEL CLIENTE Y PROYECTO</b>", estilo_subtitulos))
    datos_cliente_bloque = f"""<b>CLIENTE:</b> {cliente_nombre} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>DNI/CUIT:</b> {dni_val} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>TELÉFONO:</b> {tel_val}<br/>
    <b>EMAIL:</b> {email_val}<br/>
    <b>DOMICILIO PARTICULAR:</b> {dom_particular}<br/>
    <b>DOMICILIO DE INSTALACIÓN / OBRA:</b> {dom_obra}<br/>
    <b>OBSERVACIONES / GUÍA DE OBRA:</b> {observaciones_val if observaciones_val else 'SIN OBSERVACIONES ADICIONALES'}<br/>
    <b>SUPERFICIE A CUBRIR:</b> {metros_cuadrados} m²<br/>
    <b>PLAZO DE ENTREGA ESTIMADO:</b> {plazo_entrega_texto}"""
    elementos.append(Paragraph(datos_cliente_bloque, estilo_cuerpo))
    elementos.append(Spacer(1, 15))
    elementos.append(Paragraph("<b>1. ESPECIFICACIONES TÉCNICAS DEL MATERIAL</b>", estilo_subtitulos))
    
    # 🌟 REPARADO: Corrección de texto comercial automático según el destino real de la placa
    if destino_val == "Exterior":
        linea_comercial_texto = "Exterior Decorativa de Alta Resistencia Climática"
    else:
        linea_comercial_texto = "Interior Antihumedad"
        
    acabado_texto = "PINTADA (TRATAMIENTO CON SELLADOR Y PINTURA)" if pintura_estado == "Sí" else "CRUDA (AL NATURAL SECADA EN FÁBRICA)"
    detalle_modelo = f"<b>Línea:</b> {linea_comercial_texto} | <b>Modelo seleccionado:</b> {modelo_nombre} ({int(ancho_val)}x{int(alto_val)} cm) | <b>Normativa de Fabricación:</b> Bajo lineamientos de Norma IRAM 11643 | <b>Acabado de fábrica:</b> {acabado_texto}"
    elementos.append(Paragraph(detalle_modelo, estilo_cuerpo))
    elementos.append(Spacer(1, 15))

    elementos.append(Paragraph("<b>2. DESGLOSE DE COSTOS Y COMPONENTES ADICIONALES</b>", estilo_subtitulos))
    filas_costos = [["Componente", "Detalle Comercial", "Monto Subtotal"]]
    filas_costos.append(["Placas Fabricadas", f"{placas_cant} unidades de {modelo_nombre} (Unit: ${placas_precio_vta:.2f})", f"$ {placas_cant*placas_precio_vta:.2f}"])
    filas_costos.append(["Servicio de Colocación", "Mano de obra + Insumos de agarre" if colocac_estado=="Sí" else "No solicitado", f"$ {colocac_total:.2f}"])
    
    if flete_estado == "Sí":
        filas_costos.append(["Flete / Distribución", "Entrega logistica coordinada" if flete_total > 0 else "Envío SIN CARGO", f"$ {flete_total:.2f}"])
    else:
        filas_costos.append(["Flete / Distribución", "Retira por fábrica", "$ 0.00"])
    
    if molduras_estado == "Sí":
        filas_costos.append(["Molduras Terminación", f"{molduras_cant} unidades" if molduras_bonif == "No" else "Bonificación Promocional -100%", f"$ {molduras_total:.2f}"])
    else:
        filas_costos.append(["Molduras Terminación", "No solicitadas", "$ 0.00"])
        
    tabla_costos = Table(filas_costos, colWidths=[140, 300, 100])
    tabla_costos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    elementos.append(tabla_costos)
    elementos.append(Spacer(1, 15))
    
    elementos.append(Paragraph("<b>3. LIQUIDACIÓN COMERCIAL, BONIFICACIONES Y FINANCIAMIENTO</b>", estilo_subtitulos))
    filas_totales = []
    if desc_gral_porc > 0:
        filas_totales.append(["DESCUENTO GENERAL COMERCIAL APLICADO:", f"- {desc_gral_porc} %"])
    filas_totales.append(["SEÑOR CLIENTE, EL TOTAL NETO FINAL ES:", f"$ {total_neto:.2f}"])
    filas_totales.append(["ANTICIPO REQUERIDO DE SEÑA (50%):", f"$ {sena_monto:.2f}"])
    filas_totales.append(["SALDO RESTANTE CONTRA ENTREGA/OBRA:", f"$ {(total_neto-sena_monto):.2f}"])
    
    tabla_totales = Table(filas_totales, colWidths=[380, 160])
    tabla_totales.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,-1), (1,-1), colors.HexColor("#FEFCBF")), 
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elementos.append(tabla_totales)
    elementos.append(Spacer(1, 15))

    elementos.append(Paragraph("<b>4. CONDICIONES DE CONTRATACIÓN Y REGLAS DE FABRICACIÓN</b>", estilo_subtitulos))
    texto_advertencia_pintura = ""
    if pintura_estado == "No" and destino_val == "Interior":
        texto_advertencia_pintura = "<b>ADVERTENCIA DE ACABADO (IMPORTANTE):</b> Para conservar la propiedad antihumedad activa y la validez de la Garantía Escrita de 10 años, las placas crudas NO deben ser pintadas con látex común...<br/>"

    texto_legal_definitivo = f"<b>Forma de Pago:</b> 50% de anticipo obligatorio...<br/><b>Garantía de precios:</b> 15 días firmes (válido hasta el <b>{validez_fecha}</b>).<br/>{texto_advertencia_pintura}<b>Servicio de Instalación Autorizado:</b> Revestimiento vertical sobre paredes estructuralmente firmes. La causa raíz de la humedad debe estar reparada de forma previa.<br/><b>Plazos especiales por Contingencias:</b> Prórroga automática de hasta <b>7 días hábiles adicionales por factores climáticos adversos</b> (viento zonda, heladas o humedad extrema)."
    elementos.append(Paragraph(texto_legal_definitivo, estilo_legales))
    
    documento.build(elementos)
    return nombre_archivo
