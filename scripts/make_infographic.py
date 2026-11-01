"""
Infographic generator for the Andes Retail Group Power BI project.
Follows Max's standing infographic template:
Título + subtítulo -> descripción -> Pregunta de negocio -> Metodología
(pasos + script/código representativo) -> Hallazgo principal (C->F->I) -> Visualización.
Built with PIL as a single JPG.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1700, 2500
MARGIN = 70
CONTENT_W = W - 2 * MARGIN

# Palette (matched to the existing portfolio infographic style)
NAVY = (26, 42, 58)
TEAL = (20, 60, 70)
ORANGE = (214, 86, 43)
LIGHT_BLUE = (223, 237, 245)
CREAM = (247, 245, 238)
LIGHT_GREEN = (224, 240, 224)
GREEN_TEXT = (40, 110, 70)
BLUE_TEXT = (35, 90, 130)
DARK_TEXT = (35, 38, 42)
GRAY_TEXT = (90, 95, 100)
CODE_BG = (26, 32, 44)
CODE_TEXT = (210, 220, 230)
WHITE = (255, 255, 255)
LINE = (225, 225, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

f_title = F("DejaVuSans-Bold.ttf", 54)
f_subtitle = F("DejaVuSans.ttf", 28)
f_h2 = F("DejaVuSans-Bold.ttf", 30)
f_h3 = F("DejaVuSans-Bold.ttf", 22)
f_body = F("DejaVuSans.ttf", 21)
f_body_b = F("DejaVuSans-Bold.ttf", 21)
f_small = F("DejaVuSans.ttf", 18)
f_small_b = F("DejaVuSans-Bold.ttf", 18)
f_code = F("DejaVuSansMono.ttf", 17)
f_caption = F("DejaVuSans-Oblique.ttf", 17)
f_footer = F("DejaVuSans.ttf", 16)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

y = 0

def wrap_draw(text, font, fill, x, y, max_width, line_spacing=1.35, align="left"):
    avg_char_w = font.getlength("x") or 10
    wrap_chars = max(10, int(max_width / avg_char_w * 1.0))
    lines = []
    for para in text.split("\n"):
        if para.strip() == "":
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=wrap_chars))
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        bbox = font.getbbox("Ag")
        line_h = (bbox[3] - bbox[1]) * line_spacing
        y += line_h
    return y

def section_header(label, y, color=ORANGE):
    d.rectangle([MARGIN, y, MARGIN + 8, y + 36], fill=color)
    d.text((MARGIN + 22, y - 2), label, font=f_h2, fill=NAVY)
    return y + 54

# ---------- Header ----------
d.rectangle([0, 0, W, 190], fill=NAVY)
d.text((MARGIN, 38), "Andes Retail Group", font=f_title, fill=WHITE)
d.text((MARGIN, 108), "Desempeño Comercial 2024–2025 · Dashboard en Power BI", font=f_subtitle, fill=(200, 215, 225))
d.rectangle([MARGIN, 160, MARGIN + 420, 166], fill=ORANGE)
d.text((MARGIN, 172), "Chile · Colombia · Perú  —  Power Query · DAX · Modelado de datos", font=f_small, fill=(170, 190, 205))

y = 220

# ---------- Description ----------
desc = ("Dashboard interactivo en Power BI que analiza 5,000 pedidos de Andes Retail Group entre 2024 y 2025 "
        "en tres mercados (Chile, Colombia, Perú) y cuatro categorías de producto. El modelo se construyó con "
        "transformaciones documentadas en Power Query y medidas DAX diseñadas para permitir comparaciones año "
        "contra año aun cuando el usuario filtra por un año específico. Dos vistas — Overview y Detalle — llevan "
        "al lector de «qué pasó» a «por qué pasó».")
y = wrap_draw(desc, f_body, DARK_TEXT, MARGIN, y, CONTENT_W)
y += 26

# ---------- Pregunta de negocio ----------
y = section_header("Pregunta de negocio", y)
questions = [
    "¿Cómo evolucionó el ingreso total entre 2024 y 2025, y qué tan generalizada es la caída?",
    "¿Qué segmentos de cliente y categorías de producto explican ese resultado?",
    "Si el volumen de pedidos casi no bajó, ¿de dónde viene la caída de ingreso — y dónde está la oportunidad de revertirla?",
]
for q in questions:
    d.ellipse([MARGIN, y + 6, MARGIN + 10, y + 16], fill=ORANGE)
    y = wrap_draw(q, f_body, DARK_TEXT, MARGIN + 26, y, CONTENT_W - 26)
    y += 8
y += 16

# ---------- Metodología ----------
y = section_header("Metodología", y)
steps = [
    ("Power Query", "tipos de datos validados, columna condicional Nivel_Venta (Venta Alta ≥ $1,000), columnas calculadas Beneficio y Margen_Rentabilidad."),
    ("Modelo DAX", "medidas fijas respecto al segmentador de Año (REMOVEFILTERS) para comparar 2024 vs 2025 bajo cualquier filtro, y una medida interactiva (Ticket promedio) que sí respeta todos los filtros."),
    ("Validación de calidad", "Vista de Perfil de Columna y Detalles de calidad en Power Query — 100% de datos válidos en las 12 columnas, 5,000 pedidos sin nulos ni duplicados."),
    ("Diseño iterativo", "KPIs y gráficos ajustados tras construir y revisar cada vista; decisiones descartadas documentadas por transparencia (ver README)."),
]
for label, text in steps:
    d.rectangle([MARGIN, y + 4, MARGIN + 10, y + 24], fill=TEAL)
    d.text((MARGIN + 24, y), label + ":", font=f_body_b, fill=TEAL)
    label_w = f_body_b.getlength(label + ": ")
    y2 = wrap_draw(text, f_body, DARK_TEXT, MARGIN + 24, y + 30, CONTENT_W - 24)
    y = y2 + 10

y += 10
d.text((MARGIN, y), "Medida DAX representativa (no es el modelo completo — ver el .pbix):", font=f_caption, fill=GRAY_TEXT)
y += 30

code_lines = [
    "Ingreso 2025 =",
    "CALCULATE(",
    "    SUM('Andes_Retail_Group_2024_2025'[Ingresos]),",
    "    REMOVEFILTERS('Andes_Retail_Group_2024_2025'[Fecha_Pedido]),",
    "    YEAR('Andes_Retail_Group_2024_2025'[Fecha_Pedido]) = 2025",
    ")",
    "",
    "Ticket promedio (texto) =",
    '"$" & FORMAT(AVERAGE(\'Andes_Retail_Group_2024_2025\'[Ingresos]), "#,##0.00")',
    "",
    "Variación Premium YoY =",
    "DIVIDE([Ingreso Premium 2025] - [Ingreso Premium 2024], [Ingreso Premium 2024])",
]
code_h = 26 * len(code_lines) + 36
d.rounded_rectangle([MARGIN, y, MARGIN + CONTENT_W, y + code_h], radius=10, fill=CODE_BG)
cy = y + 18
for line in code_lines:
    d.text((MARGIN + 24, cy), line, font=f_code, fill=CODE_TEXT)
    cy += 26
y += code_h + 30

# ---------- Hallazgo principal C -> F -> I ----------
y = section_header("Hallazgo principal  (Contexto → Hallazgo → Implicación)", y)

panel_h = 330
panel_w = (CONTENT_W - 40) // 3
panels = [
    ("Contexto", LIGHT_BLUE, BLUE_TEXT,
     "Andes Retail Group cerró 2024 con $2.86 millones en ingresos, operando en Chile, Colombia y Perú "
     "a través de cuatro categorías de producto (Deportes, Electrónica, Hogar, Ropa). Dataset completo: "
     "5,000 pedidos, 0% de valores nulos o duplicados."),
    ("Hallazgo", CREAM, NAVY,
     "En 2025 el ingreso retrocedió a $2.67M (−6.8% YoY). Los pedidos casi no bajaron (−3.92%) y el "
     "margen se mantuvo estable (−0.16%), pero el ticket promedio cayó −10.93% ($1,222.90 → $1,089.23), "
     "concentrado en el cliente Premium (−14.04%) y en Ventas Altas (−9.06%). Perú, el mercado líder, tuvo "
     "la caída más fuerte (−10%). Hogar fue la única categoría que no cayó, y ascendió al 1er lugar en beneficio."),
    ("Implicación", LIGHT_GREEN, GREEN_TEXT,
     "La prioridad comercial es recuperar valor por transacción en el cliente Premium y de Alto Valor "
     "(fidelización, upselling) — no es un problema de volumen, costos ni eficiencia. Replicar lo que explica "
     "el crecimiento de Hogar, y anticipar promociones fuera de la temporada navideña (nov–ene) para "
     "suavizar la caída de los meses centrales."),
]
x = MARGIN
for title, bg, text_color, body in panels:
    d.rounded_rectangle([x, y, x + panel_w, y + panel_h], radius=10, fill=bg)
    d.text((x + 20, y + 18), title, font=f_h3, fill=text_color)
    d.line([x + 20, y + 52, x + panel_w - 20, y + 52], fill=text_color, width=2)
    wrap_draw(body, f_small, DARK_TEXT, x + 20, y + 66, panel_w - 40, line_spacing=1.4)
    x += panel_w + 20
y += panel_h + 40

# ---------- Visualización ----------
y = section_header("Visualización", y)
d.text((MARGIN, y), "Dashboard completo — dos vistas interactivas (segmentadores de Año, País, Categoría, Segmento y Nivel de venta):", font=f_caption, fill=GRAY_TEXT)
y += 34

chart_w = (CONTENT_W - 30) // 2
chart_h = int(chart_w * (1654 / 2339))

ov = Image.open("assets/dashboard_overview.png").resize((chart_w, chart_h))
dt = Image.open("assets/dashboard_detalle.png").resize((chart_w, chart_h))

y = int(y)
img.paste(ov, (MARGIN, y))
img.paste(dt, (MARGIN + chart_w + 30, y))
d.rectangle([MARGIN, y, MARGIN + chart_w, y + chart_h], outline=LINE, width=2)
d.rectangle([MARGIN + chart_w + 30, y, MARGIN + chart_w + 30 + chart_w, y + chart_h], outline=LINE, width=2)

y += chart_h + 14
d.text((MARGIN, y), "Vista Overview — tendencia, categorías, países", font=f_caption, fill=GRAY_TEXT)
d.text((MARGIN + chart_w + 30, y), "Vista Detalle — segmentos, estacionalidad, síntesis", font=f_caption, fill=GRAY_TEXT)
y += 50

# ---------- Footer ----------
footer_h = 90
d.rectangle([0, y, W, y + footer_h], fill=NAVY)
d.text((MARGIN, y + 34), "Max Santana — Data Analyst, Business Intelligence & Strategic Foresight", font=f_footer, fill=(200, 215, 225))
d.text((W - MARGIN - f_footer.getlength("github.com/maxsantana-data2strategy"), y + 34),
       "github.com/maxsantana-data2strategy", font=f_footer, fill=(200, 215, 225))
y += footer_h

final = img.crop((0, 0, W, y))
final.save("assets/Infographic_AndesRetail_ES.jpg", quality=92)
print("saved", final.size)
