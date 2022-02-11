import sys, random, time

try:
    import bext
except ImportError:
    print('Не удалось импортировать модуль Bext.\n Установите его.')
    sys.exit()

# Задаем константы
WIDTH, HEIGHT = bext.size()
WIDTH -= 1
NUMBERS_OF_LOGO = 3
PAUSE_AMOUNT = 0.1
COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

UP_RIGHT = 'ur'
UP_LEFT = 'ul'
DOWN_RIGHT = 'dr'
DOWN_LEFT = 'dl'
DIRECTIONS = (UP_LEFT, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT)

# Название ключей для асоциативных массивов логотипов
COLOR = 'color'
X = 'x'
Y = 'y'
DIR = 'direction'


def main():
    bext.clear()

    # Генерация логотипов
    logos = []
    for i in range(NUMBERS_OF_LOGO):
        logos.append({COLOR: random.choice(COLORS),
                      X: random.randint(1, WIDTH - 4),
                      Y: random.randint(1, HEIGHT - 4),
                      DIR: random.choice(DIRECTIONS)})
        if logos[-1][X] % 2 == 1:
            # Гарантируем что Х четное число, для сталкновения с углом
            logos[-1][X] -= 1

    cornerBounce = 0  # Считаем сколько раз логотип столкнулся с углом
    while True:  # Основной цикл программы
        for logo in logos:  # Обрабатываем все логотипы в списке логотипов
            # Очищаем место где ранее находился логотип
            bext.goto(logo[X], logo[Y])
            print('   ', end='')

            originalDirection = logo[DIR]
            # Проверяем не отскакивает ли логотип от угла
            if logo[X] == 0 and logo[Y] == 0:
                logo[DIR] = DOWN_RIGHT
                cornerBounce += 1
            elif logo[X] == 0 and logo[Y] == HEIGHT - 1:
                logo[DIR] = UP_RIGHT
                cornerBounce += 1
            elif logo[X] == WIDTH - 3 and logo[Y] == 0:
                logo[DIR] = DOWN_LEFT
                cornerBounce += 1
            elif logo[X] == WIDTH - 3 and logo[Y] == HEIGHT - 1:
                logo[DIR] = UP_LEFT
                cornerBounce += 1

            # Проверяем, не отскакивает ли логотип от левого края:
            elif logo[X] == 0 and logo[DIR] == UP_LEFT:
                logo[DIR] = UP_RIGHT
            elif logo[X] == 0 and logo[DIR] == DOWN_LEFT:
                logo[DIR] = DOWN_RIGHT

            # Проверяем, не отскакивает ли логотип от правого края:
            # (WIDTH - 3, поскольку 'DVD' состоит из трех букв.)
            elif logo[X] == WIDTH - 3 and logo[DIR] == UP_RIGHT:
                logo[DIR] = UP_LEFT
            elif logo[X] == WIDTH - 3 and logo[DIR] == DOWN_RIGHT:
                logo[DIR] = DOWN_LEFT

            # Проверяем, не отскакивает ли логотип от верхнего края:
            elif logo[Y] == 0 and logo[DIR] == UP_LEFT:
                logo[DIR] = DOWN_LEFT
            elif logo[Y] == 0 and logo[DIR] == UP_RIGHT:
                logo[DIR] = DOWN_RIGHT

            # Проверяем, не отскакивает ли логотип от нижнего края:
            elif logo[Y] == HEIGHT - 1 and logo[DIR] == DOWN_LEFT:
                logo[DIR] = UP_LEFT
            elif logo[Y] == HEIGHT - 1 and logo[DIR] == DOWN_RIGHT:
                logo[DIR] = UP_RIGHT

            if logo[DIR] != originalDirection:
                # Меняем цвет при отскакивании логотипа:
                logo[COLOR] = random.choice(COLORS)

            # Перемещаем логотип. (Координата X меняется на 2, поскольку
            # в терминале высота символов вдвое превышает ширину.
            if logo[DIR] == UP_RIGHT:
                logo[X] += 2
                logo[Y] -= 1
            elif logo[DIR] == UP_LEFT:
                logo[X] -= 2
                logo[Y] -= 1
            elif logo[DIR] == DOWN_RIGHT:
                logo[X] += 2
                logo[Y] += 1
            elif logo[DIR] == DOWN_LEFT:
                logo[X] -= 2
                logo[Y] += 1

        # Отображает количество отскакиваний от углов:
        bext.goto(5, 0)
        bext.fg('white')
        print('Corner bounces:', cornerBounce, end='')
        for logo in logos:
            # Отрисовывает логотипы на новом месте:
            bext.goto(logo[X], logo[Y])
            bext.fg(logo[COLOR])
            print('DVD', end='')

        sys.stdout.flush()  # Нужно для программ, использующих модуль bext
        time.sleep(PAUSE_AMOUNT)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Отображение гуляющего логотипа, create ZQRey')
        sys.exit()
