from time import time, sleep
from random import randint, random
from win32con import SRCCOPY
from win32gui import DeleteObject, ReleaseDC
from gdilib import get_scaled_resolution, create_screenshot_context, flicker_effect, create_artifacts, draw_text, rotate_screen

def main():
    """
    Основной цикл программы для создания эффектов мерцания, артефактов, текста и поворота экрана.
    """
    # Получаем разрешение экрана с учетом масштабирования
    scaled_width, scaled_height = get_scaled_resolution()

    # Создаем контекст для захвата изображения с экрана
    hdesktop, desktop_dc, img_dc, mem_dc, screenshot = create_screenshot_context()

    try:
        last_rotation_time = time()
        while True:
            # Копируем текущее изображение экрана в битмап
            mem_dc.BitBlt((0, 0), (scaled_width, scaled_height), img_dc, (0, 0), SRCCOPY)

            # Случайные координаты и размер для мерцания
            x = randint(0, scaled_width - 100)
            y = randint(0, scaled_height - 100)
            size = randint(50, 150)

            # Эффект мерцания
            flicker_effect(mem_dc, x, y, size)

            # Создаем артефакты вокруг мерцания
            create_artifacts(mem_dc, x, y, size)

            # Эффект ряби (изредка)
            if random() < 0.2:
                for i in range(10):
                    x_ripple = x + randint(-10, 10)
                    y_ripple = y + randint(-10, 10)
                    flicker_effect(mem_dc, x_ripple, y_ripple, size)
                    img_dc.BitBlt((x_ripple, y_ripple), (size, size), mem_dc, (x_ripple, y_ripple), SRCCOPY)
                    sleep(0.05)

            # Случайное мерцание в разных местах экрана
            for _ in range(randint(1, 5)):
                flicker_x = randint(0, scaled_width - 50)
                flicker_y = randint(0, scaled_height - 50)
                flicker_size = randint(20, 100)
                flicker_effect(mem_dc, flicker_x, flicker_y, flicker_size)
                img_dc.BitBlt((flicker_x, flicker_y), (flicker_size, flicker_size), mem_dc, (flicker_x, flicker_y),
                              SRCCOPY)

            # Рисуем текст "virus!"
            draw_text(mem_dc, "virus!", scaled_width, scaled_height)
            img_dc.BitBlt((0, 0), (scaled_width, scaled_height), mem_dc, (0, 0), SRCCOPY)

            # Поворачиваем экран каждые 5-7 секунд
            if time() - last_rotation_time > randint(7, 11):
                rotate_screen()
                last_rotation_time = time()

            sleep(0.1)

    except KeyboardInterrupt:
        # Очистка
        mem_dc.DeleteDC()
        DeleteObject(screenshot.GetHandle())
        img_dc.DeleteDC()
        ReleaseDC(hdesktop, desktop_dc)

if __name__ == "__main__":
    main()