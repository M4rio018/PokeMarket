import streamlit as st
import pandas as pd
import uuid

# Configuración de la página
st.set_page_config(page_title="PokeTrade - E-Commerce", page_icon="🃏", layout="wide")

# Inicializar nuestra "base de datos" simulada en la sesión
if 'archivo_cartas' not in st.session_state:
    st.session_state['archivo_cartas'] = []

st.title("🃏 PokeTrade Marketplace")
st.subheader("Compra, venta e intercambio de cartas Pokémon")

# --- VISTA LATERAL: REGISTRO DE NUEVA CARTA ---
st.sidebar.header("📝 Publicar Nueva Carta")

with st.sidebar.form(key="form_registro"):
    # Campos basados en nuestro diseño de registro
    nombre = st.text_input("Nombre del Pokémon / Carta (AN50)")
    id_carta_api = st.text_input("ID Oficial API (ej: swsh4-044) (AN15)")
    expansion = st.text_input("Expansión / Set (AN40)")
    numero_coleccion = st.text_input("Número de Colección (ej: 188/195) (AN10)")
    
    rareza = st.selectbox("Rareza (AN25)", ["Common", "Uncommon", "Rare", "Ultra Rare", "Secret Rare", "Promo"])
    tipo_pokemon = st.selectbox("Tipo (AN15)", ["Planta", "Fuego", "Agua", "Rayo", "Psíquico", "Lucha", "Oscuro", "Metal", "Dragón", "Incoloro", "Entrenador", "Energía"])
    estado_carta = st.selectbox("Estado de la Carta (AN15)", ["Mint (Perfecta)", "Near Mint", "Played", "Heavily Played"])
    modalidad = st.radio("Modalidad (AN15)", ["Venta", "Intercambio", "Ambas"])
    
    precio = st.number_input("Precio ($) (N10,2)", min_value=0.0, step=0.5, value=0.0)
    detalles_adicionales = st.text_area("Detalles Adicionales (AN200)", max_chars=200)
    id_usuario_dueno = st.text_input("Tu ID de Usuario (AN20)", value="Trainer_Ash")
    
    botón_guardar = st.form_submit_form_button("Publicar Carta")

# Lógica para guardar el registro (simulando escritura en archivo)
if botón_guardar:
    if nombre and expansion:
        # Creamos el registro con su Clave Principal única (id_publicacion)
        reg_carta = {
            "id_publicacion": str(uuid.uuid4())[:8], # Genera un ID corto único
            "id_carta_api": id_carta_api,
            "nombre": nombre,
            "expansion": expansion,
            "numero_coleccion": numero_coleccion,
            "rareza": rareza,
            "tipo_pokemon": tipo_pokemon,
            "id_usuario_dueno": id_usuario_dueno,
            "estado_carta": estado_carta,
            "modalidad": modalidad,
            "precio": precio if modalidad != "Intercambio" else 0.0,
            "detalles_adicionales": detalles_adicionales
        }
        # Guardamos en nuestro "archivo"
        st.session_state['archivo_cartas'].append(reg_carta)
        st.sidebar.success(f"¡Carta '{nombre}' publicada con éxito! ID: {reg_carta['id_publicacion']}")
    else:
        st.sidebar.error("Por favor, completa al menos el nombre y la expansión.")

# --- VISTA PRINCIPAL: MARKETPLACE ---
st.write("---")
st.header("🗂️ Cartas Disponibles en el Mercado")

if len(st.session_state['archivo_cartas']) == 0:
    st.info("Aún no hay cartas publicadas. ¡Usa el panel de la izquierda para agregar la primera!")
else:
    # Convertimos el archivo de registros en un DataFrame para mostrarlo como tabla limpia
    df_cartas = pd.DataFrame(st.session_state['archivo_cartas'])
    
    # Reordenar columnas para que la clave principal esté al inicio
    columnas = ['id_publicacion', 'nombre', 'expansion', 'numero_coleccion', 'rareza', 'tipo_pokemon', 'estado_carta', 'modalidad', 'precio', 'id_usuario_dueno']
    st.dataframe(df_cartas[columnas], use_container_width=True)

    # Simulación del Match de Intercambio
    st.write("---")
    st.header("🤝 Zona de Match Automatizado (Simulación)")
    st.caption("El sistema cruza datos de lo que tienes y lo que buscas.")
    if st.button("Simular Match de Intercambio"):
        st.balloons()
        st.success("¡MATCH ENCONTRADO! El usuario 'Trainer_Mystic' quiere tu carta y tiene el Charizard que buscas. ¡Se ha abierto un chat!")
