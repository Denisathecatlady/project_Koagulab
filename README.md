# KoaguLab

KoaguLab je jednoduchá laboratorní aplikace pro správu pacientů, vzorků a laboratorních výsledků. Projekt vznikl jako závěrečný úkol v rámci kurzu Python Backend Developer.

---

## Funkce

- **Správa pacientů:** Přehledné ukládání údajů o pacientech včetně rodného čísla, pojišťovny a poznámky.
- **Evidence vzorků:** Každý pacient může mít více odebraných vzorků, vzorkům je automaticky generován kód.
- **Zadávání výsledků:** U každého vzorku lze zadávat výsledky různých laboratorních testů (např. APTT, D-dimer, PT aj.) včetně referenčních rozmezí.
- **Přehled typů testů:** Správce může přidávat nové typy testů a nastavovat jejich jednotky a referenční hodnoty.
- **Registrace a přihlášení uživatelů:** Každý uživatel má své vlastní přihlašovací údaje, možnost registrace nového účtu.
- **Admin rozhraní:** Pro správu všech dat lze využít i vestavěné Django admin rozhraní.

---

## Jak spustit projekt

1. **Klonuj repozitář:**
    ```
    git clone <adresa-repozitáře>
    cd <název-složky>
    ```

2. **Vytvoř a aktivuj virtuální prostředí:**
    ```
    python -m venv .venv
    source .venv/bin/activate      # Linux/macOS
    .venv\Scripts\activate         # Windows
    ```

3. **Nainstaluj závislosti:**
    ```
    pip install -r requirements.txt
    ```

4. **Migrace databáze:**
    ```
    python manage.py migrate
    ```

5. **Vytvoření admin účtu:**
    ```
    python manage.py createsuperuser
    ```

6. **Spuštění serveru:**
    ```
    python manage.py runserver
    ```

---

## Struktura aplikace

- `samples/` – hlavní aplikace s modely, views a formuláři pro pacienty, vzorky a testy.
- `templates/` – složka se šablonami pro všechny stránky.
- `static/` – Bootstrap a případně další statické soubory.

---

## Přihlášení do administrace

- Adresa: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- Použij vytvořený admin účet (viz výše).
- V administraci lze spravovat všechny tabulky a data.

---

## Výchozí uživatelé a data

- Můžeš si v adminu nebo v aplikaci přidat libovolné pacienty, vzorky i typy testů.
- Pro testování lze vkládat zkušební data přímo přes webové formuláře.

---

## Ukázka typických rodných čísel (pro testovací pacienty):

- 9001011235, 8902034567, 9206307890, 8512254321, 9704056789, ...
- Vždy použij platný formát (9 nebo 10 číslic, může být i s lomítkem: `900101/1235`).

---
