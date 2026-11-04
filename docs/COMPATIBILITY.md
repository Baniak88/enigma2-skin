# OpenATV — zakres zgodności 0.3.3

Układy TvSat są autorskie. Nazwy ekranów, widgetów i formaty list sprawdzono
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
| Menu | Menu (tryby default, text, number, image, both), QuickMenu |
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
definicji. Mogą mieć inny układ niż 42 ekranów TvSat.

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
   tryb radia i pusty bukiet. Sprawdź tryb Legacy oraz szablon TvSat.
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

Fonty `TvSatText` i `TvSatStrong` wskazują odpowiednio DejaVuSans.ttf oraz
LiberationSans-Bold.ttf dostarczane przez Enigma2 (`data/fonts/Makefile.am` w
7.5, 7.6, 8.0). Nie redefiniujemy globalnego fontu Regular dla obcych wtyczek.
Szablon TvSat ma 88-pikselowe wiersze w liście o wysokości 704 pikseli,
co daje osiem wierszy. W Legacy wysokość wiersza oblicza system na podstawie
ustawień użytkownika; nie można wymusić ośmiu wierszy samym serviceItemHeight.

Testy sprawdzają obecność podglądu w obu standardowych wariantach, brak
zasłaniających dekoracji w oknie wideo, proporcje 16:9, fonty, rozdzielenie
nazwy/tytułu, kontrast zaznaczenia i wariant bez wideo. Oryginalny Pig z OpenATV
8.0 przeszedł próbę decoder=0, geometrii i przywracania pełnego ekranu ze stubem
sterownika (`scripts/check_upstream_video.py`). Nadal potrzebny jest test obrazu
na rzeczywistym urządzeniu. Nie zmieniamy mapowania pilota ani trybu przełączania
kanałów przy przesuwaniu kursora.

## Poprawki 0.3.1 — bez plusa i nowe QuickMenu

Na zdjęciu użytkownika przez przezroczyste logo Polsat prześwitywał plus z pliku
picon_default.png. Obraz zastępczy jest teraz jednolitym neutralnym tłem. Test
pikseli PNG sprawdza, że plik nie zawiera kolorowego symbolu. Warstwy pikon
pozostają takie jak w poprawce 0.2.2.

Dodano QuickMenu zgodnie z kodem Screens/QuickMenu.py w 7.5, 7.6 i 8.0. Jego
mainlist ma krotkę (nazwa, podtytuł, ikona), a sublist (nazwa, podtytuł).
Szablony konwertera sprawdzono z trzema wersjami upstream: razem 11 kombinacji
szablonu/stylu na wersję. Zachowano aktywną kolumnę i funkcje kolorowych przycisków.

ChoiceBox ma osiem wierszy po 72 piksele. Alias ChoiceList ustawia faktyczny font
TvSatText 30 w komponencie ChoiceList, a parametry ChoicelistName/NameSingle/Icon
ustalają pozycje zawartości. Oryginalne ChoiceList i ChoiceEntryComponent z trzech
wersji przeszły próbę konstruktora i geometrii wiersza z zastąpioną warstwą C++
(`scripts/check_upstream_choices.py`). Same atrybuty font/itemHeight na widżecie
nie wystarczały do zmiany fontu listy wieloelementowej.

## Nazwa i miniaturka — 0.3.2

Katalog, nazwa paczki, style listy i nagłówki używają nazwy TvSat. Miniaturka
`TvSat/prev.png` ma rozmiar 640×360 i format RGBA PNG. Jest generowana z podglądu
menu; natywny `Screens/SkinSelection.py` z OpenATV 8.0 wyszukuje `prev.png`
w katalogu wybranej skórki. Starsza instalacja CanalPL nie jest usuwana ani
automatycznie przełączana. Po instalacji wybierz TvSat i jego szablon listy.

## Poprawki 0.3.3 — ustawienia, przezroczyste pikony i potwierdzenie instalacji

Natywny ConfigList pobiera font nazwy i font wartości niezależnie. Dotychczas
skórka ustawiała jedynie `font`, więc wartości po prawej dziedziczyły mały
font domyślny. Dodano `valueFont=TvSatText;30` do trzech widżetów config oraz
domyślne entryFont/valueFont/headerFont w windowstyle/configList. Nazwy i wartości
mają regularny krój 30 px. Setup zawiera dziesięć pełnych wierszy 64 px.
`scripts/check_upstream_fonts.py` wykonuje oryginalny setter valueFont
z przypiętych źródeł 7.5/7.6/8.0 przy zastąpionym C++ i ładowaniu fontów.

InfoBar i SecondInfoBar dziedziczą nieprzezroczyste tło #21262c. Renderer Picon
ma przezroczyste tło, a picon_default.png zawiera wyłącznie przezroczyste piksele.
Test regresji sprawdza kanał alfa każdego piksela i atrybuty renderera.
Nieprzezroczyste tło zapisane w zewnętrznym logo PNG pozostaje częścią tego pliku.

Pakiet ma wykonywalny skrypt control/postinst (0755). Test wydobywa ten skrypt
z rzeczywistego IPK, sprawdza błąd przy brakującym payloadzie, następnie rozpakowuje
payload do katalogu testowego i wykonuje hook ze standardowym IPKG_INSTROOT.
Komunikat sukcesu pojawia się dopiero po obecności plików. Test ręcznej instalacji
sprawdza również komunikat sukcesu oraz jego brak po błędzie. Nie restartujemy
GUI ani nie zmieniamy ustawionej skórki automatycznie.

GitHub Actions generuje układy i grafiki, wykonuje testy, buduje paczki oraz
publikuje zweryfikowane wyniki na main. Fizyczny dekoder nadal wymaga sprawdzenia.
