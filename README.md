# CanalPL 0.2.2 — skórka Enigma2 dla OpenATV

Ciemny interfejs Full HD 1920×1080 inspirowany polskim CANAL+: białe napisy,
zielone zaznaczenie, duże menu, pikony, bukiety i program TV. Projekt niezależny,
bez oficjalnych logotypów i grafik operatora.

**Baza: natywne ekrany i komponenty OpenATV 7.5 / 7.6 / 8.0.** Wersja 0.2.2 zastępuje
wstępną bazę OpenPLi z 0.1.0. Sprawdzono kontrakty widgetów trzech wersji OpenATV,
układy, grafiki, menu, paczki i instalator. **Test na fizycznym dekoderze jest
jeszcze wymagany** — nie deklarujemy potwierdzonej zgodności sprzętowej.

## Podglądy

Wizualizacje powstają z układu XML i przykładowych danych. Listy, tytuły i pikony
w podglądach są przykładowe; nie są zrzutami z działającego odbiornika. Liczba
wierszy i rozmiary fontów na dekoderze zależą także od ustawień OpenATV.

![Menu główne](docs/menu.svg)
![Lista kanałów z pikonami](docs/channels.svg)
![Wybór bukietów](docs/bouquets.svg)
![Graficzne EPG](docs/epg.svg)
![Pasek informacji](docs/infobar.svg)

## Co obejmuje

- Menu główne i podmenu, opisy oraz standardowe style listy OpenATV.
- Lista kanałów i radia, wybór bukietów i wariant z podglądem TV.
- Pikona bieżącego i zaznaczonego kanału; natywne pikony w liście i EPG.
- EPG pojedyncze, multi, graficzna siatka, PIG, szybkie i pionowe; bukiety w EPG.
- Opis audycji, programowanie nagrania, przegląd timerów.
- Lista nagrań, odtwarzacz, pauza/przewijanie i stan timeshiftu.
- Ustawienia, dźwięk/napisy, wtyczki lista/siatka i podstawowe okna dialogowe.

Łącznie 40 definicji ekranów. Specjalistyczne ekrany i zewnętrzne wtyczki mogą
korzystać z układu systemowego. Pełny zakres, źródła API i lista testów sprzętowych:
[COMPATIBILITY.md](docs/COMPATIBILITY.md).

## Instalacja `.ipk` — OpenATV

Pobierz [enigma2-plugin-skins-canalpl_0.2.2_all.ipk](packages/enigma2-plugin-skins-canalpl_0.2.2_all.ipk)
przyciskiem pobierania pliku na GitHubie. Prześlij go przez SFTP do `/tmp` dekodera:

```sh
opkg install /tmp/enigma2-plugin-skins-canalpl_0.2.2_all.ipk
```

Następnie wybierz **CanalPL** w ustawieniach interfejsu / wyborze skórki i zatwierdź
restart GUI. Dokładne nazwy menu zależą od tłumaczenia i wydania OpenATV.
Pakiet nie przełącza skórki ani nie restartuje dekodera automatycznie.
Aktualizacjami i usuwaniem wersji `.ipk` zarządza `opkg`.

## Instalacja z terminala — również OpenATV 8.0

OpenATV 8.0 używa `opkg`. Wersja 0.2.2 dopasowuje kontrole do nowych klas EPG
oraz zapisuje w `.ipk` katalogi i ścieżki `./` w stylu `opkg-build`.
Nie znamy jeszcze komunikatu błędu zgłoszonego dla 0.2.0, więc nie przypisujemy
mu jednej potwierdzonej przyczyny.

Instalacja paczki z GitHuba:

```sh
wget -O /tmp/CanalPL-0.2.2.ipk https://raw.githubusercontent.com/Baniak88/enigma2-skin/main/packages/enigma2-plugin-skins-canalpl_0.2.2_all.ipk &&
opkg install /tmp/CanalPL-0.2.2.ipk
```

Jeśli instalacja pakietu nie powiodła się i CanalPL nie widnieje jako zainstalowana
paczka w `opkg`, można użyć instalacji ręcznej opisanej niżej. Pobiera ona komplet
plików i omija obsługę `.ipk`. Nie potwierdza to działania GUI na danym sprzęcie.
Nie uruchamiaj aktualizacji całego systemu ani opcji wymuszających zależności,
żeby naprawić błąd jednej skórki. Zachowaj dokładny komunikat z terminala.

## Pikony — poprawka 0.2.2

Usunięto zasłanianie pikon przez tło panelu. Enigma2 tworzy dekoracje po
rendererach, dlatego teraz logo ma wyższą warstwę niż grafika zastępcza.
Poprawka dotyczy paska informacji, panelu wybranego kanału i ekranów EPG
korzystających z renderera `Picon`. Obsługa pikonów wewnątrz natywnej listy
kanałów nie została zmieniona.

Jeśli logotypy działały na poprzedniej skórce, aktualizacja zachowa korzystanie
z istniejącej paczki i ustawień OpenATV. Po aktualizacji wykonaj restart GUI.
Jeżeli logo kanału nie zostanie znalezione, widać autorską grafikę zastępczą.

## Pikony i lista kanałów

1. Zainstaluj swoją paczkę pikonów zgodną z listą kanałów. Typowe katalogi:
   `/usr/share/enigma2/picon/`, `/media/usb/picon/`, `/media/hdd/picon/`.
   OpenATV wykrywa katalogi `picon` na zamontowanych nośnikach.
2. Włącz wyświetlanie pikonów w ustawieniach interfejsu i listy kanałów.
3. W ustawieniach listy kanałów wybierz styl ekranu **CanalPL — lista** i szablon
   listy **CanalPL**, następnie włącz pikony. Są to natywne ustawienia OpenATV.
   Po zmianie skórki ustawienia mogą wymagać ponownego wybrania.
4. Jeśli używasz trybu Legacy, włącz jego oddzielne ustawienie pikonów listy.

Logotypy stacji nie są dołączone. Skórka korzysta z natywnego renderera `Picon`
i wyszukiwania po referencji/nazwie kanału. Brakujący plik nie wymaga pobierania
z internetu; w pasku i panelu kanału wyświetli się autorska pikona zastępcza.
Wiersze natywnej listy mogą pozostawić puste miejsce przy braku logo.

Bukiety w liście kanałów otwierasz **niebieskim klawiszem**. Nie trzeba instalować
wtyczki do obsługi bukietów. Skórka nie tworzy ani nie modyfikuje list kanałów.

## EPG

Wybierz preferowany typ przewodnika w ustawieniach EPG OpenATV. Obsługiwane są
zarówno siatka z kolorami, jak i tryb graficzny z teksturami. Kolorowe przyciski
pobierają etykiety i funkcje z systemu. Rozkład przycisków zależy od ustawień pilota.
Pikony w siatce włączasz w ustawieniu sposobu wyświetlania nazw/pikonów kanałów.
Wariant PIG wymaga obsługi podglądu obrazu przez dekoder. Skórka nie dostarcza
danych EPG — pochodzą one z kanału lub skonfigurowanego przez użytkownika źródła.

## Alternatywna instalacja `.tar.gz` lub SFTP

Pobierz [CanalPL-0.2.2.tar.gz](packages/CanalPL-0.2.2.tar.gz), prześlij do `/tmp`:

```sh
mkdir -p /tmp/canalpl-install
cd /tmp/canalpl-install
tar -xzf /tmp/CanalPL-0.2.2.tar.gz
sh install.sh
```

Instalator kopiuje **cały katalog** CanalPL razem z grafikami i szablonem.
Przy aktualizacji zachowuje istniejący katalog jako `CanalPL.backup-...`.
Nie zmienia ustawień użytkownika. Archiwum `.tar.gz` nie jest paczką `opkg`.
Przez SFTP także prześlij cały katalog `CanalPL` do `/usr/share/enigma2/`;
samo `skin.xml` nie wystarczy w tej wersji. Nie mieszaj instalacji ręcznej i `opkg`.

## Powrót do poprzedniej skórki

W menu wybierz poprzednią skórkę i zrestartuj GUI. Jeżeli GUI nie startuje,
zaloguj się przez SSH, zatrzymaj je (`init 4` w obrazach z runlevel), zachowaj
kopię `/etc/enigma2/settings` i usuń z niego wyłącznie wiersz:

```text
config.skin.primary_skin=CanalPL/skin.xml
```

Uruchom GUI (`init 3` w obrazach z runlevel). Zostanie wybrana skórka domyślna.
W obrazach z innym menedżerem usług zastosuj właściwą procedurę restartu GUI.

## Rozwój i kontrole

Python 3.12+; budowanie i kontrola paczek nie wymagają dodatkowych bibliotek:

```sh
python3 scripts/generate_skin.py
python3 scripts/build_assets.py
python3 scripts/validate.py
python3 scripts/preview.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

Pliki wynikowe trafiają do `dist/`. Generowanie podglądów PNG wymaga opcjonalnego
Pillow: `python3 scripts/preview.py --png`. Podglądy SVG nie wymagają Pillow.
Testy sprawdzają strukturę `.ipk`, kompletność plików, instalację i kopię aktualizacji.
Walidator porównuje widgety z zapisanymi kontraktami oficjalnego kodu OpenATV.
To kontrole statyczne/integracyjne, a nie test uruchomienia GUI Enigma2.

Do zgłoszenia problemu dołącz model dekodera, wersję OpenATV, nazwę ekranu i log
błędu. Pliki i grafiki CanalPL: MIT. Nazwa CANAL+ należy do jej właściciela.
