# FL_HW06

- В файле `parser.py` находится парсер упрощенного множества пролога.
- Тесты находятся в файле `grammar_test.py`.
- Файлы для тестов находятся в папке `test_files`.

Отдельный запуск парсера:

```
python3 parser.py file_name [key]
```

Так же есть ключи, с помощью которых можно проверять отдельные лексемы языка. Чтобы некоторые из них работали, нужно, чтобы каждая лексема находилась на отдельной строчке. Например `inp.txt` должени иметь вид при запуке с ключем `--typeexpr`:

```
A -> B -> C
list (list A) -> list A -> o
pair A B -> (A -> C) -> (B -> D) -> pair C D
```

Список ключей `[key]`:

- `--atom` -- проверяет атомы, для проверки каждый атом должен находится на отдельной строке;

- `--typeexpr` -- проверяет типы (только выражения), для проверки каждый атом должен находится на отдельной строке;

- `--type` -- проверяет определение типов, лексема может распологаться на нескольких строчках;

- `--module` -- проверяет определение модуля, лексема может распологаться на нескольких строчках;

- `--relation` -- проверяет определение отношений, лексема может распологаться на нескольких строчках;

- `--list` -- проверяет списки, для проверки каждый атом должен находится на отдельной строке;

- `--prog` -- проверяет программу полностью, ключ может отсутствовать и по умолчанию выполняется этот ключ.

Тесты можно запустить командой:

```
pytest grammar_test.py
```
