# TvSat 0.3.3 — skórka Enigma2 dla OpenATV

Ciemny interfejs Full HD 1920×1080 inspirowany polskim CANAL+: białe napisy,
zielone zaznaczenie, duże menu, pikony, bukiety i program TV. Projekt niezależny,
bez oficjalnych logotypów i grafik operatora.

**Baza: natywne ekrany i komponenty OpenATV 7.5 / 7.6 / 8.0.** Wersja 0.3.3 zastępuje
wstępną bazę OpenPLi z 0.1.0. Sprawdzono kontrakty widgetów trzech wersji OpenATV,
układy, grafiki, menu, paczki i instalator. **Test na fizycznym dekoderze jest
jeszcze wymagany** — nie deklarujemy potwierdzonej zgodności sprzętowej.

## Poprawki 0.3.3 — czcionki, pasek i instalacja

- Nazwy oraz wartości ustawień korzystają z DejaVu Sans Regular 30 px.
  Ustawiono osobny `valueFont` komponentu ConfigList i domyślne fonty konfiguracji.
- Lista ustawień ma dziesięć pełnych wierszy po 64 px i szersze miejsce na wartości.
  Opis po prawej ma font 28 px, a na dole jest podpowiedź nawigacji.
- Pasek informacji jest lekko jaśniejszy (`#21262c`). Pole pikony i obraz
  zastępczy są przezroczyste, więc nie tworzą osobnego prostokąta.
- Instalacja `.ipk` kończy się komunikatem **TvSat — INSTALACJA ZAKOŃCZONA
  POMYŚLNIE** i przypomnieniem o restarcie GUI. Komunikat drukuje skrypt
  `postinst` wykonywany przez opkg. Instalator ręczny wyświetla ten sam komunikat.
  W systemowym instalatorze treść może być widoczna w jego oknie lub logu.

Jeśli sama pikona PNG ma zapisane nieprzezroczyste tło, pozostanie ono częścią
tego obrazka. Skórka usuwa własne tło; logotypów z Twojej paczki nie zmienia.

![Ustawienia — czytelne nazwy i wartości](docs/setup.svg)

## TvSat — nowa nazwa i miniaturka (0.3.2)

Skórka, nagłówki, style ekranu i szablon listy mają nazwę **TvSat**.
Miniaturka `TvSat/prev.png` jest wyświetlana przez natywny wybór skórek OpenATV.
Przedstawia układ menu z przykładowymi danymi, bez obrazu z tunera.

![Miniaturka TvSat](TvSat/prev.png)

TvSat instaluje się do osobnego katalogu `/usr/share/enigma2/TvSat` i używa paczki
`enigma2-plugin-skins-tvsat`. Wcześniej zainstalowana skórka CanalPL pozostaje
na dekoderze. Po instalacji wybierz **TvSat** w wyborze skórek i zrestartuj GUI.
W ustawieniach listy kanałów wybierz ponownie styl **TvSat — podgląd TV**
i szablon **TvSat**, jeśli poprzednio były ustawione warianty CanalPL.

## Układ listy kanałów — 0.3.0

- Domyślna lista oraz wariant `ChannelSelection_PIG` mają podgląd TV 640×360,
  czyli 16:9. Natywny renderer `Pig` pokazuje aktualnie odtwarzany kanał.
- Opis zaznaczonej audycji znajduje się pod podglądem. Nie trzeba zasłaniać go
  pełnym tekstem; klawisz INFO otwiera pełny opis.
- Czcionka interfejsu to DejaVu Sans Regular (`TvSatText`), z osobnym krojem
  dla mocniejszych nagłówków. Oba pliki fontów dostarcza OpenATV.
- Zaznaczenie jest ciemnozielone z białym tekstem i zielonym paskiem w szablonie
  TvSat. Nazwa kanału i tytuł audycji są w oddzielnych liniach.
- Dostępny jest także wariant **TvSat — bez podglądu**.

**Aby uzyskać osiem wierszy jak na podglądzie:** w ustawieniach listy kanałów
wybierz styl ekranu **TvSat — podgląd TV** (lub **TvSat — standard z TV**)
i szablon listy **TvSat**. Włącz pikony listy i zatwierdź zmiany.
W liście kanałów menu ustawień otwierasz klawiszem MENU; nazwy pozycji zależą
od tłumaczenia OpenATV. Po aktualizacji skórki wykonaj restart GUI.

Tryb **Legacy** nadal korzysta z ustawionej w OpenATV liczby wierszy i sposobu
wyświetlania informacji. Skórka poprawia w nim fonty, kontrast i podgląd, ale nie
nadpisuje preferencji użytkownika. Jeżeli chcesz zachować Legacy, wybierz w jego
ustawieniach osiem wierszy, dwie linie i zerowe korekty rozmiaru czcionek.

Podgląd TV pokazuje kanał oglądany; przesuwanie kursora zmienia opis zaznaczonej
audycji. Przełączanie obrazu odbywa się standardowymi klawiszami OpenATV.
Obsługa podglądu zależy od sterownika wideo urządzenia. Wariant bez podglądu
pozostawia pełny panel informacji.

## Poprawki 0.3.1 — pikony i niebieski przycisk

- Usunięto plus z `picon_default.png`. Pod przezroczystymi fragmentami logotypów
  znajduje się neutralne tło, które nie zawiera znaku ani innej grafiki.
- Niebieski przycisk otwiera natywny **QuickMenu**. Ekran ma teraz układ TvSat:
  pełny nagłówek, dwie czytelne kolumny, regularne fonty i wspólny pasek przycisków.
- Powiększono wiersze i faktyczny font komponentu ChoiceList, z którego korzysta
  m.in. wybór nośnika do skanowania. To osobne ustawienie od fontu okna dialogowego.

Po aktualizacji wykonaj restart GUI, aby odświeżyć obrazy oraz aliasy fontów.
Układ nie zmienia działania przycisków ani operacji dostępnych w szybkim menu.

## Podglądy

Wizualizacje powstają z układu XML i przykładowych danych. Listy, tytuły i pikony
w podglądach są przykładowe; nie są zrzutami z działającego odbiornika. Liczba
wierszy i rozmiary fontów na dekoderze zależą także od ustawień OpenATV.
Pole TV na wizualizacji jest symboliczne; nie zawiera obrazu z tunera.

![Menu główne](docs/menu.svg)
![Szybkie menu — niebieski przycisk](docs/quickmenu.svg)
![Wybór nośnika](docs/choices.svg)
![Lista kanałów z pikonami](docs/channels.svg)
![Wybór bukietów](docs/bouquets.svg)
![Graficzne EPG](docs/epg.svg)
![Pasek informacji](docs/infobar.svg)

## Co obejmuje

- Menu główne, QuickMenu z niebieskiego przycisku, podmenu i opisy.
- Lista kanałów i radia, wybór bukietów i wariant z podglądem TV.
- Pikona bieżącego i zaznaczonego kanału; natywne pikony w liście i EPG.
- EPG pojedyncze, multi, graficzna siatka, PIG, szybkie i pionowe; bukiety w EPG.
- Opis audycji, programowanie nagrania, przegląd timerów.
- Lista nagrań, odtwarzacz, pauza/przewijanie i stan timeshiftu.
- Ustawienia, dźwięk/napisy, wtyczki lista/siatka i podstawowe okna dialogowe.

Łącznie 42 definicji ekranów. Specjalistyczne ekrany i zewnętrzne wtyczki mogą
korzystać z układu systemowego. Pełny zakres, źródła API i lista testów sprzętowych:
[COMPATIBILITY.md](docs/COMPATIBILITY.md).

## Instalacja `.ipk` — OpenATV

Pobierz [enigma2-plugin-skins-tvsat_0.3.3_all.ipk](packages/enigma2-plugin-skins-tvsat_0.3.3_all.ipk)
przyciskiem pobierania pliku na GitHubie. Prześlij go przez SFTP do `/tmp` dekodera:

```sh
opkg install /tmp/enigma2-plugin-skins-tvsat_0.3.3_all.ipk
```

Następnie wybierz **TvSat** w ustawieniach interfejsu / wyborze skórki i zatwierdź
restart GUI. Dokładne nazwy menu zależą od tłumaczenia i wydania OpenATV.
Pakiet nie przełącza skórki ani nie restartuje dekodera automatycznie.
Aktualizacjami i usuwaniem wersji `.ipk` zarządza `opkg`.

## Instalacja z terminala — również OpenATV 8.0

OpenATV 8.0 używa `opkg`. Paczka jest zgodna z formatem tego menedżera.

Instalacja paczki z GitHuba:

```sh
wget -O /tmp/TvSat-0.3.3.ipk https://raw.githubusercontent.com/Baniak88/enigma2-skin/main/packages/enigma2-plugin-skins-tvsat_0.3.3_all.ipk &&
opkg install /tmp/TvSat-0.3.3.ipk
```

Jeśli instalacja pakietu nie powiodła się i TvSat nie widnieje jako zainstalowana
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
Jeżeli logo kanału nie zostanie znalezione, pozostaje neutralne pole bez symboli.

## Pikony i lista kanałów

1. Zainstaluj swoją paczkę pikonów zgodną z listą kanałów. Typowe katalogi:
   `/usr/share/enigma2/picon/`, `/media/usb/picon/`, `/media/hdd/picon/`.
   OpenATV wykrywa katalogi `picon` na zamontowanych nośnikach.
2. Włącz wyświetlanie pikonów w ustawieniach interfejsu i listy kanałów.
3. W ustawieniach listy kanałów wybierz styl ekranu **TvSat — podgląd TV** i szablon
   listy **TvSat**, następnie włącz pikony. Są to natywne ustawienia OpenATV.
   Po zmianie skórki ustawienia mogą wymagać ponownego wybrania.
4. Jeśli używasz trybu Legacy, włącz jego oddzielne ustawienie pikonów listy.

Logotypy stacji nie są dołączone. Skórka korzysta z natywnego renderera `Picon`
i wyszukiwania po referencji/nazwie kanału. Brakujący plik nie wymaga pobierania
z internetu; w pasku i panelu kanału pozostanie neutralne tło.
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

Pobierz [TvSat-0.3.3.tar.gz](packages/TvSat-0.3.3.tar.gz), prześlij do `/tmp`:

```sh
mkdir -p /tmp/tvsat-install
cd /tmp/tvsat-install
tar -xzf /tmp/TvSat-0.3.3.tar.gz
sh install.sh
```

Instalator kopiuje **cały katalog** TvSat razem z grafikami i szablonem.
Przy aktualizacji zachowuje istniejący katalog jako `TvSat.backup-...`.
Nie zmienia ustawień użytkownika. Archiwum `.tar.gz` nie jest paczką `opkg`.
Przez SFTP także prześlij cały katalog `TvSat` do `/usr/share/enigma2/`;
samo `skin.xml` nie wystarczy w tej wersji. Nie mieszaj instalacji ręcznej i `opkg`.

## Powrót do poprzedniej skórki

W menu wybierz poprzednią skórkę i zrestartuj GUI. Jeżeli GUI nie startuje,
zaloguj się przez SSH, zatrzymaj je (`init 4` w obrazach z runlevel), zachowaj
kopię `/etc/enigma2/settings` i usuń z niego wyłącznie wiersz:

```text
config.skin.primary_skin=TvSat/skin.xml
```

Uruchom GUI (`init 3` w obrazach z runlevel). Zostanie wybrana skórka domyślna.
W obrazach z innym menedżerem usług zastosuj właściwą procedurę restartu GUI.

## Rozwój i kontrole

Python 3.12+; budowanie i kontrola paczek nie wymagają dodatkowych bibliotek:

```sh
python3 scripts/generate_skin.py
python3 scripts/build_assets.py
python3 scripts/validate.py
python3 scripts/check_upstream_fonts.py --download
python3 scripts/preview.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

Pliki wynikowe trafiają do `dist/`. Generowanie podglądów PNG wymaga opcjonalnego
Pillow: `python3 scripts/preview.py --png --thumbnail`. Podglądy SVG nie wymagają Pillow.
Testy sprawdzają strukturę `.ipk`, kompletność plików, instalację i kopię aktualizacji.
Walidator porównuje widgety z zapisanymi kontraktami oficjalnego kodu OpenATV.
GitHub Actions generuje pliki, wykonuje testy i buduje paczki. Po udanym teście
na głównej gałęzi zapisuje wynikowe pliki skórki, podglądy i paczki w repozytorium.
Publikacja nie jest wykonywana dla pull requestów. To kontrole
statyczne/integracyjne, a nie test uruchomienia GUI Enigma2.

Do zgłoszenia problemu dołącz model dekodera, wersję OpenATV, nazwę ekranu i log
błędu. Pliki i grafiki TvSat: MIT. Nazwa CANAL+ należy do jej właściciela.
