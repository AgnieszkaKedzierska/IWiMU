## Konsultacja wstecz

Przykładowa konsultacja systemu ekspertowego wspomagającego
wybór zwierzęcia domowego:

=== Wnioskowanie wstecz ===

Czy masz uczulenie na sierść? (tak/nie) nie

Jak duże masz mieszkanie? (małe/duże) duże

Ile minut dziennie na opiekę? 120

Czy możesz wyprowadzać na spacery? (tak/nie) nie

Jaki kontakt preferujesz? (obserwacja/bliski kontakt) bliski kontakt

Polecam: kot

Reguły: R2 -> R9 -> R24

Silnik rozpoczyna wnioskowanie od celu, którym jest wybór
zwierzęcia domowego, a następnie zadaje użytkownikowi pytania
niezbędne do podjęcia decyzji.

- R2 – określenie czasu opieki na co najmniej 60 minut.
- R9 – ustalenie pośredniego profilu opieki.
- R24 – wybór kota na podstawie braku możliwości
  wyprowadzania na spacery i preferencji bliskiego kontaktu.

System zadał pięć pytań i na podstawie uzyskanych odpowiedzi
oraz reguł z bazy wiedzy wyznaczył decyzję końcową.

## Strategia rozwiązywania konfliktów reguł

W silniku zastosowano strategię pierwszej pasującej reguły.
Jeżeli warunki kilku reguł są spełnione, a ich wnioski są
sprzeczne, pierwszeństwo ma reguła sprawdzona jako pierwsza.

W celu przeprowadzenia testu konfliktu utworzono kopię bazy
wiedzy i usunięto warunek dotyczący spacerów z reguły R24.
Dzięki temu dla tych samych danych wejściowych spełnione
zostały dwie reguły:
- R22 – wybór psa.
- R24 – wybór kota.

### Wyniki testu konfliktu

| Kolejność reguł | Wynik |
|---|---|
| R22 przed R24 | pies |
| R24 przed R22 | kot |

Reguła R22 ma pierwszeństwo w pierwotnej kolejności,
ponieważ możliwość wyprowadzania zwierzęcia na spacery
w tej gałęzi drzewa prowadzi do wyboru psa.

Test pokazuje, że kolejność reguł ma wpływ na wynik
wnioskowania. Konflikt został celowo wywołany na kopii
bazy wiedzy, bez modyfikowania oryginalnego pliku bazy.






