import google.generativeai as genai
from dotenv import load_dotenv
import os
import main

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

general_prompt = (
    "Eres un asistente inteligente diseñado para ayudar a los usuarios de una aplicación de gestión de proyectos "
    "similar a Trello. Tu objetivo es mejorar la experiencia del usuario utilizando inteligencia artificial "
    "generativa. Utiliza la información contextual proporcionada sobre tableros, listas y tarjetas para construir "
    "respuestas útiles y relevantes.\n"
    "El tablero actual contiene varias listas, cada una con un título y una descripción. Cada lista puede tener "
    "múltiples tarjetas, las cuales también tienen títulos y descripciones.\n"
    "Recuerda que todas las respuestas deben ser claras, concisas y utilizar un lenguaje amigable. No incluyas "
    "símbolos inusuales y asegúrate de que la información se base únicamente en los datos del contexto que se te "
    "proporcionen.\n"
    "Cada uno de los mensajes te te mande no deben tener estado, o sea una vez que me contestes olvidate de lo que me "
    "respondiste, solo basate en el mensaje que recibas, no te bases en el historial de mensajes."
    "Por ultimo no dubloques informacion, si detectas que ya esta la informacion en el tablero, no agregues cosas "
    "similares, agrega contenido nuevo solo."
)


def summarizeContent(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        "Resumen solicitado:\n"
        "Genera un resumen claro y conciso del siguiente contenido, destacando los puntos clave y eliminando detalles "
        "innecesarios.\n"
        "El resultado debe tener menos palabras que el texto original.\n\n"
        f"Texto a resumir:\n\"{text}\""
    )
    return model.generate_content(prompt).text


def expandContent(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        "Expansión solicitada:\n"
        "Amplía el contenido a continuación, proporcionando detalles adicionales, ejemplos relevantes y explicaciones "
        "más profundas.\n"
        "La expansión debe contener un número significativamente mayor de palabras que el texto original.\n\n"
        f"Texto a ampliar:\n\"{text}\""
    )
    return model.generate_content(prompt).text


def rewriteAndCorrectContent(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        "Reescritura y corrección solicitada:\n"
        "Reformula el texto proporcionado para mejorar la claridad, la fluidez y la corrección gramatical.\n"
        "Haz los ajustes necesarios para asegurar un mejor estilo y legibilidad.\n\n"
        f"Texto a reescribir:\n\"{text}\""
    )
    return model.generate_content(prompt).text


def generateVariations(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        "Variaciones solicitadas:\n"
        "Crea hasta 4 formas diferentes de expresar el siguiente texto, manteniendo su significado original.\n"
        "Las variaciones deben presentarse en una lista, separadas por guiones de la siguiente forma:\n"
        "Variación 1: variacion 1 \n Variación 2: variacion 2 \n Variación 3: variacion 3 ...\n\n"
        f"Texto a variar:\n\"{text}\""
    )
    return model.generate_content(prompt).text


def correctContent(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        "Corrección solicitada:\n"
        "Revisa y corrige cualquier error gramatical, ortográfico o de estilo en el siguiente texto, "
        "asegurando que la redacción sea clara y precisa.\n\n"
        f"Texto a corregir:\n\"{text}\""
    )
    return model.generate_content(prompt).text


def generateListsForBoard(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        f"El contexto del tablero es el siguiente:\n{main.getContext()}\n\n"
        "Tu tarea es crear listas de manera inteligente, basadas en el tema del tablero indicado, y proporcionar "
        "descripciones detalladas y útiles para cada lista. Considera la temática implícita del título del tablero y "
        "adapta las listas para que sean relevantes y útiles. El objetivo es que las listas cubran aspectos "
        "importantes relacionados con la temática del tablero.\n\n"
        "Para el formato de salida cada par de título y descripción debe seguir esta estructura, esta estructura se "
        "debe respetar si o si, no podes agregarle nada mas, solo el titulo un - y la descripcion (recuerda tratar "
        "todo como texto, no markdown, noo sea  uses ** o ##):\n"
        "Título de la lista - Descripción de la lista\n\n"
        "Maximo generame 6 elementos, o sea maximo 6 conjuntos titulo descripcion"
        f"Aparte del contexto, la informacion principal para basarte es la siguiente: \"{text}\"\n"
    )
    return model.generate_content(prompt).text


def generateCardsForList(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        f"El contexto del tablero es el siguiente:\n{main.getContext()}\n\n"
        "Tu tarea es crear títulos y descripciones de tarjetas para tareas basadas en el título de una lista y el "
        "contexto del tablero. Las tarjetas deben ser precisas, relevantes y deben alinearse con la temática del "
        "tablero y la lista específica. Piensa en pasos detallados, tareas y subprocesos que serían útiles dentro de "
        "la lista dada.\n\n"
        "Para el formato de salida cada par de título y descripción debe seguir esta estructura, esta estructura se "
        "debe respetar si o si, no podes agregarle nada mas, solo el titulo un - y la descripcion (recuerda tratar "
        "todo como texto, no markdown, noo sea  uses ** o ##):\n"
        "Título de la tarjeta - Descripción de la tarjeta\n\n"
        "Recorda de no darme mas de 10 elementos, maximo 10 conjuntos titulo descripcion.\n"
        f"Aparte del contexto, la informacion principal para basarte es la siguiente: \"{text}\"\n"
    )
    print(prompt)
    return model.generate_content(prompt).text


def generateListDescription(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        f"El contexto del tablero es el siguiente:\n{main.getContext()}\n\n"
        "Tu objetivo es crear una descripción clara y útil para una lista, basada en su título y cualquier contexto "
        "adicional proporcionado. La descripción debe explicar el propósito de la lista y detallar qué tipo de "
        "elementos o tareas se agrupan en ella, independientemente del tema que se trate\n\n"
        f"Aparte del contexto, la informacion principal para basarte es la siguiente: \"{text}\"\n"
    )
    return model.generate_content(prompt).text


def generateCardDescription(text: str):
    prompt = (
        f"{general_prompt}\n\n"
        "Tu tarea es generar descripciones claras y detalladas para las tarjetas de tareas o elementos dentro de una "
        "lista, basándote en el título de la tarjeta y cualquier contexto adicional proporcionado. La descripción "
        "debe explicar de manera concisa el propósito de la tarjeta, los posibles pasos o detalles necesarios para "
        "completar la tarea, y cualquier información relevante que ayude a entenderla mejor.\n\n"
        f"Aparte del contexto, la informacion principal para basarte es la siguiente: \"{text}\"\n"
    )
    return model.generate_content(prompt).text


