from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import ia
import utils


app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
uvicorn main:app --reload
http://127.0.0.1:8000/docs
pip install fastapi
pip install uvicorn
pip install pydantic
"""


class BoardTitleModel(BaseModel):
    boardTitle: str


class BoardTopicModel(BaseModel):
    boardTopic: str


class ListModel(BaseModel):
    idList: Optional[str] = ""
    title: str
    description: str


class CardModel(BaseModel):
    idCard: Optional[str] = ""
    description: str
    idList: str
    title: str


class IAModel(BaseModel):
    text: str


lists: List[ListModel] = []
cards: List[CardModel] = []
boardTitle: str = "Titulo de la targeta"
boardTopic: str = "Libre"


@app.get("/boardTitle", response_model=BoardTitleModel)
async def getBoardTitle():
    return {"boardTitle": boardTitle}


@app.get("/boardTopic", response_model=BoardTopicModel)
async def getBoardTopic():
    return {"boardTopic": boardTopic}


@app.get("/topics")
async def getTopics():
    top = []
    for e in topics.keys():
        top.append(e)
    return {"topics": top}


@app.put("/boardTitle")
async def updateBoardTitle(boardTitleModel: BoardTitleModel):
    global boardTitle
    boardTitle = boardTitleModel.boardTitle
    return {"detail": "Board title updated"}


@app.put("/boardTopic")
async def updateBoardTopic(boardTopicModel: BoardTopicModel):
    global boardTopic
    boardTopic = boardTopicModel.boardTopic
    return {"detail": "Board topic updated"}


@app.get("/list", response_model=List[ListModel])
async def getLists():
    return lists


@app.get("/card", response_model=List[CardModel])
async def getCards():
    return cards


@app.post("/list")
async def createList(listData: ListModel):
    newList = ListModel(idList=str(uuid4()), title=listData.title, description=listData.description)
    lists.append(newList)
    return {"detail": "List created"}


@app.post("/card")
async def createCard(cardData: CardModel):
    newCard = CardModel(
        idCard=str(uuid4()),
        description=cardData.description,
        idList=cardData.idList,
        title=cardData.title
    )
    cards.append(newCard)
    return {"detail": "Card created"}


@app.put("/list/{idList}")
async def updateList(idList: str, listData: ListModel):
    for i, item in enumerate(lists):
        if item.idList == idList:
            updatedList = ListModel(idList=idList, title=listData.title, description=listData.description)
            lists[i] = updatedList
            return {"detail": "List updated"}
    raise HTTPException(status_code=404, detail="List not found")


@app.put("/card/{idCard}")
async def updateCard(idCard: str, cardData: CardModel):
    for i, item in enumerate(cards):
        if item.idCard == idCard:
            updatedCard = CardModel(
                idCard=idCard,
                description=cardData.description,
                idList=cardData.idList,
                title=cardData.title
            )
            cards[i] = updatedCard
            return {"detail": "Card updated"}
    raise HTTPException(status_code=404, detail="Card not found")


@app.delete("/list/{idList}")
async def deleteList(idList: str):
    isFinded = False
    for i, item in enumerate(lists):
        if item.idList == idList:
            del lists[i]
            isFinded = True
    for i, item in enumerate(cards):
        if item.idList == idList:
            del cards[i]
    if isFinded:
        return {"detail": "List deleted"}
    raise HTTPException(status_code=404, detail="List not found")


@app.delete("/card/{idCard}")
async def deleteCard(idCard: str):
    print(1)
    for i, item in enumerate(cards):
        if item.idCard == idCard:
            del cards[i]
            return {"detail": "Card deleted"}
    raise HTTPException(status_code=404, detail="Card not found")


@app.post("/ia/summarizeContent")
async def summarizeContent(iaModel: IAModel):
    return ia.summarizeContent(iaModel.text)


@app.post("/ia/expandContent")
async def expandContent(iaModel: IAModel):
    return ia.expandContent(iaModel.text)


@app.post("/ia/rewriteAndCorrectContent")
async def rewriteAndCorrectContent(iaModel: IAModel):
    return ia.rewriteAndCorrectContent(iaModel.text)


@app.post("/ia/generateVariations")
async def generateVariations(iaModel: IAModel):
    return ia.generateVariations(iaModel.text)


@app.post("/ia/correctContent")
async def correctContent(iaModel: IAModel):
    return ia.correctContent(iaModel.text)


@app.post("/ia/generateListsForBoard")
async def generateListsForBoard():
    return utils.processGenerateListsForBoard(ia.generateListsForBoard(boardTitle))


@app.post("/ia/generateCardsForList")
async def generateCardsForList(iaModel: IAModel):
    return utils.processGenerateCardsForList(ia.generateCardsForList(iaModel.text))


@app.post("/ia/generateListDescription")
async def generateListDescription(iaModel: IAModel):
    return ia.generateListDescription(iaModel.text)


@app.post("/ia/generateCardDescription")
async def generateCardDescription(iaModel: IAModel):
    return ia.generateCardDescription(iaModel.text)


def getContext() -> str:
    context = f"--- Titulo del tablero: {boardTitle} ---\n\n"
    if (boardTopic != "Libre"):
        context += "El tema del tablero es el siguiente:\n"
        context += f"- Tema: {boardTopic}"
        context += f"- Descripcion del tema: {topics[boardTopic]}\n\n"
    for index, list in enumerate(lists, start=1):
        context += f"Lista {index}:\n"
        context += f"- Titulo: {list.title}\n"
        context += f"- Descripcion: {list.description}\n"
        context += "- Tarjetas:\n"
        filtered_cards = [card for card in cards if card.idList == list.idList]
        for card_index, card in enumerate(filtered_cards, start=1):
            context += f"   Tarjeta {card_index}:\n"
            context += f"   - Titulo: {card.title}\n"
            context += f"   - Descripcion: {card.description}\n"
        context += "\n"
    print(context)
    return context


topics = {
    "Libre": "",
    "Gestión de Proyectos": "Tableros orientados a la planificación y seguimiento de proyectos, que incluyen listas como 'Fases del proyecto', 'Tareas pendientes', 'En progreso' y 'Finalizadas'. Este tipo de tablero ayuda a los equipos a coordinar esfuerzos, asignar tareas y realizar un seguimiento de los plazos para garantizar la entrega efectiva de los objetivos.",
    "Planificación de Tareas Diarias": "Tableros que ayudan a gestionar tareas diarias o semanales, con listas como 'Por hacer', 'En proceso', 'Completado' y 'Prioridad alta'. Estos tableros permiten una visualización clara de las tareas que necesitan atención inmediata y aquellas que ya se han completado, optimizando la productividad personal o del equipo.",
    "Organización de Eventos": "Tableros dedicados a coordinar todos los detalles de un evento, como bodas, fiestas o conferencias. Las listas pueden incluir 'Preparativos', 'Confirmaciones de asistentes', 'Contrataciones de proveedores' y 'Logística'. Este tipo de tablero es útil para no dejar ningún detalle al azar y garantizar que el evento se desarrolle sin inconvenientes.",
    "Planificación de Viajes": "Tableros diseñados para organizar viajes, con listas como 'Itinerario', 'Reservas de hotel', 'Lugares por visitar', 'Documentación requerida' y 'Transporte'. Permite que los viajeros se mantengan organizados y preparados, reduciendo el estrés y mejorando la experiencia general del viaje.",
    "Compras y Listas de Regalos": "Tableros que facilitan la organización de compras y la planificación de regalos, especialmente útiles durante festividades o eventos importantes. Las listas pueden incluir 'Por comprar', 'Comprado', 'Comparar precios' y 'Regalos empaquetados'. Ideal para mantener el control del presupuesto y asegurarse de que no falte nada.",
    "Aprendizaje Personal": "Tableros orientados al seguimiento de actividades de aprendizaje, con listas como 'Temas a estudiar', 'En proceso', 'Completado' y 'Recursos adicionales'. Útil para estudiantes o autodidactas que desean seguir un plan de estudio y monitorear su progreso a lo largo del tiempo.",
    "Gestión de Equipos de Trabajo": "Tableros que ayudan a coordinar y gestionar las tareas de un equipo, con listas como 'Asignaciones de tareas', 'Tareas en revisión', 'Feedback' y 'Reuniones pendientes'. Ayuda a mantener la comunicación clara y asegura que cada miembro del equipo conozca sus responsabilidades.",
    "Planificación de Contenidos para Redes Sociales": "Tableros que permiten planificar y organizar la creación y publicación de contenido para redes sociales, con listas como 'Ideas de contenido', 'En proceso de diseño', 'Programado' y 'Publicado'. Es ideal para los administradores de redes sociales y creadores de contenido que buscan mantener un flujo constante de publicaciones.",
    "Planificación de Menús y Dietas": "Tableros que ayudan a estructurar y planificar menús diarios o semanales, con listas como 'Desayuno', 'Almuerzo', 'Cena' y 'Snacks', así como recetas y horarios de comidas. Ideal para personas que buscan seguir un plan alimenticio saludable y organizado.",
    "Seguimiento de Hábitos": "Tableros dedicados al seguimiento de hábitos saludables y rutinas diarias, con listas como 'Hábitos diarios', 'En progreso', 'Completado' y 'Evaluación semanal'. Perfecto para quienes buscan establecer y mantener hábitos consistentes a lo largo del tiempo.",
    "Gestión de Finanzas Personales": "Tableros que ayudan a monitorear ingresos, gastos y presupuestos personales o familiares, con listas como 'Ingresos', 'Gastos', 'Próximos pagos' y 'Metas de ahorro'. Ofrecen una manera visual y organizada de gestionar las finanzas y planificar el futuro financiero.",
    "Proyectos de Desarrollo de Software": "Tableros orientados al desarrollo de software, con listas como 'Backlog', 'En desarrollo', 'En revisión', 'Desplegado' y 'Bugs reportados'. Son una herramienta esencial para equipos de desarrollo que desean seguir metodologías ágiles como Kanban o Scrum.",
    "Mantenimiento del Hogar": "Tableros que facilitan la organización de tareas relacionadas con el mantenimiento del hogar, como 'Tareas de limpieza', 'Reparaciones', 'Mantenimiento mensual' y 'Compras para el hogar'. Ideal para mantener la casa en perfecto estado y llevar un registro de lo que se ha realizado y lo que falta por hacer.",
    "Preparativos para Festividades": "Tableros para organizar festividades como Navidad, Halloween o fiestas de fin de año. Las listas pueden incluir 'Decoraciones', 'Compras de regalos', 'Invitaciones' y 'Actividades planificadas'. Ayuda a que la planificación sea más divertida y organizada.",
    "Planificación Académica": "Tableros diseñados para estudiantes que necesitan organizar sus clases, tareas y exámenes. Las listas pueden incluir 'Clases', 'Asignaciones', 'Proyectos de grupo' y 'Exámenes próximos'. Es una herramienta útil para mantener todo bajo control durante el período académico.",
    "Desarrollo Personal y Metas": "Tableros enfocados en el desarrollo personal, con listas como 'Objetivos a largo plazo', 'Metas semanales', 'Reflexiones', 'Logros alcanzados' y 'Áreas de mejora'. Ayuda a mantener la motivación y a seguir un plan de crecimiento constante.",
    "Revisión de Libros y Películas": "Tableros donde los usuarios pueden gestionar los libros que quieren leer o las películas que quieren ver. Las listas pueden ser 'Por leer/ver', 'En progreso', 'Completado' y 'Reseñas'. Ideal para aquellos que quieren llevar un registro de sus experiencias literarias y cinematográficas.",
    "Planificación de Sesiones de Brainstorming": "Tableros que facilitan las sesiones de brainstorming, con listas como 'Ideas iniciales', 'Desarrollo de ideas', 'Filtrado de ideas' y 'Acciones a seguir'. Perfecto para fomentar la creatividad y mantener un registro de todas las ideas generadas durante las reuniones.",
    "Preparación de Charlas o Presentaciones": "Tableros diseñados para organizar y estructurar presentaciones con listas como 'Ideas', 'Contenido', 'Diapositivas completadas' y 'Pruebas de presentación'. Ayuda a mantener un flujo claro y asegurar que todos los aspectos de la presentación estén preparados y revisados antes del evento.",
    "Gestión de Recursos Humanos": "Tableros que facilitan la gestión de procesos de selección y reclutamiento con listas como 'Candidatos', 'Entrevistas programadas', 'Feedback de entrevistas' y 'Ofertas enviadas'. Útil para centralizar información sobre los candidatos y el progreso de las entrevistas.",
    "Organización de Talleres o Cursos": "Tableros dedicados a la planificación y gestión de talleres o cursos, con listas como 'Módulos', 'Materiales', 'Tareas de los participantes' y 'Feedback de los estudiantes'. Facilita la organización del contenido y la monitorización del progreso de los estudiantes.",
    "Seguimiento de Proyectos de Renovación o Remodelación": "Tableros creados para coordinar proyectos de renovación, con listas como 'Planos', 'Materiales comprados', 'Obras en progreso' y 'Inspección final'. Ayuda a organizar las fases del proyecto y a garantizar que todos los pasos se completen a tiempo.",
    "Planificación de Reuniones": "Tableros que permiten organizar reuniones eficientemente con listas de 'Agenda', 'Puntos a discutir', 'Acciones tomadas' y 'Tareas asignadas post-reunión'. Permite un seguimiento claro de las decisiones tomadas y las responsabilidades posteriores a la reunión.",
    "Control de Inventario": "Tableros diseñados para la gestión de inventarios, con listas de 'Productos', 'Stock actual', 'Reabastecer' y 'Productos en oferta'. Facilita el seguimiento del inventario y la planificación de compras futuras.",
    "Planificación de Campañas de Marketing": "Tableros orientados a la creación y seguimiento de campañas de marketing, con listas de 'Objetivos de la campaña', 'Estrategias', 'En proceso' y 'Análisis de resultados'. Ayuda a coordinar equipos y a evaluar la efectividad de las estrategias implementadas.",
    "Organización de Voluntariados o Actividades Comunitarias": "Tableros diseñados para planificar y coordinar actividades de voluntariado con listas como 'Tareas', 'Reuniones comunitarias', 'Voluntarios asignados' y 'Eventos pasados'. Facilita la organización y asignación de tareas a los voluntarios.",
    "Desarrollo de Proyectos Artísticos": "Tableros orientados a proyectos creativos, con listas de 'Inspiración', 'Bocetos', 'En progreso' y 'Finalizado'. Útil para artistas que deseen estructurar sus procesos creativos y llevar un seguimiento de sus obras.",
    "Planificación de Clases para Profesores": "Tableros que ayudan a los profesores a planificar y organizar sus clases, con listas de 'Lecciones planificadas', 'Materiales necesarios', 'Tareas de los estudiantes' y 'Evaluaciones'. Permite una gestión efectiva del contenido y de las evaluaciones de los estudiantes.",
    "Organización de Conferencias o Seminarios": "Tableros orientados a la planificación de conferencias y seminarios con listas de 'Ponentes', 'Agenda', 'Tareas de logística' y 'Material de conferencia'. Facilita la gestión de detalles logísticos y el seguimiento de la planificación del evento.",
    "Planificación de Estrategias Empresariales": "Tableros que ayudan a coordinar la planificación estratégica de una empresa, con listas como 'Análisis FODA', 'Ideas estratégicas', 'Proyectos a implementar' y 'Resultados esperados'. Permite a los equipos directivos visualizar y gestionar las estrategias a implementar."
}
