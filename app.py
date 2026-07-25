from io import BytesIO
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

st.set_page_config(
    page_title="Ora del Click - Generador de Ofertas",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Generador Profesional de Ofertas y Diseños")
st.write(
    "Sube la foto de tu producto, personaliza el descuento y descarga el banner"
    " publicitario listo para redes sociales."
)

# --- SECCIÓN 1: DATOS Y DISEÑO DEL BANNER ---
st.header("1. Personaliza tu Banner de Oferta")

col1, col2 = st.columns(2)

with col1:
  producto = st.text_input(
      "Nombre del Producto", placeholder="Ej. Kit de Serums Facial"
  )
  precio_oferta = st.text_input(
      "Precio de Oferta (Ej. 1125)", placeholder="1125"
  )
  porcentaje_desc = st.text_input(
      "Texto del Descuento", value="25% OFF"
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

# Subir la imagen del producto en bruto
imagen_subida = st.file_uploader(
    "Sube la foto de tu producto en formato PNG (preferiblemente sin fondo) o JPG",
    type=["png", "jpg", "jpeg"],
)

st.divider()

# --- SECCIÓN 2: RENDERIZADO VISUAL DEL BANNER ---
if imagen_subida and precio_oferta and precio_original:
  st.subheader("🖼️ Vista Previa del Banner Generado")

  try:
    # 1. Crear el lienzo base (Simulando la plantilla vertical 1080x1920)
    ancho, alto = 1080, 1920
    # Color de fondo azul degradado simulado con un tono sólido elegante (#489be6)
    banner_base = Image.new("RGBA", (ancho, alto), (72, 155, 230, 255))
    draw = ImageDraw.Draw(banner_base)

    # 2. Cargar y ajustar la imagen del producto subido por el administrador
    img_prod = Image.open(imagen_subida).convert("RGBA")
    # Redimensionar la imagen para que encaje perfectamente en el centro del diseño
    img_prod = img_prod.resize((700, 700))

    # Coordenadas para centrar el producto en el área superior-media
    pos_x = (ancho - 700) // 2
    pos_y = 350
    banner_base.paste(img_prod, (pos_x, pos_y), img_prod)

    # 3. Dibujar textos y elementos gráficos (Precios y elementos de oferta)
    try:
      # Fuentes tipográficas (Asegúrate de tener una fuente estándar o usa la por defecto)
      font_precio_grande = ImageFont.truetype("arial.ttf", 110)
      font_tachado = ImageFont.truetype("arial.ttf", 70)
    except:
      font_precio_grande = ImageFont.load_default()
      font_tachado = ImageFont.load_default()

    # --- RENDERIZAR PRECIO ORIGINAL TACHADO ---
    texto_original_str = f"${precio_original}"
    # Medir ancho aproximado para centrarlo
    draw.text(
        (400, 1350),
        texto_original_str,
        fill=(230, 230, 230),
        font=font_tachado,
    )
    # Línea roja horizontal tachando el precio original
    draw.line([(380, 1395), (700, 1395)], fill=(235, 50, 50), width=10)

    # --- RENDERIZAR PRECIO CON DESCUENTO (Verde brillante inferior) ---
    texto_oferta_str = f"${precio_oferta} MXN"
    draw.text(
        (220, 1470),
        texto_oferta_str,
        fill=(60, 255, 60),
        font=font_precio_grande,
        stroke_width=3,
        stroke_fill=(0, 0, 0),
    )

    # 4. Guardar imagen en memoria para mostrarla y descargarla
    buffered = BytesIO()
    banner_base.save(buffered, format="PNG")

    # Mostrar la imagen resultante en la interfaz de Streamlit
    st.image(
        buffered.getvalue(),
        caption="Diseño listo con precios y producto integrados",
        use_container_width=True,
    )

    # Botón de descarga directa
    st.download_button(
        label="📥 Descargar Imagen Publicitaria Completa",
        data=buffered.getvalue(),
        file_name=f"oferta_{producto.replace(' ', '_')}.png",
        mime="image/png",
    )

  except Exception as e:
    st.error(f"Error al generar la imagen: {e}")

else:
  st.info(
      "👆 Sube una imagen de producto y llena los campos de precios arriba"
      " para generar el diseño automáticamente."
  )

st.divider()

# --- SECCIÓN 3: TEXTO Y WHATSAPP ---
st.header("3. Genera el Mensaje para WhatsApp")

estilo = st.selectbox(
    "Elige el estilo del mensaje:", ["Llamativo", "Corto y directo", "Urgencia"]
>

if producto and precio_oferta and link_ml:
  # Lógica de textos adaptados
  emoji_cat = "🎁🛍️"
  frase_cat = f"¡Aprovecha este ofertón! Llévate {producto} con un {porcentaje_desc} de descuento."

  if estilo == "Llamativo":
    mensaje_default = f"🔥 ¡GRAN OFERTA ({porcentaje_desc})! 🔥\n\n{emoji_cat} {frase_cat}\n\n💰 Precio anterior: ${precio_original}\n💰 Precio especial de remate: ${precio_oferta} 😱\n\n👉 Cómpralo de forma segura aquí: \n{link_ml} \n\n#Ofertas #Descuentos #Imperdible"
  elif estilo == "Corto y directo":
    mensaje_default = f"✅ {emoji_cat} {producto} con {porcentaje_desc} a solo ${precio_oferta}.\n\n🛒 Cómpralo aquí: {link_ml}"
  else:
    mensaje_default = f"🚨 ¡ÚLTIMAS PIEZAS CON {porcentaje_desc}! 🚨\n\n{producto} súper rebajado a solo ${precio_oferta}. 😱\n\n🛒 Haz tu pedido AQUÍ antes de que se acabe: {link_ml}"

  mensaje_final = st.text_area(
      "Edita tu mensaje para WhatsApp:",
      value=mensaje_default,
      height=180,
  )

  # Botón de WhatsApp
  wa_link = f"https://wa.me/?text={urllib.parse.quote(mensaje_final)}"
  st.link_button(
      "💬 Enviar Oferta por WhatsApp", wa_link, use_container_width=True
  )

else:
  st.warning("Completa los datos del producto para habilitar el mensaje.")
