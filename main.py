import importlib

# Importación dinámica para evitar errores del analizador cuando Streamlit
# está instalado en un entorno virtual distinto al seleccionado por el IDE.
st = importlib.import_module("streamlit")

import streamlit as st
import os
import re
import urllib.parse
import base_datos
import pdf_manager

# --- Configuración estética de la página web de KROMA3D ---
st.set_page_config(page_title="KROMA3D - Cotizador Móvil", page_icon="📋", layout="centered")

# Cabecera corporativa automática con tu logotipo subido
if os.path.exists("logo.png"):
    st.image("logo.png", width=220)
else:
    st.title("📋 KROMA3D Revestimientos")

st.subheader("Módulo Comercial para Celulares")

# Estructura de solapas nativas de internet (se tocan directo con el dedo)
pestana_carga, pestana_historial = st.tabs(["📋 Nueva Cotización", "📊 Historial de Ventas"])

# =========================================================================
# SOLAPA 1: PANEL DE CARGA TÁCTIL (Se despliega en pestana_carga)
# =========================================================================
with pestana_carga:
    st.markdown("### 👤 Ficha del Cliente")
    cliente = st.text_input("Nombre y Apellido del Cliente:").upper()
    
    col1, col2 = st.columns(2)
    with col1:
        dni = st.text_input("DNI / CUIT:")
    with col2:
        telefono = st.text_input("Teléfono Celular:")
        
    email = st.text_input("Correo Electrónico:").lower()
    domicilio = st.text_input("Domicilio Particular:").upper()
    dom_obra = st.text_input("Domicilio de la Instalación / Obra:").upper()
    
    # 🌟 REPARADO: Buscador satelital blindado para navegadores móviles
    if dom_obra:
        texto_buscar = f"{dom_obra}, Mendoza, Argentina"
        enlace_maps = f"https://google.com{urllib.parse.quote(texto_buscar)}"
        st.markdown(f"🔗 [📍 CLIC ACÁ PARA VER EN GOOGLE MAPS]({enlace_maps})")

    observaciones = st.text_area("Observaciones o Guía de Obra:").upper()
    st.markdown("---")
    st.markdown("### 📐 Especificaciones de la Placa")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        modelo = st.text_input("Modelo Placa:").upper()
    with col4:
        ancho = st.number_input("Ancho (cm):", min_value=0, value=50)
    with col5:
        alto = st.number_input("Alto (cm):", min_value=0, value=50)
        
    destino = st.selectbox("Línea Destino:", ["Interior", "Exterior"])
    metros = st.number_input("Superficie a Cubrir (m²):", min_value=0.0, value=0.0, step=0.5)
    
    pintura = st.checkbox("Lleva Tratamiento / Pintura Fábrica")
    inmediata = st.checkbox("Entrega INMEDIATA (Stock de Fábrica)")
    descuento = st.number_input("Descuento General Comercial (%):", min_value=0, max_value=100, value=0)

    st.markdown("---")
    st.markdown("### 🛠️ Servicios Adicionales")
    
    colocacion = st.checkbox("Incluye Servicio de Colocación")
    mo_m2 = 0.0
    ins_m2 = 0.0
    if colocacion:
        c1, c2 = st.columns(2)
        with c1: mo_m2 = st.number_input("Mano Obra por m² ($):", value=4500)
        with c2: ins_m2 = st.number_input("Insumos Agarre por m² ($):", value=1500)

    flete = st.checkbox("Incluye Flete / Distribución")
    flete_monto = 0.0
    if flete:
        flete_gratis = st.checkbox("Envío SIN CARGO Logístico (Promoción)")
        if not flete_gratis:
            flete_monto = st.number_input("Costo del Flete ($):", value=12000)

    molduras = st.checkbox("Lleva Molduras de Terminación")
    metros_lineales = 0.0
    molduras_gratis = "No"
    if molduras:
        metros_lineales = st.number_input("Metros Lineales Requeridos:", value=0.0)
        if st.checkbox("Molduras BASE GRATIS (Promoción -100%)"):
            molduras_gratis = "Sí"

    st.markdown("---")
    
    # 🌟 REPARADO: Generación de PDF en memoria y botón de descarga táctil instantáneo
    if st.button("🚀 GENERAR Y GUARDAR COTIZACIÓN", use_container_width=True):
        if not cliente or not dni or not metros or not modelo:
            st.error("❌ Faltan datos esenciales: Completa el nombre, DNI, modelo y m².")
        else:
            try:
                dni_limpio = re.sub(r'\D', '', dni)
                tel_limpio = re.sub(r'\D', '', telefono)
                
                # Guarda el registro en SQLite
                base_datos.calcular_e_insertar(
                    cliente, dni_limpio, tel_limpio, email, domicilio, dom_obra, observaciones, metros, modelo, float(ancho), float(alto), destino, pintura, 
                    colocacion, float(mo_m2), float(ins_m2), flete, float(flete_monto), 
                    molduras, float(metros_lineales), molduras_gratis, float(descuento), inmediata
                )
                
                # Fuerza a ReportLab a dibujar el archivo en la nube
                p_completo = base_datos.buscar_presupuesto_completo(cliente)
                if p_completo:
                    ruta_pdf = pdf_manager.generar_pdf_presupuesto(p_completo)
                    st.success("✅ ¡Presupuesto guardado con éxito!")
                    
                    # Le ofrece el PDF directo en la pantalla del celular para descargar o enviar por WhatsApp
                    if os.path.exists(ruta_pdf):
                        with open(ruta_pdf, "rb") as file:
                            st.download_button(
                                label="📥 DESCARGAR ORDEN EN PDF (HACÉ CLIC ACÁ)",
                                data=file,
                                file_name=os.path.basename(ruta_pdf),
                                mime="application/pdf",
                                use_container_width=True
                            )
            except Exception as e:
                st.error(f"Ocurrió un detalle: {str(e)}")

# =========================================================================
# SOLAPA 2: HISTORIAL GENERAL DE VENTAS PARA CELULARES
# =========================================================================
with pestana_historial:
    st.markdown("### 📊 Cuaderno de Ventas")
    criterio_busqueda = st.text_input("🔍 Buscar por Nombre o CUIT del Cliente:").upper()
    
    registros = base_datos.obtener_presupuestos()
    if registros:
        registros_ordenados = sorted(registros, key=lambda x: x[0], reverse=True)
        
        for r in registros_ordenados:
            id_p, cl_nom, m2, mod, total, sena, plazo, fecha = r
            if criterio_busqueda and criterio_busqueda not in cl_nom:
                continue
                
            with st.expander(f"📦 OP N° {id_p} - {cl_nom} ({fecha})"):
                st.markdown(f"**Material:** {m2} m² del modelo **{mod}**")
                st.markdown(f"**Total Neto:** $ {total:,.2f} | **Seña 50%:** $ {sena:,.2f}")
                st.markdown(f"**Plazo Otorgado:** {plazo}")
                
                # Botón de descarga histórico para PDFs viejos guardados en el servidor
                fecha_l = fecha.replace("/", "-")
                nom_l = cl_nom.replace(" ", "_")
                ruta_p = f"presupuestos_emitidos/Presupuesto_{nom_l}_Nro_{id_p}_{fecha_l}.pdf"
                
                if os.path.exists(ruta_p):
                    with open(ruta_p, "rb") as f_hist:
                        st.download_button(label="📥 Descargar PDF", data=f_hist, file_name=os.path.basename(ruta_p), mime="application/pdf", key=f"dl_{id_p}")
                else:
                    st.caption("⚠️ Archivo físico no generado en la nube. Dale click a Generar arriba.")
