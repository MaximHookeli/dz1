import speech_recognition as sr
import pyttsx3
import datetime
import sys

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.commands = {
            "hello": "Привет! Чем могу помочь?",
            "what time is it": self.get_time,
            "help me": self.help_command,
            "goodbye": "До свидания! Хорошего дня!",
            "exit": self.exit_program
        }

    def speak(self, text):
        print(f"Ассистент: {text}")
        self.speaker.say(text)
        self.speaker.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("\nСлушаю...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                print(f"Вы сказали: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                self.speak("Извините, произошла ошибка при обработке запроса")
                return ""

    def get_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"Текущее время {current_time}"

    def help_command(self):
        help_text = "Вот список доступных команд:\n"
        help_text += "1. 'Hello' - Приветствие\n"
        help_text += "2. 'What time is it' - Узнать текущее время\n"
        help_text += "3. 'Help me' - Показать список команд\n"
        help_text += "4. 'Goodbye' или 'Exit' - Завершить работу"
        return help_text

    def exit_program(self):
        self.speak("До свидания!")
        sys.exit()

    def process_command(self, command):
        if not command:
            return
            
        for key, value in self.commands.items():
            if key in command:
                if callable(value):
                    response = value()
                else:
                    response = value
                self.speak(response)
                return
        
        self.speak("Извините, я не понимаю эту команду. Скажите 'help me' для списка доступных команд.")

    def run(self):
        self.speak("Привет! Я ваш голосовой помощник. Скажите 'help me' для получения списка команд.")
        
        while True:
            command = self.listen()
            self.process_command(command)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
