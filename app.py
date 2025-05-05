import streamlit as st
import requests
import json
import time
import random
import anthropic
import openai
import elevenlabs
from elevenlabs.client import ElevenLabs

# Настройка страницы
st.set_page_config(
    page_title="Тренажёр испанских глаголов",
    page_icon="🇪🇸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Добавление CSS для адаптации под мобильные устройства
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

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

# Список времён и конструкций для тренировки
TENSES = [
    "Presente",
    "Pretérito indefinido (perfecto simple)",
    "Pretérito imperfecto",
    "Pretérito perfecto compuesto",
    "Futuro simple",
    "Futuro compuesto"
]

FORMS = [
    "Participio",
    "Gerundio"
]

CONSTRUCTIONS = [
    "Estar + gerundio",
    "Ir a + infinitivo",
    "Acabar de + infinitivo",
    "Tener que + infinitivo",
    "Deber + infinitivo",
    "Poder + infinitivo",
    "Volver a + infinitivo",
    "Pronombres (притяжательные и пр.)"
]

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

def generate_exercise(model="claude"):
    """Генерирует новое упражнение с использованием выбранной модели LLM"""
    # Выбираем случайное время или конструкцию
    all_options = TENSES + FORMS + CONSTRUCTIONS
    selected_option = random.choice(all_options)
    
    prompt = f"""
    Создай простое предложение на испанском языке (Castellano, Испания) для тренировки глагола в форме "{selected_option}".
    
    Верни ответ строго в формате JSON:
    {{
        "sentence": "полное предложение на испанском",
        "incomplete_sentence": "предложение с пропуском на месте целевого глагола",
        "verb_infinitive": "глагол в инфинитиве",
        "tense": "{selected_option}",
        "correct_form": "правильная форма глагола, которая должна быть в пропуске",
        "explanation": "краткое грамматическое объяснение, почему используется эта форма",
        "translation": "перевод полного предложения на русский язык"
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
            return exercise
        except Exception as e:
            st.error(f"Ошибка при обработке ответа: {str(e)}")
            return None
    return None

def check_answer(user_input, correct_answer):
    """Проверяет ответ пользователя"""
    # Нормализация строк для сравнения
    user_norm = user_input.strip().lower()
    correct_norm = correct_answer.strip().lower()
    return user_norm == correct_norm

def generate_audio(text, voice_id):
    """Генерирует аудио с помощью Elevenlabs API"""
    try:
        audio = elevenlabs_client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        return audio.content
    except Exception as e:
        st.error(f"Ошибка при генерации аудио: {str(e)}")
        return None

def next_exercise():
    """Переход к следующему упражнению"""
    st.session_state.current_exercise = generate_exercise(st.session_state.selected_model)
    st.session_state.user_answer = ""
    st.session_state.submitted = False
    st.session_state.correct = None
    st.session_state.show_translation = False
    st.session_state.audio_ready = False
    st.session_state.audio_data = None

# Боковая панель с настройками
with st.sidebar:
    st.title("Настройки")
    
    st.session_state.selected_model = st.radio(
        "Выберите LLM модель:",
        options=["claude", "gpt"],
        index=0,
        format_func=lambda x: "Claude 3.7 Sonnet" if x == "claude" else "GPT-4o"
    )
    
    st.session_state.selected_voice = st.radio(
        "Выберите голос для озвучивания:",
        options=["Jhenny Antiques", "Benjamin"],
        index=0
    )
    
    voice_id_map = {
        "Jhenny Antiques": "2Lb1en5ujrODDIqmp7F3",
        "Benjamin": "LruHrtVF6PSyGItzMNHS"
    }
    st.session_state.voice_id = voice_id_map[st.session_state.selected_voice]

# Основной интерфейс
st.title("Тренажёр испанских глаголов 🇪🇸")

# Генерация упражнения при первом запуске или нажатии кнопки "Далее"
if not st.session_state.current_exercise:
    with st.spinner("Генерируем задание..."):
        st.session_state.current_exercise = generate_exercise(st.session_state.selected_model)

# Если упражнение загружено, отображаем его
if st.session_state.current_exercise:
    exercise = st.session_state.current_exercise
    
    # Отображение инфинитива глагола и времени
    st.markdown(f"### {exercise['verb_infinitive']} ({exercise['tense']})")
    
    # Отображение предложения с пропуском
    st.markdown(f"**{exercise['incomplete_sentence']}**")
    
    # Поле ввода ответа
    user_input = st.text_input(
        "Введите форму глагола:",
        value=st.session_state.user_answer,
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
            "Перевести",
            use_container_width=True
        )
    
    # Проверка ответа
    if check_button:
        st.session_state.user_answer = user_input
        st.session_state.submitted = True
        st.session_state.correct = check_answer(user_input, exercise['correct_form'])
        
        # Генерируем аудио после проверки
        with st.spinner("Подготовка аудио..."):
            st.session_state.audio_data = generate_audio(
                exercise['sentence'],
                st.session_state.voice_id
            )
            st.session_state.audio_ready = True
        
        # Перезагружаем страницу для отображения результатов
        st.rerun()
    
    # Отображение результатов проверки
    if st.session_state.submitted:
        if st.session_state.correct:
            st.success("✅ Правильно!")
        else:
            st.error(f"❌ Неправильно. Верный ответ: **{exercise['correct_form']}**")
            st.info(f"**Объяснение:** {exercise['explanation']}")
    
    # Отображение перевода
    if translate_button:
        st.session_state.show_translation = True
    
    if st.session_state.show_translation:
        st.info(f"**Перевод:** {exercise['translation']}")
    
    # Кнопки "Озвучить" и "Далее"
    col3, col4 = st.columns(2)
    
    with col3:
        if st.session_state.submitted and st.session_state.audio_ready:
            audio_button = st.button(
                "🔊 Озвучить",
                use_container_width=True
            )
            if audio_button and st.session_state.audio_data:
                try:
                    st.audio(st.session_state.audio_data, format="audio/mp3")
                except Exception as e:
                    st.error(f"Ошибка при воспроизведении аудио: {str(e)}")
    
    with col4:
        next_button = st.button(
            "Далее ➡️",
            use_container_width=True
        )
        if next_button:
            with st.spinner("Генерируем новое задание..."):
                next_exercise()
                st.rerun()
else:
    st.warning("Не удалось загрузить упражнение. Пожалуйста, попробуйте еще раз.")
    if st.button("Попробовать снова"):
        next_exercise()
        st.rerun() 