from io import BytesIO
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

st.set_page_config(page_title="Generador de Ofertas y Diseños", page_icon="🛒")

st.title("🛒 Generador de Ofertas para WhatsApp y Redes Sociales")
st.write(
    "Sube la foto de tu producto, ingresa los precios y genera la imagen publicitaria junto con tu texto."
)

# --- SECCIÓN 1: DATOS DEL PRODUCTO Y DISEÑO DE IMAGEN ---
st.header("1. Personaliza tu Imagen y Producto")

col1, col2 = st.columns(2)
with col1:
  producto = st.text_input(
      "Nombre del Producto", placeholder="Ej. Kit de Serums Facial"
  )
  precio_oferta = st.text_input(
      "Precio con Descuento (Ej. 1125)", placeholder="1125"
  )
  porcentaje_desc = st.text_input(
      "Porcentaje de Descuento (Ej. 25%)", value="25% OFF"
  )
with col2:
  precio_original = st.text_input(
      "Precio Original Tachado (Ej. 1500)", placeholder="1500"
  )
  link_ml = st.text_input(
      "Link de MercadoLibre",
      placeholder="https://articulo.mercadolibre.com.mx/...",
  )

  lista_categorias = [
      "General / Cualquiera",
      "Vehículos y Accesorios",
      "Supermercado y Alimentos",
      "Tecnología y Electrónica",
      "Videojuegos y Consolas",
      "Electrodomésticos",
      "Hogar y Muebles",
      "Moda",
      "Joyería y Relojes",
      "Deportes y Fitness",
      "Herramientas y Construcción",
      "Mascotas",
      "Bebés y Juguetes",
      "Salud y Belleza",
      "Libros y Música",
      "Instrumentos Musicales",
      "Papelería y Arte",
  ]
  categoria = st.selectbox("Categoría del producto:", lista_categorias)

# Subir la imagen del producto
imagen_subida = st.file_uploader(
    "Sube la foto de tu producto (PNG o JPG)", type=["png", "jpg", "jpeg"]
)

# --- LÓGICA DE CREACIÓN DE LA IMAGEN CON PIL ---
if imagen_subida and precio_oferta and precio_original:
  st.subheader(" Vista previa de tu imagen generada:")

  try:
    # Cargamos una plantilla base (puedes reemplazar esta ruta por tu diseño base predeterminado)
    # Nota: Si no tienes una plantilla creada, crearemos un lienzo base de 1080x1920 simulado.
    ancho, alto = 1080, 1920
    base = Image.new("RGBA", (ancho, alto), (74, 158, 219, 255))  # Fondo azul

    # Abrir la imagen del producto que subió el usuario
    img_producto = Image.open(imagen_subida).convert("RGBA")
    # Redimensionar la imagen del producto para adaptarla al diseño
    img_producto = img_producto.resize((650, 650))

    # Pegar la imagen del producto en el centro-superior del lienzo
    pos_x = (ancho - 650) // 2
    pos_y = 450
    base.paste(img_producto, (pos_x, pos_y), img_producto)

    # Dibujar textos dinámicos (Precios y Descuento) usando Pillow
    draw = ImageDraw.Draw(base)

    try:
      # Intentamos cargar una fuente llamativa del sistema o predeterminada
      font_grande = ImageFont.truetype(
          "arial.ttf", 90
      )  # Asegúrate de tener fuentes compatibles o usar default
      font_tachado = ImageFont.truetype("arial.ttf", 60)
    except:
      font_grande = ImageFont.load_default()
      font_tachado = ImageFont.load_default()

    # Dibuja Precio Original Tachado
    texto_orig = f"${precio_original}"
    draw.text(
        (420, 1400),
        texto_orig,
        fill=(220, 220, 220),
        font=font_tachado,
        stroke_width=2,
    )
    # Línea de tachado manual sobre el precio original
    draw.line([(400, 1435), (680, 1435)], fill=(230, 50, 50), width=8)

    # Dibuja Precio con Descuento (Verde brillante)
    texto_desc = f"${precio_oferta} MXN"
    draw.text((250, 1520), texto_desc, fill=(50, 255, 50), font=font_grande)

    # Convertir imagen para mostrar en Streamlit y permitir descarga
    buffered = BytesIO()
    base.save(buffered, format="PNG")
    st.image(
        buffered.getvalue(),
        caption="Imagen lista para descargar",
        use_container_width=True,
    )

    # Botón de descarga de la imagen
    st.download_button(
        label="📥 Descargar Imagen Publicitaria",
        data=buffered.getvalue(),
        file_name="oferta_producto.png",
        mime="image/png",
    )

  except Exception as e:
    st.error(f"Hubo un error al procesar la imagen: {e}")

else:
  st.info(
      "Sube una foto del producto y llena los precios para generar la imagen"
      " automáticamente."
  )

st.divider()

# --- SECCIÓN 2: PLANTILLA Y EDICIÓN DE TEXTO PARA WHATSAPP ---
st.header("2. Personaliza tu mensaje para WhatsApp")

estilo = st.selectbox(
    "Elige el estilo del mensaje:", ["Llamativo", "Corto y directo", "Urgencia"]
>

if producto and precio_oferta and link_ml:
  # Lógica de textos y emojis por categoría
  if categoria == "Salud y Belleza":
    emoji_cat = "✨💄"
    frase_cat = f"Consiéntete como te mereces. Este {producto} es justo lo que necesitas."
    frase_urgencia = (
        "¡Cuida de ti al mejor precio antes de que se agote el 25% de descuento!"
    )
  else:
    emoji_cat = "🎁🛍️"
    frase_cat = f"¡Checa este productazo! El {producto} que estabas buscando."
    frase_urgencia = "¡Corre porque vuelan las piezas!"

  # Plantillas de texto
  if estilo == "Llamativo":
    mensaje_default = f"🔥 ¡GRAN OFERTA DE NO CREER ({porcentaje_desc})! 🔥\n\n{emoji_cat} {frase_cat}\n\n💰 Precio anterior: ${precio_original}\n💰 Precio especial: solo $ {precio_oferta}. 😱\n\n👉 Cómpralo de forma segura en MercadoLibre aquí: \n{link_ml} \n\n#Ofertas #MercadoLibre #Imperdible"
  elif estilo == "Corto y directo":
    mensaje_default = f"✅ {emoji_cat} {producto} con {porcentaje_desc} de descuento por solo ${precio_oferta}.\n\n🛒 Cómpralo aquí directo en MercadoLibre: {link_ml}"
  else:
    mensaje_default = f"🚨 ¡ÚLTIMAS PIEZAS CON {porcentaje_desc}! 🚨\n\n{producto} súper rebajado a solo ${precio_oferta}. 😱\n\n⚠️ {frase_urgencia}\n\n🛒 Haz tu pedido AQUÍ antes de que se acabe: {link_ml}"

  mensaje_final = st.text_area(
      "Edita el texto final si deseas agregar o quitar algo:",
      value=mensaje_default,
      height=200,
  )

  mensaje_codificado = urllib.parse.quote(mensaje_final)
  url_whatsapp = f"https://wa.me/?text={mensaje_codificado}"

  st.link_button("Enviar por WhatsApp", url_whatsapp, type="primary")

else:
  st.info(
      "Por favor, completa los datos del producto arriba para generar los"
      " textos de WhatsApp."
  )
