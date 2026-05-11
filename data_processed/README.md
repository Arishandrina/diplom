Здесь лежат промежуточные и итоговые таблицы пайплайна (в Git не коммитятся)

| Файл | Откуда / зачем |
|---------------|----------------|
| **Реестр Торги - Результаты поиска 25.01.26 10-59.xlsx** | Сырая выгрузка МАРКЕР («Результаты»). Вход для `marker_prepare.ipynb` |
| **Реестр Торги - Цены 25.01.26 11-07.xlsx** | Сырая выгрузка МАРКЕР («Цены»). Вход для `marker_prepare.ipynb` |
| **marker_results_main_clean.csv** | После `marker_prepare.ipynb`: одна строка на закупку, поля МАРКЕР, ссылки |
| **marker_results_participants_clean.csv** | Участники и цены по закупкам (из той же подготовки) |
| **docs/`<registry_number>`__`<purchase_code>`/raw/** | Каталог **`docs/`** — скачанная тендерная документация (`docs_download_marker_playwright.ipynb`) |
| **marker_docs_parsed_auto.csv** | После `docs_parse.ipynb`: места, площадь, адрес, тип работ по документам |
| **marker_results_classified.csv** | После `analysis_01_classify.ipynb`: тип работ и флаг `include_base` (LLM) |
| **analysis_objects_core.csv** | После `analysis_02_dataset.ipynb`: объекты строительства, удельная стоимость, дефлятор, основные регрессоры |
| **eis_restrictions.csv** | После `fetch_eis_data.py`: признаки с карточек ЕИС (ПП 2571, субподряд) + поля МАРКЕР по закупке |
| **places_validation_filled.csv** | Разметка по извлеченным `places` для оценки качества (`analysis_05_places_extraction.ipynb`) |
| **minstroy_school_indices_2022Q1_2025Q4_long_filled.csv** | Индексы Минстроя для дефлятора СМР (квартальные ряды, регионы, 3 компоненты) — имена задаются в `analysis_02_dataset.ipynb` |
