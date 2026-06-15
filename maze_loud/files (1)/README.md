# A1_Maze_Py

Проект «Лабиринт» — Школа 21, Python Bootcamp.

## Что уже готово (этап 1 из 6)

- [x] Доменная модель `Maze` (тонкие стены, проверка размеров 1..50)
- [x] Загрузка лабиринта из файла (формат из задания)
- [x] Сохранение лабиринта в файл
- [x] GUI на Tkinter с кнопкой «Открыть» и отрисовкой 500×500
- [x] Модульные тесты для модуля загрузки
- [ ] Часть 2 — генерация идеального лабиринта (Эллер)
- [ ] Часть 3 — решение лабиринта (BFS)
- [ ] Часть 4 — генерация пещер (клеточный автомат)
- [ ] Часть 5 — Q-обучение агента
- [ ] Часть 6 — веб-интерфейс

## Структура

```
A1_Maze_Py/
├── Makefile
├── requirements.txt
├── README.md
├── src/
│   ├── main.py
│   └── maze/
│       ├── domain.py       — модель Maze + Point + направления
│       ├── file_io.py      — load_maze, save_maze, MazeFileError
│       └── gui.py          — Tkinter-приложение
├── tests/
│   └── test_file_io.py     — pytest-тесты
├── examples/
│   └── maze_4x4.txt        — пример из задания
└── _commented/
    ├── domain_commented.py
    ├── file_io_commented.py
    └── gui_commented.py
```

Папка `_commented/` — те же файлы, но с подробными комментариями
для изучения. В финальной сдаче её можно удалить.

## Сборка и запуск

```bash
# Создать виртуальное окружение и поставить зависимости
make all

# Запустить приложение
make run

# Прогнать тесты
make tests

# Собрать архив для сдачи
make dist

# Установить программу в $HOME/Maze_app
make install

# Удалить установленную версию
make uninstall

# Очистить временные файлы
make clean
```

## Если Tkinter не запускается на Fedora

Tkinter обычно идёт со стандартным Python, но на Fedora он вынесен
в отдельный пакет:

```bash
sudo dnf install python3-tkinter
```

## Стиль кода

Соблюдается Google Python Style Guide.
Проверка через `make lint` (запускает pylint).
