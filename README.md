
# Open Game Translator

`Game Translator` - это аудио-переводчик для игр, интегрирующий whisper.cpp для транскрипции и LLaMA 3 в Ollama для перевода. Этот инструмент позволяет транскрибировать и переводить аудиоконтент игры на целевой язык.

## Возможности
- Транскрипция аудиофайлов с использованием whisper.cpp.
- Перевод транскрибированного текста на целевой язык с помощью LLaMA 3.
- Поддержка предварительно записанных аудиофайлов.

## Требования
- Python 3.8 или выше.
- Установленный whisper.cpp.
- Установленный Ollama (для модели LLaMA 3).

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your-username/game-translator.git
    cd game-translator
    ```

2. Установите зависимости Python:
    ```bash
    pip install -r requirements.txt
    ```

3. Скачайте и установите [whisper.cpp](https://github.com/ggerganov/whisper.cpp):
    ```bash
    git clone https://github.com/ggerganov/whisper.cpp
    cd whisper.cpp
    make
    ```

4. Убедитесь, что у вас установлен Ollama и LLaMA 3:
    - [Ollama](https://ollama.com)
    - Модель LLaMA 3:
      ```bash
      ollama run llama3
      ```

## Использование
Для запуска аудио-переводчика выполните следующие действия:

1. Подготовьте аудиофайл, который хотите транскрибировать и перевести.
2. Запустите `Game Translator` с командной строки:
    ```bash
    python translator.py --file /path/to/your/audiofile.wav \
                         --transcription_model whisper_cpp \
                         --pre_recorded \
                         -i english \
                         -o russian
    ```

### Пример
```bash
python translator.py --file ./example.wav \
                     --transcription_model whisper_cpp \
                     --pre_recorded \
                     -i english \
                     -o russian
```

## Аргументы командной строки
- `--file`: Путь к аудиофайлу для транскрипции.
- `--transcription_model`: Модель транскрипции (только `whisper_cpp` поддерживается).
- `--pre_recorded`: Использовать ли предварительно записанный аудиофайл.
- `-i`, `--input_language`: Язык аудио для транскрипции (например, `english`, `chinese`).
- `-o`, `--output_language`: Целевой язык для перевода (например, `english`, `russian`).

## Пример кода
```python
from game_translator import GameTranslator

translator = GameTranslator(
    transcription_model="whisper_cpp",
    filepath="./example.wav",
    prerecorded=True,
    input_language="english",
    output_language="russian"
)

translation_result = translator.translate()
print(f"Перевод:\n{translation_result}")
```

## Лицензия
Этот проект находится под лицензией MIT License. См. [LICENSE](LICENSE) для деталей.
