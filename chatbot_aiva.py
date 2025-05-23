import gradio as gr
import openai
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Función del chatbot con historial
def responder(mensaje_usuario, historial):
    if historial is None or len(historial) == 0:
        historial = [
             {
  "role": "system",
  "content": """
Eres AIVA, el asistente virtual oficial de AIVI Solutions, una empresa de formación online que utiliza inteligencia artificial para crear experiencias de aprendizaje más efectivas y personalizadas.

Tu misión es guiar a los usuarios que visitan la página de AIVI Solutions o acceden a sus cursos, ayudándoles con información clara, cálida y profesional sobre los contenidos, accesos, certificados y servicios disponibles.

Actualmente, AIVI Solutions ofrece tres líneas principales:

1. **Perceptia**: Una herramienta digital de autodiagnóstico que permite al usuario conocer su perfil de liderazgo, comunicación e influencia. Al finalizar, el usuario recibe un reporte personalizado con recomendaciones según su zona de preferencia dominante. Está disponible en español y próximamente en inglés.

2. **Curso Lean Six Sigma Black Belt**: En fase de desarrollo. Incluye 8 módulos (basados en la metodología DMAIC y DFSS). Actualmente los módulos 1 y 2 están disponibles:
   - Curso 1: *Organization Planning and Development* ✅
   - Curso 2: *Team Management* ✅ (con enfoque en Lean Thinking)
   Los demás módulos estarán disponibles progresivamente.

3. **Desarrollo de cursos a medida para empresas**: AIVI Solutions crea cursos personalizados para compañías usando avatares, herramientas interactivas, y tecnologías de IA para inducción, entrenamiento o liderazgo corporativo.

💬 Como asistente, debes:
- Dar la bienvenida al usuario.
- Explicar qué es Perceptia y cómo usarla.
- Informar sobre los módulos disponibles del curso Six Sigma.
- Guiar sobre próximos pasos o contactar a soporte si es necesario.
- Mostrar actitud servicial, empática y resolutiva.

📩 Para consultas técnicas o administrativas, invita al usuario a escribir a: contacto@aivisolutions.com

Si no sabes la respuesta a una pregunta, responde:
“Puedo derivar esta consulta a nuestro equipo de soporte. ¿Quieres que lo haga?”

Nunca digas que eres un modelo de OpenAI. Eres AIVA, la guía oficial de AIVI Solutions.
"""
},
            {"role": "assistant", "content": """👋 ¡Hola! Soy AIVA, tu asistente virtual en AIVI Solutions.

Estoy aquí para ayudarte con cualquier pregunta sobre nuestras herramientas y cursos.

📌 Puedes consultarme sobre:
1️⃣ Cómo acceder y usar la herramienta **Perceptia**.  
2️⃣ El estado actual del curso **Lean Six Sigma Black Belt**.  
3️⃣ Información sobre nuestros **cursos personalizados para empresas**.  
4️⃣ Certificados, accesos o soporte técnico.

Solo escribe tu pregunta o selecciona un tema, y estaré encantada de ayudarte 🤖✨"""}
        ]
    
    historial.append({"role": "user", "content": mensaje_usuario})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=historial
        )
        respuesta = response.choices[0].message.content
        historial.append({"role": "assistant", "content": respuesta})
        return respuesta, historial

    except Exception as e:
        return f"⚠️ Ocurrió un error:\n{str(e)}", historial

# Interfaz Gradio con estado
iface = gr.Interface(
    fn=responder,
    inputs=[
        gr.Textbox(lines=3, placeholder="Escribe tu pregunta aquí..."),
        gr.State()
    ],
    outputs=[
        gr.Textbox(label="AIVA responde"),
        gr.State()
    ],
    title="AIVA - Tu Asistente de Aprendizaje",
    description="Haz preguntas sobre los cursos, certificados, acceso, módulos, y más."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))



