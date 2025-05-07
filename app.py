import streamlit as st
import requests
import json
import time
import random
import anthropic
import openai
import elevenlabs
import unicodedata
import base64
from elevenlabs.client import ElevenLabs
import re
import httpx

# Скрываем стандартные элементы Streamlit
st.set_page_config(
    page_title="Тренажёр по грамматике",
    page_icon="🇪🇸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Добавление CSS для адаптации под мобильные устройства и скрытия элементов Streamlit
hide_streamlit_style = """
<style>
    /* Скрываем стандартные элементы Streamlit */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    .viewerBadge_container__1QSob {visibility: hidden !important;}
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK {visibility: hidden !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden !important;}
    
    /* Дополнительные элементы для скрытия */
    button[data-testid="baseButton-headerNoPadding"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    .st-emotion-cache-h5rgaw {display: none !important;}
    ._terminalButton_rix23_138 {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    button.st-emotion-cache-iiif1v {display: none !important;}
    .st-emotion-cache-18ni7ap {display: none !important;}
    
    /* Скрываем бейдж Streamlit и аватар пользователя */
    ._container_gzau3_1 {display: none !important;}
    ._viewerBadge_nim44_23 {display: none !important;}
    ._profileContainer_gzau3_53 {display: none !important;}
    ._profilePreview_gzau3_63 {display: none !important;}
    [data-testid="appCreatorAvatar"] {display: none !important;}
    a[href*="streamlit.io/cloud"] {display: none !important;}
    a[href*="share.streamlit.io/user"] {display: none !important;}
    
    /* Для всех svg внутри скрываемых элементов */
    ._container_gzau3_1 svg, 
    ._viewerBadge_nim44_23 svg {
        display: none !important;
    }
    
    /* Основные стили приложения */
    .stButton button {
        width: 100%;
        margin-bottom: 10px;
    }
    .css-1d391kg {
        padding: 1rem 1rem;
    }
    input[type="text"] {
        font-size: 18px !important;
        height: 50px !important;
    }
    .st-emotion-cache-16idsys p {
        font-size: 18px;
    }
    .st-emotion-cache-5rimss {
        font-size: 18px;
    }
    @media (max-width: 600px) {
        .st-emotion-cache-16idsys p {
            font-size: 16px;
        }
        .st-emotion-cache-5rimss {
            font-size: 16px;
        }
    }
    
    /* Стили для спрятанных настроек */
    .settings-section {
        margin-top: 30px;
        padding: 10px;
        border-top: 1px solid #ddd;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Дополнительная попытка скрыть элементы Streamlit с помощью JavaScript
hide_streamlit_js = """
<script>
    // Функция для скрытия элементов
    function hideElements() {
        // Скрываем все элементы Streamlit
        const elementsToHide = [
            'header', 
            'footer', 
            '.stDeployButton', 
            '#MainMenu',
            '[data-testid="stToolbar"]',
            '[data-testid="stDecoration"]',
            '[data-testid="stStatusWidget"]',
            '.viewerBadge_container__1QSob',
            '.styles_viewerBadge__1yB5_', 
            '.viewerBadge_link__1S137', 
            '.viewerBadge_text__1JaDK',
            '[data-testid="baseButton-headerNoPadding"]',
            '[data-testid="stHeader"]',
            '.st-emotion-cache-h5rgaw',
            '._terminalButton_rix23_138',
            '[data-testid="manage-app-button"]',
            'button.st-emotion-cache-iiif1v',
            '.st-emotion-cache-18ni7ap',
            '._container_gzau3_1',
            '._viewerBadge_nim44_23',
            '._profileContainer_gzau3_53',
            '._profilePreview_gzau3_63',
            '[data-testid="appCreatorAvatar"]',
            'a[href*="streamlit.io/cloud"]',
            'a[href*="share.streamlit.io/user"]'
        ];
        
        // Функция для полного скрытия элемента
        function hideElement(el) {
            if (el) {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.opacity = '0';
                el.style.pointerEvents = 'none';
                el.style.height = '0';
                el.style.width = '0';
                el.style.position = 'absolute';
                el.style.zIndex = '-9999';
                el.style.overflow = 'hidden';
            }
        }
        
        // Применяем скрытие к каждому элементу
        elementsToHide.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(hideElement);
        });
        
        // Дополнительно ищем все ссылки на streamlit
        document.querySelectorAll('a').forEach(a => {
            if (a.href && (a.href.includes('streamlit.io') || a.href.includes('share.streamlit'))) {
                hideElement(a);
            }
        });
        
        // Удаляем все svg внутри нежелательных элементов
        document.querySelectorAll('._container_gzau3_1 svg, ._viewerBadge_nim44_23 svg').forEach(hideElement);
    }
    
    // Запускаем сразу и через небольшую задержку, чтобы учесть асинхронную загрузку элементов
    hideElements();
    setTimeout(hideElements, 500);
    setTimeout(hideElements, 1000);
    setTimeout(hideElements, 2000);
    setTimeout(hideElements, 5000);
    
    // Также добавляем обработчик на изменение DOM, чтобы скрывать вновь появляющиеся элементы
    const observer = new MutationObserver(function(mutations) {
        hideElements();
    });
    
    // Запускаем наблюдение за изменениями в DOM
    observer.observe(document.body, { 
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'style', 'href']
    });
</script>
"""
st.markdown(hide_streamlit_js, unsafe_allow_html=True)

# Получение API ключей
elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Инициализация клиентов API
elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)

# Добавляем глобальные переменные для хранения глаголов из файлов
VERBS_LIST_1 = []
VERBS_LIST_2 = []
VERBS_SESSION_1 = []  # Для отслеживания использованных глаголов из первого списка
VERBS_SESSION_2 = []  # Для отслеживания использованных глаголов из второго списка

# Загружаем глаголы из файлов
try:
    with open('verbs_list_1.txt', 'r', encoding='utf-8') as f:
        VERBS_LIST_1 = [line.strip() for line in f if line.strip()]
except Exception as e:
    print(f"Ошибка при загрузке verbs_list_1.txt: {str(e)}")

try:
    with open('verbs_list_2.txt', 'r', encoding='utf-8') as f:
        VERBS_LIST_2 = [line.strip() for line in f if line.strip()]
except Exception as e:
    print(f"Ошибка при загрузке verbs_list_2.txt: {str(e)}")

def initialize_session_state():
    """Инициализирует переменные состояния сессии."""
    if 'response_history' not in st.session_state:
        st.session_state.response_history = []
    
    if 'current_exercise' not in st.session_state:
        st.session_state.current_exercise = None
    
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False
    
    if 'selected_topics' not in st.session_state:
        # По умолчанию выбраны все темы
        st.session_state.selected_topics = {
            'Presente': True,
            'Pretérito indefinido (perfecto simple)': True,
            'Pretérito imperfecto': True,
            'Pretérito perfecto compuesto': True, 
            'Futuro simple': True,
            'Futuro compuesto': True,
            'Imperativo': True,
            'Participio': True,
            'Gerundio': True,
            'Pronombres': True,
            'Paráfrasis': True
        }
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    
    if 'previous_response' not in st.session_state:
        st.session_state.previous_response = ""
    
    if 'used_verbs' not in st.session_state:
        st.session_state.used_verbs = []  # Список для отслеживания недавно использованных глаголов
    
    if 'settings_expanded' not in st.session_state:
        st.session_state.settings_expanded = False
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "claude-haiku"
    
    if 'speech_rate' not in st.session_state:
        st.session_state.speech_rate = 0.8
    
    if 'gender_preference' not in st.session_state:
        st.session_state.gender_preference = "Мужской"
    
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""
    
    if 'correct' not in st.session_state:
        st.session_state.correct = None
    
    if 'show_translation' not in st.session_state:
        st.session_state.show_translation = False
    
    if 'audio_ready' not in st.session_state:
        st.session_state.audio_ready = False
    
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None
    
    if 'show_settings' not in st.session_state:
        st.session_state.show_settings = False
    
    if 'selected_voice' not in st.session_state:
        st.session_state.selected_voice = "Jhenny Antiques"
    
    if 'voice_id' not in st.session_state:
        st.session_state.voice_id = "2Lb1en5ujrODDIqmp7F3"  # ID для Jhenny Antiques по умолчанию
    
    if 'needs_new_exercise' not in st.session_state:
        st.session_state.needs_new_exercise = False
    
    # Добавляем переменные состояния для отслеживания глаголов из файлов
    if 'verbs_session_1' not in st.session_state:
        st.session_state.verbs_session_1 = []
        
    if 'verbs_session_2' not in st.session_state:
        st.session_state.verbs_session_2 = []

# Основной интерфейс
st.title("Тренажёр по грамматике 🇪🇸")

# Инициализация переменных сессии
initialize_session_state()

# Список времён и конструкций для тренировки
TENSES = [
    "Presente",
    "Pretérito indefinido (perfecto simple)",
    "Pretérito imperfecto",
    "Pretérito perfecto compuesto",
    "Futuro simple",
    "Futuro compuesto",
    "Imperativo"
]

FORMS = [
    "Participio",
    "Gerundio"
]

PRONOUNS = [
    "Pronombres"
]

CONSTRUCTIONS = [
    "Estar + gerundio",
    "Ir a + infinitivo",
    "Acabar de + infinitivo",
    "Tener que + infinitivo",
    "Deber + infinitivo",
    "Poder + infinitivo",
    "Volver a + infinitivo"
]

# Словарь для групп тем
TOPIC_GROUPS = {
    'Paráfrasis': CONSTRUCTIONS
}

def normalize_spanish_text(text):
    """Нормализует испанский текст: удаляет акценты и заменяет ñ на n"""
    # Сначала заменяем ñ на n
    text = text.replace("ñ", "n").replace("Ñ", "N")
    # Затем удаляем все диакритические знаки (акценты)
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')

def get_llm_response(prompt, model="claude-haiku"):
    """Получает ответ от выбранной LLM модели"""
    try:
        if model.startswith("claude"):
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            model_name = ""
            if model == "claude-haiku":
                model_name = "claude-3-haiku-20240307"
            elif model == "claude-sonnet":
                model_name = "claude-3-sonnet-20240229"
            elif model == "claude-3.7-sonnet":
                model_name = "claude-3-5-sonnet-20240620"
            elif model == "claude-opus":
                model_name = "claude-3-opus-20240229"
            
            response = client.messages.create(
                model=model_name,
                max_tokens=1000,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        elif model.startswith("gpt"):
            try:
                # Самый простой способ инициализации OpenAI с минимумом параметров
                client = openai.OpenAI(api_key=openai_api_key)
                model_name = "gpt-4o" if model == "gpt-4o" else "gpt-4o-mini"
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "Ты - помощник для тренировки испанских глаголов."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            except Exception as e:
                # Альтернативный метод, если основной не сработал
                st.error(f"Пробуем альтернативный метод для GPT после ошибки: {str(e)}")
                # Используем legacy метод без создания клиента
                openai.api_key = openai_api_key
                model_name = "gpt-4o" if model == "gpt-4o" else "gpt-4o-mini"
                response = openai.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "Ты - помощник для тренировки испанских глаголов."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000
                )
                return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка при обращении к API: {str(e)}")
        return None

def generate_exercise(model="claude-haiku", max_attempts=3):
    """Генерирует новое упражнение с использованием выбранной модели LLM"""
    # Получаем активные темы
    active_topics = []
    
    # Добавляем выбранные времена
    for tense in TENSES:
        if st.session_state.selected_topics.get(tense, False):
            active_topics.append(tense)
    
    # Добавляем выбранные формы
    for form in FORMS:
        if st.session_state.selected_topics.get(form, False):
            active_topics.append(form)
    
    # Добавляем местоимения, если выбраны
    if st.session_state.selected_topics.get('Pronombres', False):
        active_topics.append('Pronombres (притяжательные и пр.)')
    
    # Добавляем конструкции, если выбрана парафразис
    if st.session_state.selected_topics.get('Paráfrasis', False):
        active_topics.extend(CONSTRUCTIONS)
    
    # Проверяем, что хотя бы одна тема выбрана
    if not active_topics:
        st.warning("Выберите хотя бы одну тему в настройках")
        # Возвращаем все темы, если ничего не выбрано
        active_topics = TENSES + FORMS + ['Pronombres (притяжательные и пр.)'] + CONSTRUCTIONS
    
    # Выбираем случайную тему из активных
    selected_option = random.choice(active_topics)
    
    # Выбираем глагол из одного из файлов согласно указанным вероятностям (60/40)
    selected_verb = None
    
    # Если оба списка глаголов не пусты, выбираем глагол
    if VERBS_LIST_1 or VERBS_LIST_2:
        # Восстанавливаем списки, если все глаголы были использованы
        if not set(VERBS_LIST_1) - set(st.session_state.verbs_session_1) and VERBS_LIST_1:
            st.session_state.verbs_session_1 = []
            
        if not set(VERBS_LIST_2) - set(st.session_state.verbs_session_2) and VERBS_LIST_2:
            st.session_state.verbs_session_2 = []
        
        # Определяем доступные глаголы
        available_verbs_1 = [v for v in VERBS_LIST_1 if v not in st.session_state.verbs_session_1]
        available_verbs_2 = [v for v in VERBS_LIST_2 if v not in st.session_state.verbs_session_2]
        
        # Если один из списков пуст, используем только другой
        if not available_verbs_1 and available_verbs_2:
            verb_source = 2
        elif available_verbs_1 and not available_verbs_2:
            verb_source = 1
        else:
            # В противном случае выбираем источник на основе вероятности
            verb_source = 1 if random.random() < 0.6 else 2
        
        if verb_source == 1 and available_verbs_1:
            selected_verb = random.choice(available_verbs_1)
            st.session_state.verbs_session_1.append(selected_verb)
        elif verb_source == 2 and available_verbs_2:
            selected_verb = random.choice(available_verbs_2)
            st.session_state.verbs_session_2.append(selected_verb)
    
    # Список недавно использованных глаголов для исключения
    excluded_verbs = ", ".join([f'"{verb}"' for verb in st.session_state.used_verbs[-10:]])
    
    # Особые указания для Imperativo
    special_instructions = ""
    if selected_option == "Imperativo":
        special_instructions = """
        ‼️‼️‼️ КРИТИЧЕСКИ ВАЖНО: СОЗДАВАЙ АБСОЛЮТНО УНИКАЛЬНЫЕ ЗАДАНИЯ БЕЗ КАКИХ-ЛИБО ПОВТОРЕНИЙ! ‼️‼️‼️
        
        1️⃣ КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО использовать повторяющиеся шаблоны предложений. 
        Каждое задание должно иметь УНИКАЛЬНУЮ структуру и контекст.
        
        2️⃣ КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО использовать "Señor/Señora + фамилия" (особенно Martínez, Ramírez, García) 
        в каждом задании. Это КРИТИЧЕСКАЯ ошибка!
        
        3️⃣ В КАЖДОМ задании используй ПРИНЦИПИАЛЬНО РАЗНЫЕ обращения из списка ниже.
        НЕ ПОВТОРЯЙ уже использованные обращения.
        
        🔄 ОБЯЗАТЕЛЬНО ВАРЬИРУЙ СТРУКТУРУ предложений:
        - Начинай предложения по-разному (не всегда с обращения)
        - Меняй порядок слов в предложении
        - Используй разную длину предложений
        - Смешивай вопросительные и побудительные предложения
        - Используй как прямые, так и косвенные просьбы/приказы
        
        🔽 ВЫБИРАЙ ИЗ ОГРОМНОГО РАЗНООБРАЗИЯ обращений 🔽
        
        ДЛЯ ФОРМЫ TÚ (неформальное ед. число):
        • Имена (используй РАЗНЫЕ каждый раз): 
          Javi, Miguel, Sara, Carmen, Luisa, Diego, Isabel, Roberto, Eva, Daniel, Natalia, Jorge, 
          Marina, Tomás, Lucía, Alejandro, Cristina, Gabriel, Andrea, Víctor, Julia, Alberto, 
          Beatriz, Ricardo, Teresa, Fernando, Pilar, Francisco, Rosa, Emilio, Laura
          
        • Родственники (используй РАЗНЫЕ): 
          Hijo, Hija, Hermano, Hermana, Primo, Prima, Tío, Tía, Abuelo, Abuela, Sobrino, 
          Sobrina, Nieto, Nieta, Cuñado, Cuñada, Padrino, Madrina
          
        • Неформальные обращения (используй РАЗНЫЕ): 
          Cariño, Tesoro, Cielo, Amor, Guapo, Guapa, Chico, Chica, Joven, Pequeño, Pequeña, 
          Bonito, Bonita
          
        ДЛЯ ФОРМЫ USTED (формальное ед. число):
        • Профессии (используй РАЗНЫЕ): 
          Doctor, Doctora, Profesor, Profesora, Ingeniero, Ingeniera, Arquitecto, Arquitecta, 
          Abogado, Abogada, Agente, Chef, Enfermero, Enfermera, Capitán, Sargento, Inspector, 
          Inspectora, Juez, Jueza, Conductor, Conductora, Piloto, Embajador, Embajadora
          
        • Титулы (используй РАЗНЫЕ): 
          Don, Doña, Excelentísimo, Excelentísima, Ilustrísimo, Ilustrísima, Reverendo, 
          Reverenda, Alteza, Majestad, Presidente, Presidenta, Ministro, Ministra
          
        ДЛЯ ФОРМЫ VOSOTROS (неформальное мн. число):
        • Группы (используй РАЗНЫЕ): 
          Chicos, Chicas, Niños, Niñas, Amigos, Amigas, Jóvenes, Compañeros, Compañeras, 
          Primos, Primas, Hermanos, Hermanas, Colegas, Chavales, Estudiantes, Muchachos, 
          Muchachas, Vecinos, Vecinas
          
        ДЛЯ ФОРМЫ USTEDES (формальное мн. число):
        • Группы (используй РАЗНЫЕ): 
          Señores, Señoras, Damas, Caballeros, Profesores, Profesoras, Doctores, Doctoras, 
          Ciudadanos, Ciudadanas, Pasajeros, Pasajeras, Distinguidos, Distinguidas, Estimados, 
          Estimadas, Respetables, Honorables, Visitantes, Delegados, Delegadas, Miembros
          
        🌟 ПРИМЕРЫ РАЗНООБРАЗНЫХ КОНТЕКСТОВ (не ограничивайся ими):
        
        • Бытовые ситуации: приготовление пищи, уборка, ремонт
        • В магазине: просьбы о помощи, вопросы о товарах
        • В ресторане: заказ еды, просьбы к официанту
        • В транспорте: просьбы к водителю, пассажирам
        • В школе/университете: задания от учителя
        • На работе: указания коллегам, инструкции
        • В городе: просьба показать дорогу, достопримечательности
        • В экстренных ситуациях: просьба о помощи, инструкции
        • На отдыхе: советы путешественникам, инструкции гида
        • Спорт: указания тренера, правила игры
        • Здоровье: советы врача, рекомендации
        • Технологии: инструкции по использованию устройств
        
        ✳️ РАЗНООБРАЗЬ ГЛАГОЛЫ - используй разные глаголы в разных заданиях, включая:
        • движения (andar, correr, saltar, subir, bajar, girar, etc.)
        • речи (decir, hablar, explicar, contar, responder, preguntar, etc.)
        • мышления (pensar, creer, imaginar, considerar, reflexionar, etc.)
        • чувств (sentir, querer, amar, odiar, desear, esperar, etc.)
        • повседневные (comer, beber, dormir, despertar, ducharse, vestirse, etc.)
        • творчества (escribir, dibujar, pintar, crear, diseñar, construir, etc.)
        
        🎯 ФИНАЛЬНАЯ ПРОВЕРКА ПЕРЕД ОТПРАВКОЙ ЗАДАНИЯ:
        1. Структура предложения ОРИГИНАЛЬНАЯ и НЕ повторяется?
        2. Обращение УНИКАЛЬНОЕ и НЕ повторяется?
        3. Контекст НОВЫЙ и ИНТЕРЕСНЫЙ?
        4. Глагол НЕ повторяется из предыдущих заданий?
        
        Если хотя бы на один вопрос ответ "нет" - полностью переделай задание!
        """
    
    # Особые указания для остальных времен/форм
    elif selected_option in TENSES or selected_option in FORMS:
        special_instructions = """
        ‼️‼️‼️ КРИТИЧЕСКИ ВАЖНО: СОЗДАВАЙ АБСОЛЮТНО УНИКАЛЬНЫЕ ЗАДАНИЯ БЕЗ КАКИХ-ЛИБО ПОВТОРЕНИЙ! ‼️‼️‼️
        
        1️⃣ КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО использовать повторяющиеся шаблоны предложений. 
        Каждое задание должно иметь УНИКАЛЬНУЮ структуру и контекст.
        
        2️⃣ ОБЯЗАТЕЛЬНО ВАРЬИРУЙ СТРУКТУРУ предложений:
        - Начинай предложения по-разному
        - Меняй порядок слов в предложении
        - Используй разную длину предложений
        - Используй разные временные маркеры
        
        3️⃣ ИСПОЛЬЗУЙ РАЗНООБРАЗНЫЕ ТЕМЫ И КОНТЕКСТЫ:
        • Бытовые ситуации: приготовление пищи, уборка, ремонт
        • В магазине, ресторане, транспорте, школе, на работе
        • В городе, на отдыхе, в путешествиях, в спорте
        • Здоровье, технологии, искусство, наука
        
        4️⃣ РАЗНООБРАЗЬ ГЛАГОЛЫ - используй разные глаголы в разных заданиях, включая:
        • движения (andar, correr, saltar, subir, bajar, girar, etc.)
        • речи (decir, hablar, explicar, contar, responder, preguntar, etc.)
        • мышления (pensar, creer, imaginar, considerar, reflexionar, etc.)
        • чувств (sentir, querer, amar, odiar, desear, esperar, etc.)
        • повседневные (comer, beber, dormir, despertar, ducharse, vestirse, etc.)
        • творчества (escribir, dibujar, pintar, crear, diseñar, construir, etc.)
        
        🎯 ФИНАЛЬНАЯ ПРОВЕРКА ПЕРЕД ОТПРАВКОЙ ЗАДАНИЯ:
        1. Структура предложения ОРИГИНАЛЬНАЯ и НЕ повторяется?
        2. Контекст НОВЫЙ и ИНТЕРЕСНЫЙ?
        3. Глагол НЕ повторяется из предыдущих заданий?
        
        Если хотя бы на один вопрос ответ "нет" - полностью переделай задание!
        """
    
    # Делаем несколько попыток, чтобы получить новый глагол
    for attempt in range(max_attempts):
        verb_instruction = ""
        
        # Изменяем тип запроса в зависимости от выбранной темы
        if "Pronombres" in selected_option:
            # Для местоимений не используем глаголы из списка
            selected_verb = None
            verb_instruction = ""
            prompt = f"""
            Создай простое предложение на испанском языке (Castellano, Испания) для тренировки местоимений (притяжательных, указательных, личных и др.).
            
            ВАЖНО: Задание должно быть на правильное использование МЕСТОИМЕНИЯ, а НЕ глагола. Вместо пропуска должно подходить только одно правильное местоимение.
            Добавь в предложение контекст, который чётко определяет необходимость использования конкретного местоимения.
            
            {special_instructions}
            
            Верни ответ строго в формате JSON:
            {{
                "sentence": "полное предложение на испанском",
                "incomplete_sentence": "предложение с пропуском на месте местоимения",
                "verb_infinitive": "основной глагол предложения в инфинитиве (для справки)",
                "tense": "Pronombres (притяжательные и пр.)",
                "correct_form": "правильная форма МЕСТОИМЕНИЯ, которая должна быть в пропуске",
                "explanation": "краткое грамматическое объяснение НА РУССКОМ ЯЗЫКЕ, почему используется это местоимение",
                "translation": "перевод полного предложения на русский язык",
                "word_type": "местоимение",
                "base_word": "базовая форма местоимения",
                "conjugation": {{}}
            }}
            
            Типы местоимений, которые можно использовать:
            1. Притяжательные (mi, tu, su, nuestro, vuestro, su)
            2. Указательные (este, ese, aquel, esta, esa, aquella, etc.)
            3. Личные (yo, tú, él, ella, nosotros, vosotros, ellos, ellas)
            4. Возвратные (me, te, se, nos, os, se)
            5. Вопросительные (qué, quién, cuál, etc.)
            6. Неопределенные (alguien, algo, cualquiera, etc.)
            7. Отрицательные (nada, nadie, ninguno, etc.)
            
            Убедись, что пропуск действительно требует указанного местоимения и подходит только одна форма.
            Предложение должно быть простым и понятным для начинающих/продолжающих изучать испанский язык.
            """
        else:
            # Стандартный запрос для глаголов
            if selected_verb:
                verb_instruction = f'ВАЖНО: В этом задании ОБЯЗАТЕЛЬНО используй глагол "{selected_verb}".'
            else:
                verb_instruction = f"""
                ВАЖНО: Используй разнообразные глаголы! Если возможно, НЕ используй следующие недавно использованные глаголы: {excluded_verbs}.
                Выбери другой, менее распространенный глагол. Старайся использовать глаголы из разных семантических групп 
                (движение, говорение, чувства, действия с предметами, мышление и т.д.).
                """
            
            prompt = f"""
            Создай простое предложение на испанском языке (Castellano, Испания) для тренировки глагола в форме "{selected_option}".
            
            {verb_instruction}
            
            ВАЖНО: Убедись, что задание составлено так, чтобы вместо пропуска подходил лишь один верный вариант слова/фразы.
            Добавь временные маркеры и другие элементы, чётко определяющие необходимость использования нужной видовременной формы.
            
            {special_instructions}
            
            КРИТИЧЕСКИ ВАЖНО:
            1. Объяснение (explanation) должно быть ТОЛЬКО на русском языке
            2. Перевод (translation) должен быть ТОЛЬКО на русский язык
            
            Верни ответ строго в формате JSON:
            {{
                "sentence": "полное предложение на испанском",
                "incomplete_sentence": "предложение с пропуском на месте целевого слова",
                "verb_infinitive": "глагол в инфинитиве",
                "tense": "{selected_option}",
                "correct_form": "правильная форма слова, которая должна быть в пропуске",
                "explanation": "краткое грамматическое объяснение на русском языке, почему используется эта форма",
                "translation": "перевод полного предложения на русский язык",
                "word_type": "тип пропущенного слова (глагол, местоимение, артикль, предлог и т.д.)",
                "base_word": "базовая форма пропущенного слова (например, инфинитив для глаголов или именительный падеж для местоимений)",
                "conjugation": {{
            """
            
            # Добавляем инструкции по формированию спряжений в зависимости от выбранной формы
            if selected_option == "Imperativo":
                prompt += """
                    "tú": "форма императива для tú",
                    "usted": "форма императива для usted",
                    "vosotros": "форма императива для vosotros/as",
                    "ustedes": "форма императива для ustedes"
                }}
                """
            elif selected_option in TENSES:
                prompt += """
                    "yo": "форма для yo в данном времени",
                    "tú": "форма для tú в данном времени",
                    "él": "форма для él/ella/usted в данном времени",
                    "nosotros": "форма для nosotros/as в данном времени",
                    "vosotros": "форма для vosotros/as в данном времени",
                    "ellos": "форма для ellos/ellas/ustedes в данном времени"
                }}
                """
            elif selected_option in FORMS:
                # Для Participio и Gerundio нет спряжений, поэтому просто показываем форму
                prompt += """
                    "form": "корректная форма (participio/gerundio)"
                }}
                """
            else:
                # Для остальных случаев запрашиваем спряжение в настоящем времени
                prompt += """
                    "yo": "форма для yo в Presente de Indicativo",
                    "tú": "форма для tú в Presente de Indicativo",
                    "él": "форма для él/ella/usted в Presente de Indicativo",
                    "nosotros": "форма для nosotros/as в Presente de Indicativo",
                    "vosotros": "форма для vosotros/as в Presente de Indicativo",
                    "ellos": "форма для ellos/ellas/ustedes в Presente de Indicativo"
                }}
                """
            
            prompt += f"""
            }}
            
            Убедись, что пропуск действительно требует указанной формы глагола и подходит только одна форма.
            Предложение должно быть простым и понятным для начинающих/продолжающих изучать испанский язык.
            """
        
        response = get_llm_response(prompt, model)
        if response:
            try:
                # Извлекаем JSON из ответа
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                json_str = response[json_start:json_end]
                
                # Создаем отладочную копию исходного JSON для отслеживания ошибок
                original_json = json_str
                
                # Полная очистка и нормализация JSON
                # 1. Замена одинарных кавычек на двойные
                json_str = json_str.replace("'", '"')
                
                # 2. Исправление случаев, когда после закрывающей кавычки нет запятой перед следующим полем
                json_str = json_str.replace('"\n', '",\n')
                json_str = json_str.replace('"\r\n', '",\r\n')
                
                # 3. Исправление случая, когда после закрывающей кавычки нет запятой перед следующим полем (без переноса)
                json_str = json_str.replace('" ', '", ')
                
                # 4. Исправление случаев неправильной вложенности JSON
                json_str = json_str.replace('}}"', '}}')
                json_str = json_str.replace('""', '"')
                
                # 5. Удаление возможных незакрытых кавычек в конце
                if json_str.endswith('"'):
                    if json_str[-2] != '}':
                        json_str = json_str[:-1]
                
                # 6. Исправление проблем с запятыми в JSON объектах
                # Убираем запятую перед закрывающей скобкой
                json_str = re.sub(r',(\s*)}', r'\1}', json_str)
                
                # 7. Проверка на пропущенные запятые между значениями полей
                # например: "field1": "value1" "field2": "value2"
                json_str = re.sub(r'("(?:[^"\\]|\\.)*")\s+("(?:[^"\\]|\\.)*")', r'\1, \2', json_str)
                
                # Альтернативная проверка: если мы все еще не можем разобрать JSON, 
                # попробуем регулярное выражение для извлечения нужных полей
                try:
                    exercise = json.loads(json_str)
                except Exception as json_parse_error:
                    # Отладочная информация
                    # st.error(f"Не удалось разобрать JSON: {str(json_parse_error)}")
                    # st.write("Оригинальный JSON:", original_json)
                    # st.write("Исправленный JSON:", json_str)
                    
                    # Запасной вариант - использование регулярных выражений для извлечения ключевых полей
                    try:
                        # Извлекаем основные поля из ответа с помощью regex
                        exercise = {}
                        
                        # Расширенные паттерны для извлечения основных полей с большей гибкостью
                        # Эти паттерны теперь работают с кавычками разных типов и разными форматами
                        patterns = {
                            "sentence": r'["\']sentence["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "incomplete_sentence": r'["\']incomplete_sentence["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "verb_infinitive": r'["\']verb_infinitive["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "tense": r'["\']tense["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "correct_form": r'["\']correct_form["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "explanation": r'["\']explanation["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "translation": r'["\']translation["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "word_type": r'["\']word_type["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "base_word": r'["\']base_word["\'][\s]*:[\s]*["\']([^"\']+)["\']'
                        }
                        
                        # Расширенная логика извлечения полей
                        for field, pattern in patterns.items():
                            match = re.search(pattern, response, re.IGNORECASE)
                            if match:
                                exercise[field] = match.group(1)
                            else:
                                # Попробуем более общий паттерн без кавычек
                                alt_pattern = f'["\']?{field}["\']?\\s*:\\s*["\']?([^,"\'}}]+)["\']?'
                                match = re.search(alt_pattern, response, re.IGNORECASE)
                                if match:
                                    exercise[field] = match.group(1).strip()
                                else:
                                    # Если поле не найдено, используем значения по умолчанию
                                    if field == "word_type":
                                        exercise[field] = "глагол"
                                    elif field == "base_word" and "verb_infinitive" in exercise:
                                        exercise[field] = exercise["verb_infinitive"]
                                    elif field == "tense" and selected_option:
                                        exercise[field] = selected_option
                                    else:
                                        exercise[field] = ""
                        
                        # Создаем пустой объект спряжения в качестве запасного варианта
                        exercise["conjugation"] = {}
                        
                        # Пытаемся извлечь формы спряжения для дополнительной информации
                        conjugation_patterns = {
                            "yo": r'["\']yo["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "tú": r'["\']tú["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "él": r'["\'](él|el)["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "nosotros": r'["\']nosotros["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "vosotros": r'["\']vosotros["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "ellos": r'["\']ellos["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "form": r'["\']form["\'][\s]*:[\s]*["\']([^"\']+)["\']'
                        }
                        
                        for form, pattern in conjugation_patterns.items():
                            match = re.search(pattern, response, re.IGNORECASE)
                            if match:
                                if form == "él" and len(match.groups()) > 1:
                                    exercise["conjugation"][form] = match.group(2)  # В этом паттерне два захвата
                                else:
                                    exercise["conjugation"][form] = match.group(1)
                        
                        # Дополнительные поля для Imperativo
                        imperativo_patterns = {
                            "usted": r'["\']usted["\'][\s]*:[\s]*["\']([^"\']+)["\']',
                            "ustedes": r'["\']ustedes["\'][\s]*:[\s]*["\']([^"\']+)["\']'
                        }
                        
                        if "Imperativo" in response:
                            for form, pattern in imperativo_patterns.items():
                                match = re.search(pattern, response, re.IGNORECASE)
                                if match:
                                    exercise["conjugation"][form] = match.group(1)
                        
                        # Создаем пустой объект спряжения в качестве запасного варианта
                        exercise["conjugation"] = {}
                        
                        # Проверяем, есть ли минимально необходимые поля
                        required_fields = ["sentence", "incomplete_sentence", "verb_infinitive", "correct_form"]
                        missing_fields = [field for field in required_fields if not exercise.get(field)]
                        
                        if not missing_fields:
                            # Все обязательные поля найдены
                            # Сообщение убрано, чтобы не показывать пользователю техническую информацию
                            pass
                        else:
                            # Если не хватает полей, попробуем сгенерировать их
                            if "sentence" in missing_fields and "incomplete_sentence" in exercise and "correct_form" in exercise:
                                # Восстанавливаем полное предложение из неполного + правильной формы
                                exercise["sentence"] = exercise["incomplete_sentence"].replace("...", exercise["correct_form"])
                            
                            if "incomplete_sentence" in missing_fields and "sentence" in exercise and "correct_form" in exercise:
                                # Восстанавливаем неполное предложение из полного, заменяя правильную форму на ...
                                exercise["incomplete_sentence"] = exercise["sentence"].replace(exercise["correct_form"], "...")
                            
                            # После восстановления проверяем еще раз
                            missing_fields = [field for field in ["sentence", "incomplete_sentence"] if not exercise.get(field)]
                            
                            if "verb_infinitive" in missing_fields:
                                # Если все еще не хватает глагола, используем заглушку
                                exercise["verb_infinitive"] = "usar"  # Базовый глагол в качестве заглушки
                            
                            if "correct_form" in missing_fields:
                                # Если все еще не хватает корректной формы, используем выделенный текст
                                # Это может не сработать, но лучше, чем ничего
                                form_matches = re.findall(r'["\']([^"\']+)["\'][\s]*(?:es la forma correcta|should be used|es la respuesta correcta)', response)
                                if form_matches:
                                    exercise["correct_form"] = form_matches[0]
                            
                            # Последняя проверка на наличие критичных полей
                            if not exercise.get("sentence") or not exercise.get("incomplete_sentence"):
                                raise Exception(f"Не удалось восстановить обязательные поля. Отсутствуют: {', '.join(missing_fields)}")
                            
                            # Не показываем техническое предупреждение пользователю
                            pass
                        
                    except Exception as regex_error:
                        # Если даже регулярные выражения не помогли, возвращаем ошибку
                        st.error(f"Не удалось извлечь данные из ответа: {str(regex_error)}")
                        # Предоставим дополнительную информацию для отладки
                        # st.write("Получен ответ:", response[:500] + ("..." if len(response) > 500 else ""))
                        if attempt == max_attempts - 1:
                            return None
                        continue
                
                # Если глагол был выбран из списка, убедимся что он используется
                if selected_verb and exercise['verb_infinitive'] != selected_verb:
                    if attempt < max_attempts - 1:
                        continue
                
                # Проверяем, не был ли этот глагол недавно использован
                if exercise['verb_infinitive'] not in st.session_state.used_verbs:
                    # Добавляем глагол в историю использованных глаголов
                    st.session_state.used_verbs.append(exercise['verb_infinitive'])
                    # Ограничиваем список 20 последними глаголами
                    if len(st.session_state.used_verbs) > 20:
                        st.session_state.used_verbs = st.session_state.used_verbs[-20:]
                    return exercise
                elif attempt == max_attempts - 1:
                    # Если это последняя попытка, возвращаем упражнение, даже если глагол повторяется
                    return exercise
            except Exception as e:
                st.error(f"Ошибка при обработке ответа: {str(e)}")
                if attempt == max_attempts - 1:
                    return None
    return None

def check_answer(user_input, correct_answer):
    """Проверяет ответ пользователя с учетом игнорирования акцентов и ñ"""
    if not user_input or not correct_answer:
        return False
        
    # Нормализация строк для сравнения
    user_norm = normalize_spanish_text(user_input.strip().lower())
    correct_norm = normalize_spanish_text(correct_answer.strip().lower())
    
    return user_norm == correct_norm

def generate_audio(text, voice_id):
    """Генерирует аудио с помощью Elevenlabs API напрямую через requests"""
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Ошибка API ElevenLabs: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Ошибка при генерации аудио: {str(e)}")
        return None

def autoplay_audio(audio_data):
    """Воспроизводит аудио автоматически с помощью HTML-элемента audio"""
    b64 = base64.b64encode(audio_data).decode()
    md = f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

def toggle_settings():
    """Переключает видимость настроек"""
    st.session_state.show_settings = not st.session_state.show_settings

def apply_settings_and_generate():
    """Обработчик нажатия кнопки применения настроек"""
    st.session_state.show_settings = False
    st.session_state.needs_new_exercise = True

def next_exercise_callback():
    """Обработчик нажатия кнопки 'Далее'"""
    st.session_state.needs_new_exercise = True
    # Очищаем поле ввода при переходе к новому заданию
    st.session_state.user_answer = ""

# Генерация упражнения при первом запуске или флаге needs_new_exercise
if not st.session_state.current_exercise or st.session_state.needs_new_exercise:
    st.session_state.needs_new_exercise = False
    with st.spinner("Генерируем задание..."):
        st.session_state.current_exercise = generate_exercise(st.session_state.selected_model)
        st.session_state.user_answer = ""
        st.session_state.submitted = False
        st.session_state.correct = None
        st.session_state.show_translation = False
        st.session_state.audio_ready = False
        st.session_state.audio_data = None

# Если упражнение загружено, отображаем его
if st.session_state.current_exercise:
    exercise = st.session_state.current_exercise
    
    # Получаем информацию о типе пропущенного слова
    word_type = exercise.get('word_type', 'глагол')
    base_word = exercise.get('base_word', exercise['verb_infinitive'])
    
    # Формируем заголовок задания в зависимости от типа пропущенного слова
    if (word_type == "глагол" or word_type == "verbo" or word_type.lower() == "verb" or 
        word_type == "глагол в нужной форме"):
        instruction_header = f"### Вставьте пропущенный глагол <span style='color:red; font-weight:700;'>{base_word.upper()}</span> в нужной форме"
    elif (word_type == "местоимение" or word_type == "pronombre" or 
          word_type.lower() == "pronoun" or "Pronombres" in exercise.get('tense', '')):
        # Для местоимений показываем только базовый заголовок без конкретных слов
        instruction_header = f"### Вставьте пропущенное местоимение"
    else:
        # Для всех остальных случаев используем глагол по умолчанию
        instruction_header = f"### Вставьте пропущенный глагол <span style='color:red; font-weight:700;'>{base_word.upper()}</span> в нужной форме"
    
    # Отображаем заголовок задания
    st.markdown(instruction_header, unsafe_allow_html=True)
    
    # Проверяем, был ли уже отправлен ответ
    if st.session_state.submitted:
        # Показываем предложение с подставленным правильным ответом
        complete_sentence = exercise['incomplete_sentence'].replace('...', f'**{exercise["correct_form"]}**')
        st.markdown(f"**{complete_sentence}**")
    else:
        # Отображение предложения с пропуском
        st.markdown(f"**{exercise['incomplete_sentence']}**")
    
    # Поле ввода ответа
    user_input = st.text_input(
        "Введите пропущенное слово:",
        value="" if st.session_state.needs_new_exercise else st.session_state.user_answer,
        key="answer_input",
        disabled=st.session_state.submitted
    )
    
    # Кнопки
    col1, col2 = st.columns(2)
    
    with col1:
        check_button = st.button(
            "Проверить",
            disabled=st.session_state.submitted,
            use_container_width=True
        )
    
    with col2:
        translate_button = st.button(
            "Подробнее",
            use_container_width=True
        )
    
    # Проверка ответа
    if check_button:
        st.session_state.user_answer = user_input
        st.session_state.submitted = True
        st.session_state.correct = check_answer(user_input, exercise['correct_form'])
        
        # Отмечаем, что аудио еще не готово
        st.session_state.audio_ready = False
        st.session_state.audio_data = None
        
        # Перезагружаем страницу для отображения результатов
        # st.rerun()  # Закомментируем, чтобы не терять контекст
    
    # Отображение результатов проверки
    if st.session_state.submitted:
        if st.session_state.correct:
            st.success("✅ Правильно!")
        else:
            st.error(f"❌ Неправильно. Верный ответ: **{exercise['correct_form']}**")
            st.info(f"**Объяснение:** {exercise['explanation']}")
    
    # Отображение перевода и дополнительной информации
    if translate_button:
        st.session_state.show_translation = True
    
    if st.session_state.show_translation:
        # Отображаем перевод и форму
        st.info(f"""
        **Перевод:** {exercise['translation']}
        
        **Форма:** {exercise['tense']}
        """)
        
        # Проверяем, если объяснение на испанском, попробуем автоматически перевести его
        explanation = exercise.get('explanation', '')
        if explanation and any(word in explanation.lower() for word in ['se utiliza', 'porque', 'para', 'cuando', 'como', 'el pronombre']):
            # Скорее всего, объяснение на испанском - добавим предупреждение
            st.warning(f"**Примечание:** Объяснение может быть на испанском языке: {explanation}")
            # Также можно было бы здесь добавить автоматический перевод, но это потребовало бы дополнительного API
        
        # Отображаем таблицу спряжения с использованием HTML только для глаголов
        try:
            conjugation = exercise.get('conjugation', {})
            # Инициализируем html_table со значением по умолчанию
            html_table = ""
            
            # Проверяем, что это упражнение не на местоимения 
            if ("Pronombres" not in exercise.get('tense', '') and 
                word_type not in ["местоимение", "pronombre", "pronoun"]):
                
                # Формируем заголовок таблицы в зависимости от времени/формы
                if exercise['tense'] == "Imperativo":
                    table_title = f"Спряжение глагола {exercise['verb_infinitive']} (Imperativo):"
                    
                    # Получаем формы из словаря conjugation или используем формы по умолчанию
                    tu_form = conjugation.get('tú', '-')
                    usted_form = conjugation.get('usted', '-')
                    vosotros_form = conjugation.get('vosotros', '-')
                    ustedes_form = conjugation.get('ustedes', '-')
                    
                    # Если все формы пустые, попробуем сгенерировать их
                    if tu_form == '-' and usted_form == '-' and vosotros_form == '-' and ustedes_form == '-':
                        # Определяем окончание и основу глагола
                        verb = exercise['verb_infinitive']
                        ending = verb[-2:] if len(verb) > 2 else ""
                        stem = verb[:-2] if len(verb) > 2 else verb
                        
                        # Правила для образования повелительного наклонения
                        if ending == "ar":
                            tu_form = f"{stem}a"
                            usted_form = f"{stem}e"
                            vosotros_form = f"{stem}ad"
                            ustedes_form = f"{stem}en"
                        elif ending in ["er", "ir"]:
                            tu_form = f"{stem}e"
                            usted_form = f"{stem}a"
                            vosotros_form = f"{stem}{ending[0]}d"
                            ustedes_form = f"{stem}an"
                    
                    html_table = f"""
                    <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                        <h4 style="margin-top: 0;">{table_title}</h4>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>tú</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{tu_form}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>usted</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{usted_form}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>vosotros/as</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{vosotros_form}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px;"><strong>ustedes</strong></td>
                                <td style="padding: 8px;">{ustedes_form}</td>
                            </tr>
                        </table>
                    </div>
                    """
                elif exercise['tense'] in FORMS:
                    if 'form' in conjugation:
                        html_table = f"""
                        <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                            <h4 style="margin-top: 0;">Форма глагола {exercise['verb_infinitive']} ({exercise['tense']}):</h4>
                            <p style="font-size: 16px; padding: 8px;">{conjugation.get('form', '-')}</p>
                        </div>
                        """
                    else:
                        html_table = f"""
                        <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                            <h4 style="margin-top: 0;">Форма глагола {exercise['verb_infinitive']} ({exercise['tense']}):</h4>
                            <p style="font-size: 16px; padding: 8px;">Информация отсутствует</p>
                        </div>
                        """
                else:
                    table_title = f"Спряжение глагола {exercise['verb_infinitive']} ({exercise['tense']}):"
                    
                    # Проверяем, содержит ли словарь спряжения какие-либо значения
                    if conjugation and any(conjugation.values()):
                        html_table = f"""
                        <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                            <h4 style="margin-top: 0;">{table_title}</h4>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>yo</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('yo', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>tú</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('tú', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>él/ella/usted</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('él', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>nosotros/as</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('nosotros', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>vosotros/as</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('vosotros', '-')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px;"><strong>ellos/ellas/ustedes</strong></td>
                                    <td style="padding: 8px;">{conjugation.get('ellos', '-')}</td>
                                </tr>
                            </table>
                        </div>
                        """
                    else:
                        # Используем базовую таблицу с формами по умолчанию
                        # Генерируем базовые формы
                        verb = exercise['verb_infinitive']
                        ending = verb[-2:] if len(verb) > 2 else ""
                        stem = verb[:-2] if len(verb) > 2 else verb
                        
                        if exercise['tense'] == "Presente":
                            # Разные окончания в зависимости от типа глагола
                            if ending == "ar":
                                forms = {
                                    "yo": f"{stem}o",
                                    "tú": f"{stem}as",
                                    "él": f"{stem}a",
                                    "nosotros": f"{stem}amos",
                                    "vosotros": f"{stem}áis",
                                    "ellos": f"{stem}an"
                                }
                            elif ending == "er":
                                forms = {
                                    "yo": f"{stem}o",
                                    "tú": f"{stem}es",
                                    "él": f"{stem}e",
                                    "nosotros": f"{stem}emos",
                                    "vosotros": f"{stem}éis",
                                    "ellos": f"{stem}en"
                                }
                            elif ending == "ir":
                                forms = {
                                    "yo": f"{stem}o",
                                    "tú": f"{stem}es",
                                    "él": f"{stem}e",
                                    "nosotros": f"{stem}imos",
                                    "vosotros": f"{stem}ís",
                                    "ellos": f"{stem}en"
                                }
                            else:
                                # Если не удалось определить тип глагола
                                forms = {
                                    "yo": "-",
                                    "tú": "-",
                                    "él": "-",
                                    "nosotros": "-",
                                    "vosotros": "-",
                                    "ellos": "-"
                                }
                        elif exercise['tense'] == "Imperativo":
                            # Правила для образования повелительного наклонения
                            if ending == "ar":
                                forms = {
                                    "tú": f"{stem}a",
                                    "él": f"{stem}e",
                                    "nosotros": f"{stem}emos",
                                    "vosotros": f"{stem}ad",
                                    "ellos": f"{stem}en"
                                }
                            elif ending in ["er", "ir"]:
                                forms = {
                                    "tú": f"{stem}e",
                                    "él": f"{stem}a",
                                    "nosotros": f"{stem}amos",
                                    "vosotros": f"{stem}{ending[0]}d",
                                    "ellos": f"{stem}an"
                                }
                            else:
                                forms = {
                                    "tú": "-",
                                    "él": "-",
                                    "nosotros": "-",
                                    "vosotros": "-",
                                    "ellos": "-"
                                }
                        elif exercise['tense'] == "Pretérito indefinido (perfecto simple)":
                            # Правила для образования простого прошедшего времени
                            if ending == "ar":
                                forms = {
                                    "yo": f"{stem}é",
                                    "tú": f"{stem}aste",
                                    "él": f"{stem}ó",
                                    "nosotros": f"{stem}amos",
                                    "vosotros": f"{stem}asteis",
                                    "ellos": f"{stem}aron"
                                }
                            elif ending in ["er", "ir"]:
                                forms = {
                                    "yo": f"{stem}í",
                                    "tú": f"{stem}iste",
                                    "él": f"{stem}ió",
                                    "nosotros": f"{stem}imos",
                                    "vosotros": f"{stem}isteis",
                                    "ellos": f"{stem}ieron"
                                }
                            else:
                                forms = {
                                    "yo": "-",
                                    "tú": "-",
                                    "él": "-",
                                    "nosotros": "-",
                                    "vosotros": "-",
                                    "ellos": "-"
                                }
                        elif exercise['tense'] == "Pretérito imperfecto":
                            # Правила для образования имперфекта
                            if ending == "ar":
                                forms = {
                                    "yo": f"{stem}aba",
                                    "tú": f"{stem}abas",
                                    "él": f"{stem}aba",
                                    "nosotros": f"{stem}ábamos",
                                    "vosotros": f"{stem}abais",
                                    "ellos": f"{stem}aban"
                                }
                            elif ending in ["er", "ir"]:
                                forms = {
                                    "yo": f"{stem}ía",
                                    "tú": f"{stem}ías",
                                    "él": f"{stem}ía",
                                    "nosotros": f"{stem}íamos",
                                    "vosotros": f"{stem}íais",
                                    "ellos": f"{stem}ían"
                                }
                            else:
                                forms = {
                                    "yo": "-",
                                    "tú": "-",
                                    "él": "-",
                                    "nosotros": "-",
                                    "vosotros": "-",
                                    "ellos": "-"
                                }
                        elif exercise['tense'] == "Futuro simple":
                            # Правила для образования будущего времени
                            # Futuro добавляет окончания к инфинитиву
                            forms = {
                                "yo": f"{verb}é",
                                "tú": f"{verb}ás",
                                "él": f"{verb}á",
                                "nosotros": f"{verb}emos",
                                "vosotros": f"{verb}éis",
                                "ellos": f"{verb}án"
                            }
                        elif exercise['tense'] == "Pretérito perfecto compuesto":
                            # Образование Pretérito perfecto compuesto: haber en presente + participio
                            if ending == "ar":
                                participio = f"{stem}ado"
                            elif ending in ["er", "ir"]:
                                participio = f"{stem}ido"
                            else:
                                participio = "-"
                                
                            forms = {
                                "yo": f"he {participio}",
                                "tú": f"has {participio}",
                                "él": f"ha {participio}",
                                "nosotros": f"hemos {participio}",
                                "vosotros": f"habéis {participio}",
                                "ellos": f"han {participio}"
                            }
                        elif exercise['tense'] == "Futuro compuesto":
                            # Образование Futuro compuesto: haber en futuro + participio
                            if ending == "ar":
                                participio = f"{stem}ado"
                            elif ending in ["er", "ir"]:
                                participio = f"{stem}ido"
                            else:
                                participio = "-"
                                
                            forms = {
                                "yo": f"habré {participio}",
                                "tú": f"habrás {participio}",
                                "él": f"habrá {participio}",
                                "nosotros": f"habremos {participio}",
                                "vosotros": f"habréis {participio}",
                                "ellos": f"habrán {participio}"
                            }
                        elif exercise['tense'] == "Gerundio":
                            # Правила для образования герундия
                            if ending == "ar":
                                forms = {"form": f"{stem}ando"}
                            elif ending in ["er", "ir"]:
                                forms = {"form": f"{stem}iendo"}
                            else:
                                forms = {"form": "-"}
                        elif exercise['tense'] == "Participio":
                            # Правила для образования причастия
                            if ending == "ar":
                                forms = {"form": f"{stem}ado"}
                            elif ending in ["er", "ir"]:
                                forms = {"form": f"{stem}ido"}
                            else:
                                forms = {"form": "-"}
                        else:
                            # Для других времен просто используем заглушки
                            forms = {
                                "yo": "-",
                                "tú": "-",
                                "él": "-",
                                "nosotros": "-",
                                "vosotros": "-",
                                "ellos": "-"
                            }
                            
                        # Создаем HTML-таблицу из сгенерированных форм
                        if 'form' in forms:
                            # Для Gerundio и Participio
                            html_table = f"""
                            <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                                <h4 style="margin-top: 0;">Форма глагола {exercise['verb_infinitive']} ({exercise['tense']}):</h4>
                                <p style="font-size: 16px; padding: 8px;">{forms.get('form', '-')}</p>
                            </div>
                            """
                        elif exercise['tense'] == "Imperativo":
                            # Для Imperativo
                            html_table = f"""
                            <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                                <h4 style="margin-top: 0;">{table_title}</h4>
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>tú</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('tú', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>usted</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('él', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>vosotros/as</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('vosotros', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px;"><strong>ustedes</strong></td>
                                        <td style="padding: 8px;">{forms.get('ellos', '-')}</td>
                                    </tr>
                                </table>
                            </div>
                            """
                        else:
                            # Для всех остальных времён
                            html_table = f"""
                            <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                                <h4 style="margin-top: 0;">{table_title}</h4>
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>yo</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('yo', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>tú</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('tú', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>él/ella/usted</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('él', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>nosotros/as</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('nosotros', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>vosotros/as</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{forms.get('vosotros', '-')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px;"><strong>ellos/ellas/ustedes</strong></td>
                                        <td style="padding: 8px;">{forms.get('ellos', '-')}</td>
                                    </tr>
                                </table>
                            </div>
                            """
                
                st.markdown(html_table, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Ошибка при отображении спряжений: {str(e)}")
    
    # Кнопки "Озвучить" и "Далее"
    col3, col4 = st.columns(2)
    
    with col3:
        if st.session_state.submitted:
            # Показываем кнопку озвучивания
            audio_button = st.button(
                "🔊 Озвучить",
                use_container_width=True
            )
            
            # Генерируем аудио только при нажатии на кнопку
            if audio_button:
                with st.spinner("Подготовка аудио..."):
                    try:
                        # Генерируем аудио при нажатии на кнопку
                        sentence_to_speak = exercise['sentence']
                        audio_data = generate_audio(
                            sentence_to_speak,
                            st.session_state.voice_id
                        )
                        if audio_data:
                            # Сохраняем для возможного повторного использования
                            st.session_state.audio_data = audio_data
                            st.session_state.audio_ready = True
                            # Отображаем аудио с автовоспроизведением
                            autoplay_audio(audio_data)
                        else:
                            st.error("Не удалось сгенерировать аудио.")
                    except Exception as e:
                        st.error(f"Ошибка при генерации аудио: {str(e)}")
            
            # Если аудио уже было сгенерировано, показываем его без автовоспроизведения
            elif st.session_state.audio_ready and st.session_state.audio_data:
                st.audio(st.session_state.audio_data, format="audio/mpeg")

        with col4:
            next_button = st.button(
                "Далее ➡️",
                use_container_width=True,
                on_click=next_exercise_callback
            )

# Обработка случая, когда упражнение не загружено
else:
    if not st.session_state.show_settings:  # Показываем сообщение только если не в режиме настроек
        st.warning("Не удалось загрузить упражнение. Пожалуйста, попробуйте еще раз.")
        st.button("Попробовать снова", key="retry_btn", on_click=next_exercise_callback)

# Кнопка для отображения/скрытия настроек внизу страницы
st.markdown("---")
settings_button = st.button("⚙️ Настройки", on_click=toggle_settings)

# Настройки (показываются только при нажатии на кнопку)
if st.session_state.show_settings:
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Настройки приложения")
    
    # Времена (Tenses)
    col_tenses1, col_tenses2 = st.columns(2)
    
    # Добавляем кнопку выбора всех галочек
    select_all = st.checkbox("Выбрать все", value=True, key="select_all")
    
    # Обновляем состояние всех чекбоксов при изменении select_all
    if select_all:
        for tense in TENSES + FORMS + ['Pronombres', 'Paráfrasis']:
            st.session_state.selected_topics[tense] = True
    else:
        for tense in TENSES + FORMS + ['Pronombres', 'Paráfrasis']:
            st.session_state.selected_topics[tense] = False
    
    with col_tenses1:
        for tense in TENSES[:len(TENSES)//2 + len(TENSES)%2]:
            st.session_state.selected_topics[tense] = st.checkbox(
                tense, 
                value=st.session_state.selected_topics.get(tense, True),
                key=f"check_{tense}"
            )
    with col_tenses2:
        for tense in TENSES[len(TENSES)//2 + len(TENSES)%2:]:
            st.session_state.selected_topics[tense] = st.checkbox(
                tense, 
                value=st.session_state.selected_topics.get(tense, True),
                key=f"check_{tense}"
            )
    
    # Формы (Forms)
    col_forms1, col_forms2 = st.columns(2)
    with col_forms1:
        st.session_state.selected_topics['Participio'] = st.checkbox(
            'Participio',
            value=st.session_state.selected_topics.get('Participio', True),
            key="check_Participio"
        )
    with col_forms2:
        st.session_state.selected_topics['Gerundio'] = st.checkbox(
            'Gerundio',
            value=st.session_state.selected_topics.get('Gerundio', True),
            key="check_Gerundio"
        )
    
    # Другое
    col_other1, col_other2 = st.columns(2)
    with col_other1:
        st.session_state.selected_topics['Pronombres'] = st.checkbox(
            'Pronombres (местоимения)',
            value=st.session_state.selected_topics.get('Pronombres', True),
            key="check_Pronouns"
        )
    with col_other2:
        st.session_state.selected_topics['Paráfrasis'] = st.checkbox(
            'Paráfrasis (конструкции)',
            value=st.session_state.selected_topics.get('Paráfrasis', True),
            key="check_Paraphrasis"
        )
    
    st.markdown("---")
    
    # Выбор LLM модели
    model_option = st.radio(
        "Выберите LLM модель:",
        options=["claude-haiku", "claude-3.7-sonnet", "claude-opus", "gpt-4o", "gpt-4o-mini"],
        index=["claude-haiku", "claude-3.7-sonnet", "claude-opus", "gpt-4o", "gpt-4o-mini"].index(st.session_state.selected_model),
        format_func=lambda x: {
            "claude-haiku": "Claude 3 Haiku", 
            "claude-3.7-sonnet": "Claude 3.7 Sonnet", 
            "claude-opus": "Claude 3 Opus", 
            "gpt-4o": "GPT-4o", 
            "gpt-4o-mini": "GPT-4o mini"
        }[x],
        horizontal=True
    )
    if model_option != st.session_state.selected_model:
        st.session_state.selected_model = model_option
    
    # Выбор голоса для озвучивания
    voice_option = st.radio(
        "Выберите голос для озвучивания:",
        options=["Jhenny Antiques", "Benjamin"],
        index=0 if st.session_state.selected_voice == "Jhenny Antiques" else 1,
        horizontal=True
    )
    if voice_option != st.session_state.selected_voice:
        st.session_state.selected_voice = voice_option
    
    # Карта ID голосов Elevenlabs
    voice_id_map = {
        "Jhenny Antiques": "2Lb1en5ujrODDIqmp7F3",
        "Benjamin": "LruHrtVF6PSyGItzMNHS"
    }
    st.session_state.voice_id = voice_id_map[st.session_state.selected_voice]

    # Кнопка для применения настроек и генерации нового упражнения
    st.button(
        "Применить настройки и получить новое задание", 
        use_container_width=True, 
        on_click=apply_settings_and_generate,
        key="apply_settings"
    )
    
    st.markdown('</div>', unsafe_allow_html=True) 