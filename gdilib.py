from win32api import GetSystemMetrics, RGB, EnumDisplayDevices, EnumDisplaySettings, ChangeDisplaySettingsEx
from win32con import SM_CXSCREEN, SM_CYSCREEN, BS_SOLID, TRANSPARENT, ENUM_CURRENT_SETTINGS, DM_DISPLAYORIENTATION, DM_PELSWIDTH, DM_PELSHEIGHT
from win32gui import GetDesktopWindow, GetWindowDC
from win32ui import CreateDCFromHandle, CreateBitmap, CreateBrush, CreateFont
from ctypes import windll
from random import randint

def get_scaled_resolution():
    """
    Получает реальное разрешение экрана с учетом масштабирования.

    Возвращает:
        tuple: (scaled_width, scaled_height) - ширина и высота экрана с учетом масштабирования.
    """
    # Получаем реальное разрешение экрана
    real_width = GetSystemMetrics(SM_CXSCREEN)
    real_height = GetSystemMetrics(SM_CYSCREEN)

    # Получаем DPI для масштабирования
    user32 = windll.user32
    hdesktop = GetDesktopWindow()
    dpi = user32.GetDpiForWindow(hdesktop)
    scale_factor = dpi / 96  # 96 - это стандартный DPI

    # Корректируем размеры с учетом масштабирования
    scaled_width = int(real_width * scale_factor)
    scaled_height = int(real_height * scale_factor)

    return scaled_width, scaled_height

def create_screenshot_context():
    """
    Создает контекст устройства для захвата изображения с экрана.

    Возвращает:
        tuple: (hdesktop, desktop_dc, img_dc, mem_dc, screenshot) - handles и контексты для работы с экраном.
    """
    # Получаем handle на весь экран
    hdesktop = GetDesktopWindow()

    # Получаем контекст устройства для всего экрана
    desktop_dc = GetWindowDC(hdesktop)
    img_dc = CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    # Получаем реальное разрешение экрана с учетом масштабирования
    scaled_width, scaled_height = get_scaled_resolution()

    # Создаем битмап для хранения изображения
    screenshot = CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, scaled_width, scaled_height)
    mem_dc.SelectObject(screenshot)

    return hdesktop, desktop_dc, img_dc, mem_dc, screenshot

def flicker_effect(mem_dc, x, y, size):
    """
    Создает эффект мерцания на экране.

    Аргументы:
        mem_dc (PyCDC): Контекст устройства в памяти.
        x (int): Координата X верхнего левого угла мерцания.
        y (int): Координата Y верхнего левого угла мерцания.
        size (int): Размер мерцающего квадрата.
    """
    color = RGB(randint(0, 255), randint(0, 255), randint(0, 255))
    brush = CreateBrush(BS_SOLID, color, 0)
    mem_dc.SelectObject(brush)
    mem_dc.Rectangle((x, y, x + size, y + size))

def create_artifacts(mem_dc, x, y, size):
    """
    Создает артефакты вокруг заданной области.

    Аргументы:
        mem_dc (PyCDC): Контекст устройства в памяти.
        x (int): Координата X центральной точки.
        y (int): Координата Y центральной точки.
        size (int): Размер области, вокруг которой создаются артефакты.
    """
    for _ in range(randint(1, 5)):
        artifact_x = x + randint(-size, size)
        artifact_y = y + randint(-size, size)
        artifact_size = randint(10, 50)
        flicker_effect(mem_dc, artifact_x, artifact_y, artifact_size)

def draw_text(mem_dc, text, scaled_width, scaled_height):
    """
    Рисует текст на экране в случайном месте.

    Аргументы:
        mem_dc (PyCDC): Контекст устройства в памяти.
        text (str): Текст для отображения.
        scaled_width (int): Ширина экрана с учетом масштабирования.
        scaled_height (int): Высота экрана с учетом масштабирования.
    """
    font = CreateFont({
        "name": "Arial",
        "height": randint(30, 100),  # Случайный размер шрифта
        "weight": 700,
    })
    mem_dc.SelectObject(font)

    # Случайные координаты для текста
    x = randint(0, scaled_width - 200)
    y = randint(0, scaled_height - 50)

    # Случайный цвет текста
    text_color = RGB(randint(0, 255), randint(0, 255), randint(0, 255))
    mem_dc.SetTextColor(text_color)

    # Рисуем текст с прозрачным фоном
    mem_dc.SetBkMode(TRANSPARENT)  # Устанавливаем прозрачный фон для текста
    mem_dc.TextOut(x, y, text)

def rotate_screen():
    """
    Поворачивает экран на 90 градусов.
    """
    try:
        # Получаем информацию о текущем устройстве
        d = EnumDisplayDevices(None, 0)
        dm = EnumDisplaySettings(d.DeviceName, ENUM_CURRENT_SETTINGS)

        # Текущая ориентация
        current_orientation = dm.DisplayOrientation

        # Поворачиваем экран на 90 градусов
        new_orientation = (current_orientation + 1) % 4  # 0: 0°, 1: 90°, 2: 180°, 3: 270°

        # Устанавливаем новую ориентацию и меняем ширину и высоту
        dm.DisplayOrientation = new_orientation
        dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
        dm.Fields = DM_DISPLAYORIENTATION | DM_PELSWIDTH | DM_PELSHEIGHT

        # Применяем изменения
        result = ChangeDisplaySettingsEx(d.DeviceName, dm)
    except Exception as e:
        print(f"Ошибка: {e}")