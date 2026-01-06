# Classroom Reservation System (CLI)

Jednoduchá konzolová aplikace pro správu učeben a jejich rezervací
ve škole nebo na univerzitě.  
Aplikace je napsána v jazyce Python a používá **pouze standardní knihovnu**.

---

## Funkcionalita

Aplikace umožňuje uživateli:

- vytvořit novou knihu rezervací (vymazat aktuální data),
- uložit knihu rezervací do souboru (formát JSON),
- načíst knihu rezervací ze souboru (s kontrolou konfliktů),
- přidat novou učebnu,
- přidat novou rezervaci,
- zobrazit seznam učeben,
- zobrazit seznam rezervací (všechny / filtr podle učebny / filtr podle data),
- odstranit jednu rezervaci,
- odstranit všechny rezervace,
- kompletně smazat knihu rezervací (učebny i rezervace).

Uživatelské rozhraní je **textové (CLI)**, bez grafického rozhraní.

---

## Požadavky

- Python **3.10 nebo novější**
- Není potřeba virtuální prostředí
- Nejsou použity žádné externí knihovny

---

## Spuštění aplikace

```bash
python main.py
