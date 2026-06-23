from flask import Flask, render_template_string, request

app = Flask(__name__)

# 1. INVENTARIO DE LA TIENDA
inventario = {
    "pan": {"pasillo": 3, "estante": 2},
    "leche": {"pasillo": 1, "estante": 4},
    "arroz": {"pasillo": 2, "estante": 1},
    "fideos": {"pasillo": 2, "estante": 3},
    "jabon": {"pasillo": 4, "estante": 2},
    "gaseosa": {"pasillo": 1, "estante": 5},
    "azucar": {"pasillo": 2, "estante": 2},
    "cafe": {"pasillo": 2, "estante": 4},
    "aceite": {"pasillo": 2, "estante": 5},
    "huevos": {"pasillo": 1, "estante": 1},
    "papel higienico": {"pasillo": 4, "estante": 1},
    "galletas": {"pasillo": 3, "estante": 1},
    "atun": {"pasillo": 2, "estante": 6},
    "sal": {"pasillo": 2, "estante": 2},
    "shampoo": {"pasillo": 4, "estante": 3},
    "detergente": {"pasillo": 4, "estante": 4},
    "papas fritas": {"pasillo": 3, "estante": 3},
    "chocolate": {"pasillo": 3, "estante": 4}
}

# 2. INTERFAZ VISUAL MODIFICADA
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscador de Productos - Minimarket</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 30px auto;
            padding: 20px;
            text-align: center;
            background-color: #f4f4f9;
        }
        h1 { color: #333; margin-bottom: 5px; }
        h2 { color: #555; margin-top: 30px; font-size: 20px; margin-bottom: 2px; }
        .subtitulo { color: #777; font-size: 14px; margin-top: 0; margin-bottom: 15px; }
        
        input {
            width: 80%;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover { background-color: #0056b3; }
        
        .resultado {
            margin-top: 20px;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
        }
        .encontrado { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .no-encontrado { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        
        /* Nueva sección para las etiquetas del inventario */
        .contenedor-inventario {
            max-height: 200px;
            overflow-y: auto;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: white;
        }
        .producto-tag {
            background-color: #e9ecef;
            color: #495057;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            text-transform: capitalize;
            border: 1px solid #ced4da;
        }
    </style>
</head>
<body>

    <h1>🔍 Localizador de Productos</h1>
    <p>Ingresa el producto que buscas para saber su ubicación:</p>
    
    <form method="POST">
        <input type="text" name="producto" placeholder="¿Qué buscas hoy? (ej. pan, cafe)" value="{{ producto_buscado }}">
        <br>
        <button type="submit">Buscar Ubicación</button>
    </form>

    {% if mensaje %}
        <div class="resultado {{ clase }}">
            {{ mensaje | safe }}
        </div>
    {% endif %}

    <h2>📋 Inventario de la tienda</h2>
    <p class="subtitulo">(Escribe cualquiera de estos productos arriba para conocer su pasillo)</p>
    
    <div class="contenedor-inventario">
        {% for producto in inventario.keys() %}
            <span class="producto-tag">{{ producto }}</span>
        {% endfor %}
    </div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    mensaje = ""
    clase = ""
    producto_buscado = ""
    
    if request.method == "POST":
        producto_buscado = request.form.get("producto", "").strip().lower()
        
        if not producto_buscado:
            mensaje = "Por favor, escribe el nombre de un producto."
            clase = "no-encontrado"
        elif producto_buscado in inventario:
            info = inventario[producto_buscado]
            mensaje = f"📍 El producto <strong>'{producto_buscado}'</strong> está en el <strong>Pasillo {info['pasillo']}</strong>, <strong>Estante {info['estante']}</strong>."
            clase = "encontrado"
        else:
            # MENSAJE CORREGIDO: Más realista para una tienda
            mensaje = f"❌ No disponemos de ese producto por el momento. Revisa la lista de inventario abajo."
            clase = "no-encontrado"
            
    return render_template_string(HTML_TEMPLATE, mensaje=mensaje, clase=clase, producto_buscado=producto_buscado, inventario=inventario)

if __name__ == "__main__":
    app.run(debug=True, port=5050)