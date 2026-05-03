"""
Собираю признаки ограничительности закупок с ЕИС

Шаг 1 — готового CSV беру нацрежим, тип торгов, обеспечение заявки/контракта, банковское сопровождение (МАРКЕР)
Шаг 2 — открываю страницы ЕИС через Selenium и ищу упоминания ПП-2571 и ограничений субподряда

"""

import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

df_raw = pd.read_csv("data_processed/marker_results_main_clean.csv")
df_obj = pd.read_csv("data_processed/analysis_objects_core.csv")

# шаг 1 - разворачиваем объекты -> закупки, берем готовые признаки из МАРКЕРА
rows = []
for _, obj in df_obj.iterrows():
    for rn in str(obj["registry_numbers"]).split(";"):
        rows.append({"object_id": obj["object_id"], "registry_number": rn.strip()})

df_rns = pd.DataFrame(rows)
df_rns = df_rns[df_rns["registry_number"] != ""]

df_raw["registry_number"] = df_raw["registry_number"].astype(str)
df = df_rns.merge(df_raw[["registry_number", "source_url", "Нацрежим", "Тип торгов",
                           "Обеспечение заявки, %", "Обеспечение контракта, %", "Банковское \\ казначейское сопровождение"]],
                        on="registry_number", how="left")

df["nac_regime"] = (df["Нацрежим"] == "Да").astype(int)
df["proc_type_raw"] = df["Тип торгов"]
df["bid_sec_pct"] = df["Обеспечение заявки, %"]
df["cont_sec_pct"] = df["Обеспечение контракта, %"]
df["banking_supervision"] = df["Банковское \\ казначейское сопровождение"]\
                              .str.contains("банковское|казначейское", case=False, na=False)\
                              .astype(int)


# шаг 2 - скрап страницы ЕИС
df["eis_url"] = df["source_url"].where(df["source_url"].str.contains("zakupki.gov.ru", na=False))
urls = df["eis_url"].dropna().unique()
print(f"Уникальных URL для скрапинга: {len(urls)}")

opts = webdriver.ChromeOptions()
opts.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=opts)

def scrape_page(url):
    """возвращает словарь с признаками со страницы ЕИС"""
    driver.get(url)
    time.sleep(3)
    text = driver.find_element(By.TAG_NAME, "body").text

    return {
        # 1, если упоминается постановление правительства №2571 (доп. требования к участникам)
        "pp2571": int(bool(re.search(r"2571", text, re.I))),
        # 1, если есть ограничение на привлечение субподрядчиков
        "subpodr_limit": int(bool(re.search(r"самостоятельно без привлечения|запрещ\w+ субподрядч", text, re.I))),
    }

results = {}
for i, url in enumerate(urls):
    print(f"  [{i+1}/{len(urls)}] {url[-50:]}", end=" ... ")
    results[url] = scrape_page(url)
    time.sleep(1)
driver.quit()

df["pp2571"] = df["eis_url"].map(lambda u: results.get(u, {}).get("pp2571"))
df["subpodr_limit"] = df["eis_url"].map(lambda u: results.get(u, {}).get("subpodr_limit"))

df.to_csv("data_processed/eis_restrictions.csv", index=False)