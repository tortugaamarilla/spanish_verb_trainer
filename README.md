# 🇪🇸 Тренажёр испанских глаголов

Приложение на Streamlit для тренировки испанских глаголов в различных временах и формах. Разработано специально для русскоговорящих студентов, изучающих испанский язык (Castellano, Испания).

## Особенности

- Тренировка глаголов в различных временах (Presente, Pretérito indefinido, и т.д.)
- Тренировка особых форм (Participio, Gerundio)
- Тренировка специальных конструкций (Estar + gerundio, и т.д.)
- Перевод предложений на русский язык
- Озвучивание предложений с помощью ElevenLabs
- Выбор между Claude 3.7 Sonnet и GPT-4o для генерации примеров

## Установка и запуск локально

1. Клонируйте репозиторий:
   ```bash
   git clone [url-репозитория]
   cd spanish_verb_trainer
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   # Для Linux/Mac:
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.streamlit/secrets.toml` со следующим содержимым (если не существует):
   ```toml
   OPENAI_API_KEY = "ваш-ключ-api-openai"
   ANTHROPIC_API_KEY = "ваш-ключ-api-anthropic"
   ELEVENLABS_API_KEY = "ваш-ключ-api-elevenlabs"
   ```

5. Запустите приложение:
   ```bash
   streamlit run app.py
   ```

## Деплой на Streamlit Cloud

1. Форкните или клонируйте репозиторий на GitHub
2. Зарегистрируйтесь на [streamlit.io](https://streamlit.io/)
3. Создайте новое приложение и выберите ваш репозиторий
4. В настройках приложения добавьте секреты (API ключи) в разделе "Secrets"
5. Разверните приложение

## Используемые технологии

- [Streamlit](https://streamlit.io/) - фреймворк для создания интерактивных приложений
- [Anthropic Claude 3.7](https://www.anthropic.com/) - генерация упражнений и проверка ответов
- [OpenAI GPT-4o](https://openai.com/) - альтернативная модель для генерации и проверки
- [ElevenLabs](https://elevenlabs.io/) - озвучивание испанских предложений 