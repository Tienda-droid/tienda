from flask import Flask, render_template_string, request

app = Flask(__name__)

# 1. INVENTARIO COMPLETO (30 productos con Pasillo y Estante asignado)
inventario = {
    # Pasillo 1: Lacteos y Frescos
    "leche": {"pasillo": 1, "estante": 1},
    "huevos": {"pasillo": 1, "estante": 2},
    "queso": {"pasillo": 1, "estante": 3},
    "mantequilla": {"pasillo": 1, "estante": 4},
    "yogur": {"pasillo": 1, "estante": 5},
    "jamon": {"pasillo": 1, "estante": 6},
    # Pasillo 2: Abarrotes y Secos
    "arroz": {"pasillo": 2, "estante": 1},
    "fideos": {"pasillo": 2, "estante": 2},
    "azucar": {"pasillo": 2, "estante": 3},
    "cafe": {"pasillo": 2, "estante": 4},
    "aceite": {"pasillo": 2, "estante": 5},
    "atun": {"pasillo": 2, "estante": 6},
    "sal": {"pasillo": 2, "estante": 7},
    "lentejas": {"pasillo": 2, "estante": 8},
    # Pasillo 3: Snacks y Dulces
    "pan": {"pasillo": 3, "estante": 1},
    "gaseosa": {"pasillo": 3, "estante": 2},
    "galletas": {"pasillo": 3, "estante": 3},
    "papas fritas": {"pasillo": 3, "estante": 4},
    "chocolate": {"pasillo": 3, "estante": 5},
    "jugos": {"pasillo": 3, "estante": 6},
    "caramelos": {"pasillo": 3, "estante": 7},
    "cereales": {"pasillo": 3, "estante": 8},
    # Pasillo 4: Limpieza y Aseo
    "jabon": {"pasillo": 4, "estante": 1},
    "papel higienico": {"pasillo": 4, "estante": 2},
    "shampoo": {"pasillo": 4, "estante": 3},
    "detergente": {"pasillo": 4, "estante": 4},
    "pasta dental": {"pasillo": 4, "estante": 5},
    "desodorante": {"pasillo": 4, "estante": 6},
    "esponja": {"pasillo": 4, "estante": 7},
    "cloro": {"pasillo": 4, "estante": 8}
}

# 2. INTERFAZ GRÁFICA CON PLANO DIGITAL INTEGRADO
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plano de Distribución Interactiva - Minimarket</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
        }
        
        /* Estructura del Panel de Control (Dashboard) */
        .dashboard {
            display: flex;
            width: 1100px;
            gap: 20px;
        }
        
        /* COLUMNA IZQUIERDA: Catálogo limpio sin ubicaciones iniciales */
        .columna-izquierda {
            flex: 0.8;
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            max-height: 85vh;
            display: flex;
            flex-direction: column;
        }
        
        .lista-inventario {
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding-right: 5px;
        }
        
        .producto-item {
            background-color: #f8fafc;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
            text-transform: capitalize;
            border-left: 4px solid #3498db;
            color: #334155;
            font-weight: 500;
        }
        
        /* COLUMNA DERECHA: Buscador e Interacción */
        .columna-derecha {
            flex: 2;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .panel {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        h1, h2 { color: #2c3e50; margin-top: 0; }
        h1 { font-size: 24px; text-align: center; }
        h2 { font-size: 18px; border-bottom: 2px solid #eee; padding-bottom: 8px; }
        .subtitulo { color: #7f8c8d; font-size: 13px; margin-top: -5px; margin-bottom: 15px; }
        
        /* Formulario Buscador */
        form { display: flex; gap: 10px; margin-bottom: 15px; }
        input {
            flex: 1;
            padding: 12px;
            font-size: 15px;
            border: 2px solid #cbd5e1;
            border-radius: 6px;
            outline: none;
        }
        input:focus { border-color: #3498db; }
        button {
            padding: 12px 24px;
            font-size: 15px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background-color: #2980b9; }
        
        .resultado {
            padding: 12px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 6px;
            text-align: center;
        }
        .encontrado { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .no-encontrado { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        
        /* 📐 Distribucion de la tienda (HTML/CSS) */
        .plano-tienda {
            border: 4px solid #2c3e50;
            border-radius: 12px;
            background-color: #ffffff;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        /* Categorías en la parte superior */
        .categorias-top {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            text-align: center;
        }
        .cat-box {
            padding: 6px;
            font-weight: bold;
            font-size: 11px;
            border-radius: 4px;
            border: 1px solid #ddd;
            text-transform: uppercase;
        }
        .cat-1 { background-color: #e3f2fd; color: #0d47a1; }
        .cat-2 { background-color: #e8f5e9; color: #1b5e20; }
        .cat-3 { background-color: #fff3e0; color: #e65100; }
        
        /* Área Central de Distribución */
        .area-central {
            display: flex;
            gap: 15px;
            height: 340px;
        }
        
        /* Sección Lateral Izquierda de Congelados */
        .zona-congelados {
            width: 45px;
            background-color: #e0f7fa;
            border: 2px dashed #4dd0e1;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #00838f;
            font-size: 12px;
            writing-mode: vertical-lr;
            transform: rotate(180deg);
            text-align: center;
        }
        
        /* Contenedor de los 4 Pasillos Principales */
        .grid-pasillos {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }
        
        /* Estructura Individual de cada Pasillo */
        .pasillo-bloque {
            border: 2px solid #cbd5e1;
            background-color: #f8fafc;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            padding: 8px;
            transition: all 0.3s ease;
        }
        
        .pasillo-titulo {
            text-align: center;
            font-weight: bold;
            font-size: 13px;
            color: #1e293b;
            margin-bottom: 2px;
        }
        
        .pasillo-categoria {
            text-align: center;
            font-size: 10px;
            color: #64748b;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        /* Cuadrícula interna de los estantes */
        .estantes-lista {
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
            justify-content: center;
        }
        
        .estante-celda {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 5px 0;
            font-size: 11px;
            text-align: center;
            color: #64748b;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        /* 🟩 EFECTO DINÁMICO DE MARCADO VERDE */
        /* Al activar un pasillo completo */
        .pasillo-bloque.activo {
            background-color: #f0fdf4 !important;
            border-color: #22c55e !important;
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.3);
            transform: scale(1.01);
        }
        .pasillo-bloque.activo .pasillo-titulo { color: #166534; }
        
        /* Al activar el estante preciso */
        .estante-celda.estante-activo {
            background-color: #22c55e !important;
            color: white !important;
            border-color: #16a34a !important;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(22, 163, 74, 0.3);
        }
        
        /* Elementos Arquitectónicos de la Base */
        .plano-base {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 10px;
        }
        
        .puerta-box {
            background-color: #ef4444;
            color: white;
            padding: 5px 12px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 4px;
        }
        
        .caja-box {
            background-color: #475569;
            color: white;
            padding: 8px 24px;
            font-size: 12px;
            font-weight: bold;
            border-radius: 4px;
        }
        
        .salida-box {
            background-color: #64748b;
            color: white;
            padding: 5px 12px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 4px;
        }
    </style>
</head>
<body>

    <div class="dashboard">
        
        <div class="columna-izquierda">
            <h2>📋 Catálogo</h2>
            <p class="subtitulo">Productos en tienda ({{ inventario|length }} artículos):</p>
            <div class="lista-inventario">
                {% for producto in inventario.keys()|sort %}
                    <div class="producto-item">{{ producto }}</div>
                {% endfor %}
            </div>
        </div>
        
        <div class="columna-derecha">
            
            <div class="panel">
                <h1>🔍 Localizador de Productos Tienda "La economica"</h1>
                <p style="text-align: center; color: #64748b; margin-top: -5px; font-size: 14px;">
                    Digita el artículo que necesitas para encender su ubicación física en tiempo real.
                </p>
                
                <form method="POST">
                    <input type="text" name="producto" placeholder="Escribe aquí el producto (ej. leche, fideos, cloro)" value="{{ producto_buscado }}">
                    <button type="submit">Localizar</button>
                </form>

                {% if mensaje %}
                    <div class="resultado {{ clase }}">
                        {{ mensaje | safe }}
                    </div>
                {% endif %}
            </div>
            
            <div class="panel plano-tienda">
                <h2>📐 Distribución Geométrica de la Planta</h2>
                
                <div class="categorias-top">
                    <div class="cat-box cat-1">Lácteos y Frescos</div>
                    <div class="cat-box cat-2">Abarrotes y Secos</div>
                    <div class="cat-box cat-3">Snacks y Dulces</div>
                </div>
                
                <div class="area-central">
                    
                    <div class="grid-pasillos">
                        
                        <div class="pasillo-bloque {% if pasillo_detectado == 1 %}activo{% endif %}">
                            <div class="pasillo-titulo">PASILLO 1</div>
                            <div class="pasillo-categoria">Lácteos y Frescos</div>
                            <div class="estantes-lista">
                                {% for e in range(1, 9) %}
                                    <div class="estante-celda {% if pasillo_detectado == 1 and estante_detectado == e %}estante-activo{% endif %}">
                                        Estante {{ e }}
                                    </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="pasillo-bloque {% if pasillo_detectado == 2 %}activo{% endif %}">
                            <div class="pasillo-titulo">PASILLO 2</div>
                            <div class="pasillo-categoria">Abarrotes y Secos</div>
                            <div class="estantes-lista">
                                {% for e in range(1, 9) %}
                                    <div class="estante-celda {% if pasillo_detectado == 2 and estante_detectado == e %}estante-activo{% endif %}">
                                        Estante {{ e }}
                                    </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="pasillo-bloque {% if pasillo_detectado == 3 %}activo{% endif %}">
                            <div class="pasillo-titulo">PASILLO 3</div>
                            <div class="pasillo-categoria">Snacks y Dulces</div>
                            <div class="estantes-lista">
                                {% for e in range(1, 9) %}
                                    <div class="estante-celda {% if pasillo_detectado == 3 and estante_detectado == e %}estante-activo{% endif %}">
                                        Estante {{ e }}
                                    </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="pasillo-bloque {% if pasillo_detectado == 4 %}activo{% endif %}">
                            <div class="pasillo-titulo">PASILLO 4</div>
                            <div class="pasillo-categoria">Limpieza y Aseo</div>
                            <div class="estantes-lista">
                                {% for e in range(1, 9) %}
                                    <div class="estante-celda {% if pasillo_detectado == 4 and estante_detectado == e %}estante-activo{% endif %}">
                                        Estante {{ e }}
                                    </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                    </div>
                </div>
                
                <div class="plano-base">
                    <div class="puerta-box">🚪 ENTRADA PRINCIPAL</div>
                    <div class="caja-box">🏪 CAJA / COBRO</div>
                    <div class="salida-box">🚪 SALIDA</div>
                </div>
                
            </div>
            
        </div>
        
    </div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    mensaje = ""
    clase = ""
    producto_buscado = ""
    pasillo_detectado = 0  # Inicialmente ningún pasillo se marca
    estante_detectado = 0  # Inicialmente ningún estante se marca
    
    if request.method == "POST":
        producto_buscado = request.form.get("producto", "").strip().lower()
        
        if not producto_buscado:
            mensaje = "Por favor, escribe el nombre de un producto para iniciar el escaneo."
            clase = "no-encontrado"
        elif producto_buscado in inventario:
            info = inventario[producto_buscado]
            pasillo_detectado = info['pasillo']
            estante_detectado = info['estante']
            
            mensaje = f"📍 <strong>¡Localizado!</strong> El producto <strong>'{producto_buscado}'</strong> está en el <strong>Pasillo {pasillo_detectado}</strong>, <strong>Estante {estante_detectado}</strong>. Revisa la planta gráfica abajo."
            clase = "encontrado"
        else:
            mensaje = f"❌ No disponemos de ese producto por el momento. Consulta el catálogo de la izquierda."
            clase = "no-encontrado"
            
    return render_template_string(
        HTML_TEMPLATE, 
        mensaje=mensaje, 
        clase=clase, 
        producto_buscado=producto_buscado, 
        inventario=inventario,
        pasillo_detectado=pasillo_detectado,
        estante_detectado=estante_detectado
    )

if __name__ == "__main__":
    app.run(debug=True, port=5050)
