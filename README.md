# CanalPL — skórka Full HD dla Enigma2

Autorska skórka inspirowana estetyką polskiego CANAL+: czerń, biel, zielony akcent,
duża typografia i prosty pasek teraz/następnie. To projekt niezależny, bez oficjalnego
logo i grafik operatora. Nie zmienia funkcji dekodera, uprawnień ani list kanałów.

**Wersja 0.1.0 — do testów na dekoderze.** Rozdzielczość interfejsu: 1920×1080.
Sprawdzono statycznie XML, współrzędne i pakowanie. Nie uruchomiono skórki na
fizycznym urządzeniu; nie deklarujemy jeszcze zgodności z konkretnym obrazem.
Baza API: standardowe komponenty Enigma2 z gałęzi `develop` OpenPLi.
OpenATV i inne obrazy mogą wymagać dostosowania nazw ekranów lub komponentów.

## Podgląd

![Pasek informacji — wizualizacja z XML](docs/infobar.svg)
![Lista kanałów — wizualizacja z XML](docs/channels.svg)
![Menu — wizualizacja z XML](docs/menu.svg)

Wizualizacje powstają ze współrzędnych w `skin.xml` i przykładowych danych.
Nie są zrzutami ekranu dekodera. Font systemowy, łamanie tekstu i wygląd list
mogą różnić się na urządzeniu. Tło pod paskiem jest zastępcze.

## Zakres

- `InfoBar`: nazwa kanału, zegar, bieżąca/następna audycja, postęp i nagrywanie.
- `ChannelSelection`: lista, opis wybranej audycji, godziny i klawisze kolorowe.
- `Menu`: duże pozycje, zielone zaznaczenie, zegar.
- `EPGSelection`: standardowa lista programu TV; opisy klawiszy pochodzą z systemu.
- `EventView`: przewijany opis audycji i przyciski programowania nagrania.
- `MoviePlayer`: tytuł nagrania, postęp, czas odtwarzania i pozostały czas.
- `Volume`, `Mute`: głośność i wyciszenie.

Pozostałe ekrany, w tym ustawienia, lista nagrań, okna dialogowe i graficzne EPG
specyficzne dla dystrybucji, korzystają z definicji systemowych. To pierwsza wersja
skórki, a nie kompletna kopia oprogramowania dekodera operatora. Nie wymaga
dodatkowych rendererów, konwerterów, piconów, fontów ani dostępu do internetu.
Brak danych EPG skutkuje pustym tytułem/godziną, zgodnie z zachowaniem Enigma2.

## Instalacja przez SFTP

1. Pobierz repozytorium: **Code → Download ZIP** i rozpakuj archiwum.
2. Prześlij cały katalog `CanalPL` do `/usr/share/enigma2/` na dekoderze.
   Plik powinien znaleźć się w `/usr/share/enigma2/CanalPL/skin.xml`.
   Przy aktualizacji wcześniej zachowaj kopię starego katalogu.
3. W ustawieniach interfejsu/użytkownika wybierz skórkę **CanalPL**.
   Dokładna ścieżka menu zależy od obrazu. Zatwierdź restart GUI.

## Instalacja paczki przez SSH

Gotowa paczka znajduje się w `packages/CanalPL-0.1.0.tar.gz`.
Prześlij ją do `/tmp` na dekoderze, a następnie wykonaj:

```sh
mkdir -p /tmp/canalpl-install
cd /tmp/canalpl-install
tar -xzf /tmp/CanalPL-0.1.0.tar.gz
sh install.sh
```

Instalator tworzy kopię istniejącego katalogu CanalPL i ustawia prawa plików.
Nie zmienia aktywnej skórki ani nie restartuje GUI. Wybierz skórkę w menu.
Archiwum `.tar.gz` nie jest pakietem `.ipk`; nie instaluj go poleceniem `opkg`.

## Powrót do poprzedniej skórki

Z menu wybierz poprzednią skórkę i uruchom ponownie GUI. Jeśli GUI nie startuje,
zaloguj się przez SSH i zatrzymaj je (`init 4`, jeśli obraz obsługuje runlevel).
Zrób kopię `/etc/enigma2/settings`, następnie usuń z tego pliku wyłącznie wiersz:

```text
config.skin.primary_skin=CanalPL/skin.xml
```

Uruchom GUI (`init 3` w obrazach z runlevel). Enigma2 powinno użyć skórki domyślnej.
W obrazach z innym menedżerem usług użyj właściwej dla nich procedury restartu.
Katalog CanalPL można usunąć po przełączeniu na inną skórkę.

## Weryfikacja i rozwój

Na komputerze z Pythonem 3, w katalogu repozytorium:

```sh
python3 scripts/validate.py
python3 scripts/preview.py
python3 scripts/build.py
```

Podglądy nie wymagają dodatkowych bibliotek. Wynik budowania trafia do `dist/`.
Przed wydaniem kolejnej wersji sprawdź na dekoderze: start GUI, przełączanie kanałów,
brak EPG, długie polskie tytuły, listę kanałów i bukietów, przewijanie opisu audycji,
EPG, programowanie nagrania, odtwarzanie, pauzę/przewijanie i regulację głośności.
Klawisze zachowują funkcje przypisane przez obraz; skórka nie zmienia mapowania pilota.

Do dopasowania zgłoszenia podaj model dekodera, nazwę i wersję obrazu oraz log błędu
skórki. Licencja autorskich plików: MIT. Nazwa CANAL+ należy do jej właściciela.
