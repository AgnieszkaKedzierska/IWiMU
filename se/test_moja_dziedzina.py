"""Testy własnej bazy wiedzy. Uruchom: python se/test_moja_dziedzina.py."""
from copy import deepcopy
from pathlib import Path

from silnik import wczytaj_baze, wnioskuj_w_przod, wnioskuj_wstecz

baza = wczytaj_baze(Path(__file__).parent.parent / "wiedza" / "moja_dziedzina.json")

PRZYPADKI = [
    ({"uczulenie": "nie", "czas_opieki": 90, "wielkosc_mieszkania": "duże", "kontakt": "bliski kontakt", "spacery": "tak"}, "pies", ["R2", "R15"]),
    ({"uczulenie": "nie", "czas_opieki": 120, "wielkosc_mieszkania": "duże", "kontakt": "bliski kontakt", "spacery": "nie"}, "kot", ["R2", "R19"]),
    ({"uczulenie": "tak", "czas_opieki": 59, "wielkosc_mieszkania": "małe", "kontakt": "obserwacja", "spacery": "nie"}, "rybki akwariowe", ["R1", "R3"]),
    ({"uczulenie": "tak", "czas_opieki": 60, "wielkosc_mieszkania": "małe", "kontakt": "bliski kontakt", "spacery": "nie"}, "agama", ["R1", "R6"]),
    ({"uczulenie": "nie", "czas_opieki": 45, "wielkosc_mieszkania": "małe", "kontakt": "bliski kontakt", "spacery": "nie"}, "chomik", ["R2", "R10"]),
]

ok = 0
for wejscie, oczekiwane, oczekiwany_slad in PRZYPADKI:
    fakty, slad = wnioskuj_w_przod(baza, wejscie)
    w_przod_ok = fakty.get("zwierze") == oczekiwane and (oczekiwany_slad is None or slad == oczekiwany_slad)

    zadane = []
    def zapytaj(atrybut, powod):
        zadane.append(atrybut)
        return wejscie[atrybut]

    wstecz = wnioskuj_wstecz(baza, "zwierze", {}, zapytaj, [])
    wstecz_ok = wstecz == oczekiwane and len(zadane) == len(set(zadane))

    status = "OK " if w_przod_ok and wstecz_ok else "BŁĄD"
    ok += w_przod_ok and wstecz_ok
    print(f"[{status}] {wejscie} -> w przód: {fakty.get('zwierze')}, wstecz: {wstecz}, pytań: {len(zadane)}")

print(f"\nZaliczone przypadki: {ok}/{len(PRZYPADKI)}")
print("\n=== Test konfliktu reguł ===")

baza_konflikt = deepcopy(baza)

wejscie = {
    "uczulenie": "nie",
    "czas_opieki": 90,
    "wielkosc_mieszkania": "duże",
    "kontakt": "bliski kontakt",
    "spacery": "tak"
}

# Wyszukanie reguły R19
r19 = next(r for r in baza_konflikt["reguly"] if r["id"] == "R19")

# Usunięcie warunku dotyczącego spacerów
r19["jesli"] = [
    warunek for warunek in r19["jesli"]
    if warunek[0] != "spacery"
]

def zapytaj_konflikt(atrybut, powod):
    return wejscie[atrybut]

# R15 przed R19
fakty, slad = wnioskuj_w_przod(baza_konflikt, wejscie)
wstecz = wnioskuj_wstecz(baza_konflikt, "zwierze", {}, zapytaj_konflikt, [])

print("R15 przed R19:", fakty.get("zwierze"))
print("Wstecz:", wstecz)
print("Reguły:", " -> ".join(slad))

assert fakty.get("zwierze") == wstecz == "pies"

# Przeniesienie R19 przed R15
baza_konflikt["reguly"].remove(r19)

indeks = next(
    i for i, r in enumerate(baza_konflikt["reguly"])
    if r["id"] == "R15"
)

baza_konflikt["reguly"].insert(indeks, r19)

fakty, slad = wnioskuj_w_przod(baza_konflikt, wejscie)
wstecz = wnioskuj_wstecz(baza_konflikt, "zwierze", {}, zapytaj_konflikt, [])

print("R19 przed R15:", fakty.get("zwierze"))
print("Wstecz:", wstecz)
print("Reguły:", " -> ".join(slad))

assert fakty.get("zwierze") == wstecz == "kot"

print("[OK] Test konfliktu reguł zaliczony")