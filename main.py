import keyboard
import time
import pyautogui

key = None
REGION_SKILLCHECK = (500, 300, 1000, 300)
TRIES = 10
SUMX = 168
SUMY = 27
HOOK_INTERVAL = 0
TIMEOUT = 0.65


def get_pressed_key():
    global key
    while True:
        key_pressed = keyboard.read_key()
        if key_pressed:
            key = key_pressed
            return


def key_pressed(pressed_key):
    global fisher
    if pressed_key == key:
        if fisher.state:
            print("Бот остановлен")
            fisher.stop()
        else:
            print("Бот запущен")
            fisher = Fisher()


class Fisher:
    state = 0
    firstAttempt = 0

    def stop(self):
        self.state = 0

    def skillcheck(self):
        locate = None
        try:
            locate = pyautogui.locateOnScreen('mouse.png', region=REGION_SKILLCHECK, confidence=0.9)
        except pyautogui.ImageNotFoundException:
            return
        print("Начался скиллчек")
        time.sleep(TIMEOUT)
        for i in range(3):
            pyautogui.click(locate[0] + SUMX, locate[1] + SUMY)
        print("Подсёк")
        self.state = 2
        if self.firstAttempt:
            self.firstAttempt = TRIES
        return

    def fishing(self):
        try:
            pyautogui.locateOnScreen('fishing.png', region=REGION_SKILLCHECK, confidence=0.9)
        except pyautogui.ImageNotFoundException:
            pass
        else:
            for i in range(20):
                pyautogui.click()
            self.state = 1
            print("Поймал рыбу, жду следующий скиллчек...")

    def evaluate(self):
        if self.state == 0:
            pass
        elif self.state == 1:
            self.skillcheck()
        else:
            if self.firstAttempt < TRIES:
                time.sleep(1)
                print("Не удалось подсечь, пробую ещё раз...")
                self.skillcheck()
                self.firstAttempt += 1
            else:
                self.fishing()


if __name__ == "__main__":
    print("Необходимо назначить клавишу для запуска/остановки бота.\nНажмите любую кнопку:")
    get_pressed_key()
    print(f"Выбранная кнопка: {key}")
    time.sleep(1)
    num = int(input("Введите номер удочки:"))
    TIMEOUT *= (4 - num)
    print("Ожидание запуска...")
    fisher = Fisher()
    timestamp = time.time()

    while True:
        if keyboard.is_pressed(key):
            if time.time() > timestamp:
                timestamp = time.time() + 0.5
                if not fisher.state:
                    print("Включаем бота")
                    fisher.state = 1
                else:
                    print("Выключаем бота")
                    fisher.state = 0
        fisher.evaluate()



