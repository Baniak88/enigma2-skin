# OpenATV — zakres zgodności 0.3.0

Układy CanalPL są autorskie. Nazwy ekranów, widgetów i formaty list sprawdzono
w oficjalnym kodzie [openatv/enigma2](https://github.com/openatv/enigma2).
Nie wykorzystujemy kodu, grafiki ani rendererów skórek z forum LinuxSat.
Forum posłużyło jako punkt odniesienia dla zakresu typowej skórki Enigma2.

## Wersje odniesienia

- [OpenATV 7.5](https://github.com/openatv/enigma2/tree/29c41504a2bdecd764d54373109e3c692810b189)
- [OpenATV 7.6](https://github.com/openatv/enigma2/tree/e42a0ffb0064962321bf500999ac2bc48cadec34)
- [OpenATV 8.0](https://github.com/openatv/enigma2/tree/39f548521c4c3a667348139720ebe3bf3ac3cf22)

Kontrakty w `scripts/openatv-contracts.json` zapisują nazwy i typy komponentów,
wymagane widgety oraz SHA-256 analizowanych plików. Powstają przez odczyt AST
źródeł Pythona, bez ich wykonywania. Listy i źródła tworzone warunkowo są w nim
zebrane łącznie; sam kontrakt nie dowodzi działania każdego warunku na urządzeniu.
Kontrole nie uruchamiają GUI Enigma2, nie odtwarzają telewizji i nie zastępują
testów na dekoderze. Status: **dopasowana do API 7.5/7.6/8.0, test sprzętowy oczekuje**.
Starsze OpenATV, OpenPLi, VTi i DreamOS nie są celem tego wydania.

Oryginalny `TemplatedMultiContent` z trzech gałęzi przyjął również 9 kombinacji
szablonu/stylu menu, wtyczek i wyboru dźwięku. W tej próbie zastąpiono warstwę C++
stubem; sprawdzono inicjalizację, zmianę stylu i indeksy pól. Można ją powtórzyć
poleceniem `python3 scripts/check_upstream_templates.py <katalog-checkoutów>`.

## Ekrany

| Obszar | Nazwy ekranów |
| --- | --- |
| Menu | Menu (tryby default, text, number, image, both) |
| Kanały | ChannelSelection, ChannelSelection_PIG, ChannelSelectionRadio, SimpleChannelSelection, SlimChannelSelection, ChannelSelection_NoPIG |
| Bukiety | BouquetSelector, EPGBouquetSelector, lista bukietów wewnątrz EPG |
| EPG | EPGSelection, EPGSelectionMulti, QuickEPG, GraphicalEPG, GraphicalEPGPIG, GraphicalInfoBarEPG, EPGvertical, EPGverticalPIG |
| Audycja | EventView, InfoBarEventView |
| Ustawienia | Setup, AudioSelection, QuickSubtitlesConfigMenu |
| Nagrania | MovieSelection, MovieSelectionSlim, MoviePlayer |
| Timery | RecordTimerOverview, TimerOverview, TimerEditList |
| Wtyczki | PluginBrowserList, PluginBrowserGrid |
| Okna | BouquetSelector, ChoiceBox, ChannelContextMenu, MessageBox, MessageBoxSimple |
| Odtwarzanie | InfoBar, SecondInfoBar, PVRState, TimeshiftState, NumberZap, Volume, Mute |

Specjalistyczne ekrany, np. strojenie tunerów, konfiguracja sieci, klawiatura
wirtualna, kreatory i ekrany wtyczek zewnętrznych, nadal korzystają z systemowych
definicji. Mogą mieć inny układ niż 41 ekranów CanalPL.

## Ważne różnice względem 0.1.0

- Tytuły korzystają ze źródła `Title` z `Screen`, zgodnie z OpenATV.
- Kolorowe przyciski `StaticText` są renderowane przez `source` / `Label`.
- Menu obsługuje format krotki OpenATV i wszystkie jego standardowe style listy.
- Graficzne EPG ma `timeline_text`, sześć linii czasu, linię teraz i `bouquetlist`.
- Wariant graficzny EPG otrzymuje wymagane tekstury `epg/*.png`, również dla
  nagrywania, zaznaczenia i czasu przeszłego. Wariant tekstowy używa kolorów XML.
- Nowy silnik ServiceList korzysta z `skinTemplates.xml` z trybami services,
  bouquets i other. Starszy tryb listy nadal używa natywnego ServiceListLegacy.
- Obowiązkowe pola Setup i MessageBox są obecne. Pola opcjonalne mają `conditional`.
- MovieSelection zachowuje instancję `DescriptionBorder`, do której odwołuje się
  kod systemu, oraz obiekty sortowania i zachowania po zakończeniu odtwarzania.

## Test na odbiorniku

1. Sprawdź start GUI po wyborze skórki; zachowaj dostęp SSH do przywrócenia ustawień.
2. Otwórz menu i podmenu w każdym używanym stylu menu. Sprawdź długie polskie nazwy.
3. W liście kanałów otwórz bukiety niebieskim klawiszem. Sprawdź kilka bukietów,
   tryb radia i pusty bukiet. Sprawdź tryb Legacy oraz szablon CanalPL.
4. Sprawdź pikonę bieżącego i zaznaczonego kanału, pikonę w liście i brak logo.
5. Otwórz EPG pojedyncze, multi, graficzne tekstowe, graficzne z teksturami,
   wariant PIG i pionowe. Zmień bukiet i dzień, otwórz opis i dodaj timer.
6. Sprawdź kanał bez EPG, długie opisy, brak sygnału i listę nagrań bez plików.
7. Sprawdź nagrywanie, odtwarzanie, pauzę, przewijanie, timeshift i wyciszenie.
8. Sprawdź ustawienia, komunikat tak/nie oraz przeglądarkę wtyczek lista/siatka.

Rozdzielczość framebufferu: 1920×1080. Wynik na sprzęcie zależy od ustawień liczby
wierszy, rozmiarów fontów, szerokości nazw kanałów i obsługi PIG danego dekodera.

## Poprawki 0.2.1 po zgłoszeniu z OpenATV 8.0

- Mapowanie kontraktów uwzględnia rozdzielenie EPG na klasy Single, Multi, Grid
  oraz Vertical w OpenATV 8.0. Odczyt AST obejmuje też widgety tworzone w pętlach.
- Pole wyboru numeru w EPG jest opcjonalne (`conditional="number"`), ponieważ
  wariant siatki OpenATV 8.0 nie tworzy tego pola.
- Kontenery `.ipk` mają teraz jawne katalogi i nazwy `./control`, `./usr/...`.
  Te kontrole nie zastępują próby instalacji przez `opkg` na odbiorniku.
- Bez pełnego błędu instalacji z dekodera przyczyna pierwotnego zgłoszenia
  pozostaje niepotwierdzona. Format pakietu i zgodność GUI są osobnymi kwestiami.

## Poprawka 0.2.2 — zasłonięte pikony

Zgłoszenie zawierało zdjęcie pustego panelu w InfoBar oraz potwierdzenie, że
pikony działały na poprzedniej skórce. W poprzednim XML dekoracyjne tło i renderer
Picon miały domyślne zPosition=0. `Screen.createGUIScreen` tworzy renderery przed
`additionalWidgets`, a `eWidget::insertIntoParent` wstawia późniejsze elementy
za istniejącymi o tej samej warstwie. Tło zasłaniało obrazek.

Teraz renderer ma zPosition=1, a jawna, skalowana grafika zastępcza zPosition=0.
Test regresji wykrywa pierwotny układ. Walidator sprawdza zasłanianie prostokątów
pikon przez dekoracje na wszystkich ekranach. Oryginalne klasy Picon z 7.5, 7.6
oraz 8.0 przeszły próby znalezionego/brakującego logo, wyłączenia pikon i
wyczyszczenia źródła z zastąpioną warstwą C++:
`python3 scripts/check_upstream_picons.py <katalog-checkoutów>`.
Nie jest to uruchomienie interfejsu na fizycznym dekoderze.

## Układ i podgląd 0.3.0

Domyślny ChannelSelection ma teraz natywny `session.VideoPicture` / `Pig`.
Wcześniej to okno było obecne wyłącznie w oddzielnym wariancie PIG. Podgląd ma
rozmiar 640×360, osobne miejsce na nazwę oglądanego kanału oraz panel opisu
zaznaczonej audycji. Dodano ChannelSelection_NoPIG jako wariant bez wideo.

Fonty `CanalText` i `CanalStrong` wskazują odpowiednio DejaVuSans.ttf oraz
LiberationSans-Bold.ttf dostarczane przez Enigma2 (`data/fonts/Makefile.am` w
7.5, 7.6, 8.0). Nie redefiniujemy globalnego fontu Regular dla obcych wtyczek.
Szablon CanalPL ma 88-pikselowe wiersze w liście o wysokości 704 pikseli,
co daje osiem wierszy. W Legacy wysokość wiersza oblicza system na podstawie
ustawień użytkownika; nie można wymusić ośmiu wierszy samym serviceItemHeight.

Testy sprawdzają obecność podglądu w obu standardowych wariantach, brak
zasłaniających dekoracji w oknie wideo, proporcje 16:9, fonty, rozdzielenie
nazwy/tytułu, kontrast zaznaczenia i wariant bez wideo. Oryginalny Pig z OpenATV
8.0 przeszedł próbę decoder=0, geometrii i przywracania pełnego ekranu ze stubem
sterownika (`scripts/check_upstream_video.py`). Nadal potrzebny jest test obrazu
na rzeczywistym urządzeniu. Nie zmieniamy mapowania pilota ani trybu przełączania
kanałów przy przesuwaniu kursora.
