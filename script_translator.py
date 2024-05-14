import argparse
import subprocess
import time


class GameTranslator:
    """
    Аудио-переводчик для игр.

    Этот класс предоставляет функциональность для транскрипции и перевода аудио контента.

    Атрибуты:
        filepath (str): Путь к аудиофайлу для транскрипции.
        transcription_model (str): Модель транскрипции (whisper_cpp).
        pre_recorded (bool): Использовать ли предварительно записанный файл.
        input_language (str): Язык аудио для транскрипции.
        output_language (str): Язык, на который будет переведен текст.
    """

    def __init__(
            self,
            transcription_model,
            filepath="",
            prerecorded=True,
            input_language="english",
            output_language="russian",
    ):
        """
        Инициализирует новый экземпляр GameTranslator.

        Args:
            transcription_model (str): Модель транскрипции (whisper_cpp).
            filepath (str): Путь к аудиофайлу для транскрипции.
            prerecorded (bool): Использовать ли предварительно записанный файл.
            input_language (str): Язык аудио для транскрипции.
            output_language (str): Язык, на который будет переведен текст.
        """
        self.pre_recorded = prerecorded
        self.transcription_model = transcription_model
        self.filepath = filepath
        self.input_language = input_language.lower()
        self.output_language = output_language.lower()
        self.elapsed_time = 0

    def show_translator_info(self):
        """
        Показывает основные конфигурации переводчика.

        Args:
            None
        Returns:
            None
        """
        print("****************************************")
        print(f"Transcription model : {self.transcription_model}")
        print(f"Using prerecorded audio file : {self.filepath if self.pre_recorded else 'None'}")
        print(f"Input  language : {self.input_language}")
        print(f"Output language : {self.output_language}")
        print("****************************************")

    def show_time(self):
        """
        Показывает затраченное время на транскрипцию и перевод.

        Args:
            None
        Returns:
            None
        """
        print(f"Elapsed time: {self.elapsed_time:.3f} seconds")

    def whisper_cpp_transcription(self):
        """
        Выполняет транскрипцию с использованием whisper.cpp.

        Args:
            None
        Returns:
            str: Результат транскрипции.
        """
        if not self.pre_recorded:
            raise NotImplementedError("Прямая запись аудио не реализована в этой версии.")

        # Убедитесь, что путь к whisper.cpp и модели корректен
        whisper_path = "./whisper.cpp/main"
        model_path = "./whisper.cpp/models/ggml-base.en.bin"
        result_file = self.filepath.replace(".wav.txt", ".txt")

        # Запускаем whisper.cpp для транскрипции
        command = [
            whisper_path,
            "-m", model_path,
            "-f", self.filepath,
            "-l", self.input_language,
            "-otxt"
        ]
        try:
            subprocess.run(command, check=True)
            with open(result_file, "r") as f:
                content = f.read().strip()
        except subprocess.CalledProcessError as e:
            print(f"Ошибка транскрипции с использованием whisper.cpp: {e}")
            content = ""

        return content

    def llama_translation(self, text):
        """
        Переводит текст на целевой язык с использованием LLaMA 3 в Ollama.

        Args:
            text (str): Текст для перевода.
        Returns:
            str: Результат перевода.
        """
        command = [
            "ollama", "run", "llama3",
            f"Translate the following text to {self.output_language}: {text}"
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Ошибка перевода с использованием LLaMA 3: {e}")
            return ""

    def translate(self):
        """
        Выполняет транскрипцию и перевод.

        Args:
            None
        Returns:
            str: Результат перевода.
        """
        start_time = time.time()
        self.show_translator_info()

        # Выполняем транскрипцию
        if self.transcription_model == "whisper_cpp":
            text = self.whisper_cpp_transcription()
        else:
            raise ValueError("Поддерживается только модель 'whisper_cpp'.")

        if not text:
            print("Ошибка: Транскрипция не удалась.")
            return ""

        # Выполняем перевод
        translation = self.llama_translation(text)
        end_time = time.time()
        self.elapsed_time = end_time - start_time
        self.show_time()
        return translation

def main():
        """
        Основная функция, которая получает ввод с командной строки для создания и запуска переводчика.
        """
        parser = argparse.ArgumentParser(description="Аудио-переводчик на базе Ollama и whisper.cpp")

        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Путь к аудиофайлу для транскрипции."
        )
        parser.add_argument(
            "--transcription_model",
            type=str,
            choices=["whisper_cpp"],
            required=True,
            help="Модель транскрипции (только 'whisper_cpp' поддерживается)."
        )
        parser.add_argument(
            "--pre_recorded",
            action="store_true",
            help="Если установлен, используется предварительно записанный аудиофайл."
        )
        parser.add_argument(
            "-i",
            "--input_language",
            required=True,
            type=str,
            help="Язык аудио для транскрипции (например, 'english', 'chinese')."
        )
        parser.add_argument(
            "-o",
            "--output_language",
            required=True,
            type=str,
            help="Целевой язык для перевода (например, 'english', 'russian')."
        )

        args = parser.parse_args()

        # Создаем экземпляр переводчика
        translator = GameTranslator(
            transcription_model=args.transcription_model,
            filepath=args.file,
            prerecorded=args.pre_recorded,
            input_language=args.input_language,
            output_language=args.output_language
        )

        # Выполняем перевод
        translation_result = translator.translate()
        print(f"Перевод:\n{translation_result}")

if __name__ == "__main__":
    main()
