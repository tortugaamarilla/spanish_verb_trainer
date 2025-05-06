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

# Скрываем стандартные элементы Streamlit
st.set_page_config(
    page_title="Тренажёр испанских глаголов",
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

# Настройка сессионных переменных
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = {}
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
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
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "claude"
if 'selected_voice' not in st.session_state:
    st.session_state.selected_voice = "Jhenny Antiques"
if 'voice_id' not in st.session_state:
    st.session_state.voice_id = "2Lb1en5ujrODDIqmp7F3"  # ID для Jhenny Antiques по умолчанию
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
if 'needs_new_exercise' not in st.session_state:
    st.session_state.needs_new_exercise = False
if 'used_verbs' not in st.session_state:
    st.session_state.used_verbs = []  # Список для отслеживания недавно использованных глаголов

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

def get_llm_response(prompt, model="claude"):
    """Получает ответ от выбранной LLM модели"""
    try:
        if model == "claude":
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        elif model == "gpt":
            client = openai.OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
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

def generate_exercise(model="claude", max_attempts=3):
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
        prompt = f"""
        Создай простое предложение на испанском языке (Castellano, Испания) для тренировки глагола в форме "{selected_option}".
        
        ВАЖНО: Используй разнообразные глаголы! Если возможно, НЕ используй следующие недавно использованные глаголы: {excluded_verbs}.
        Выбери другой, менее распространенный глагол. Старайся использовать глаголы из разных семантических групп 
        (движение, говорение, чувства, действия с предметами, мышление и т.д.).
        
        ВАЖНО: Убедись, что задание составлено так, чтобы вместо пропуска подходил лишь один верный вариант слова/фразы.
        Добавь временные маркеры и другие элементы, чётко определяющие необходимость использования нужной видовременной формы.
        
        {special_instructions}
        
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
                exercise = json.loads(json_str)
                
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

# Основной интерфейс
st.title("Тренажёр испанских глаголов 🇪🇸")

# Генерация упражнения при первом запуске или флаге needs_new_exercise
if not st.session_state.current_exercise or st.session_state.needs_new_exercise:
    with st.spinner("Генерируем задание..."):
        st.session_state.current_exercise = generate_exercise(st.session_state.selected_model)
        st.session_state.user_answer = ""
        st.session_state.submitted = False
        st.session_state.correct = None
        st.session_state.show_translation = False
        st.session_state.audio_ready = False
        st.session_state.audio_data = None
        st.session_state.needs_new_exercise = False

# Если упражнение загружено, отображаем его
if st.session_state.current_exercise:
    exercise = st.session_state.current_exercise
    
    # Получаем информацию о типе пропущенного слова
    word_type = exercise.get('word_type', 'глагол')
    base_word = exercise.get('base_word', exercise['verb_infinitive'])
    
    # Формируем заголовок задания в зависимости от типа пропущенного слова
    if word_type == "глагол":
        instruction_header = f"### Вставьте пропущенный глагол {base_word.upper()} в нужной форме"
    elif word_type == "местоимение":
        instruction_header = f"### Вставьте пропущенное местоимение"
    elif word_type == "артикль":
        instruction_header = f"### Вставьте пропущенный артикль"
    elif word_type == "предлог":
        instruction_header = f"### Вставьте пропущенный предлог"
    else:
        instruction_header = f"### Вставьте пропущенное слово ({word_type})"
    
    # Отображаем заголовок задания
    st.markdown(instruction_header)
    
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
        "Введите форму глагола:",
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
        
        # Отображаем таблицу спряжения с использованием HTML
        try:
            conjugation = exercise.get('conjugation', {})
            if conjugation:
                # Формируем заголовок таблицы в зависимости от времени/формы
                if exercise['tense'] == "Imperativo":
                    table_title = f"Спряжение глагола {exercise['verb_infinitive']} (Imperativo):"
                    
                    html_table = f"""
                    <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-top: 10px; margin-bottom: 20px;">
                        <h4 style="margin-top: 0;">{table_title}</h4>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>tú</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('tú', '-')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>usted</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('usted', '-')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>vosotros/as</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{conjugation.get('vosotros', '-')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px;"><strong>ustedes</strong></td>
                                <td style="padding: 8px;">{conjugation.get('ustedes', '-')}</td>
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
                        html_table = ""
                else:
                    table_title = f"Спряжение глагола {exercise['verb_infinitive']} ({exercise['tense']}):"
                    
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
                
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                # Запасной вариант, если нет данных о спряжении в новом формате
                conjugation_text = exercise.get('conjugation_table', 'Информация о спряжении недоступна')
                st.info(f"**Спряжение глагола {exercise['verb_infinitive']}:**\n\n{conjugation_text}")
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
        options=["claude", "gpt"],
        index=0 if st.session_state.selected_model == "claude" else 1,
        format_func=lambda x: "Claude 3 Opus" if x == "claude" else "GPT-4o",
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