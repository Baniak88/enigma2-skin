# OpenATV — zakres zgodności 0.4.5

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
definicji. Mogą mieć inny układ niż 59 ekranów TvSat.

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

## Interfejs 0.4.0 — instalacja i wspólna paleta

Dodano IpkgInstaller, Opkg, Console, Processing, PackageAction/PluginAction,
PackageActionLog/PluginActionLog oraz MessageBoxModal — razem 51 ekranów.
IpkgInstaller występuje w rdzeniu przypiętego OpenATV 8.0; w kontraktach 7.5/7.6
jest jawnie oznaczony jako niedostępny. Nie deklarujemy sprawdzenia starszych
zewnętrznych instalatorów. Audyt AST rozpoznaje także przypisania przez atrybut
(np. self['list'] = self.selectionList), bez wykonywania kodu systemowego.

Alias SelectionList 30/72 i parametry SelectionListDescr/Lock ustawiają faktyczny
font, wysokość wiersza i pola zaznaczenia. Oryginalna klasa SelectionList we
wszystkich trzech wersjach przechodzi próbę zaznaczania pojedynczego pakietu,
odwracania zaznaczeń i odczytu właściwych ścieżek.

ProcessingScreen.setDescription zmienia rozmiar okna i etykiety. Wszystkie stałe
elementy umieszczono nad opisem. Próba oryginalnej metody sprawdza krótki i długi
opis; nie uruchamia prawdziwego renderera C++. W natywnych StaticText oraz
ConditionalShowHide sprawdzono również ukrywanie obu części pustej funkcji
klawisza (znacznika i podpisu). Polecenie:
`python3 scripts/check_upstream_install_ui.py --download`.

Nowy kolor paska #3b4654 ma test zauważalnej różnicy jasności względem wydania
0.3.3 i głównego tła. Test wymaga również kontrastu białego tekstu co najmniej
7:1. Są to kontrole palety, nie pomiary jasności telewizora.

Opkg zachowuje własne etykiety statusu, liczbę błędów i przełączanie dziennika.
Nie zmieniono uruchamianych poleceń ani działania instalacji/odinstalowania.
TemplatedMultiContent przyjmuje obecnie 13 kombinacji szablonów/stylów na wersję,
w tym 12-polowe wiersze PackageAction. Test na dekoderze pozostaje wymagany.

## FileCommander 0.4.1

Dodano pięć ekranów: FileCommander, FileCommanderContextMenu, FileCommanderData,
FileCommanderFileViewer oraz FileCommanderTextEditor — razem 56 definicji.
Źródłem kontraktów jest FileCommander z przypiętych źródeł OpenATV: plugin.py
w 7.5/7.6 oraz ui.py w 8.0. Żaden plik wykonywalny wtyczki nie jest zastępowany.

Nagłówki mają 27-polowy natywny format danych i korzystają z indeksów 17 (ścieżka),
1 (uprawnienia), 11 (rozmiar), 13 (czas modyfikacji). Alias FileList/FileListMulti
ustawia 28 px i 64 px wysokości; pozycje ikon i tekstu mieszczą się w panelu 864 px.
Zmiana tych natywnych aliasów obejmuje również inne listy korzystające z FileList.

Testy oryginalnego kodu potwierdzają generowanie wierszy w obu trybach, wybór
i odznaczanie plików, przełączanie aktywnego panelu oraz rzeczywiste dane nagłówków
z pliku tymczasowego. Krój andale.ttf jest sprawdzany w Makefile fontów każdej
przypiętej wersji. Polecenie: `python3 scripts/check_upstream_filecommander.py --download`.
Warstwa C++ jest zastąpiona, a operacje kopiowania, przenoszenia i usuwania nie są
uruchamiane przez te próby. TemplatedMultiContent przyjmuje 15 kombinacji na wersję.

Kontrole geometrii sprawdzają osiem pełnych wierszy, równe panele, brak zasłaniania
list przez status i zachowanie kroju monospace w podglądzie/edytorze. Nadal potrzebny
jest test na dekoderze. Wtyczki FileCommander spoza OpenATV mogą używać innego API.

## Przezroczystość i układy 0.4.2

Zmieniono kolor overlay na #660c0e10. Enigma2 stosuje odwrotne znaczenie kanału
alfa: 00 oznacza nieprzezroczystość, ff pełną przezroczystość. Tło paska ma 40%
przezroczystości i 60% krycia; renderery pikon i przezroczysty PNG nie dodają
oddzielnej powierzchni. Biały tekst zachowuje testowany kontrast co najmniej 4.5:1
po zmieszaniu nawet z białą klatką testową. Globalna przezroczystość OSD i telewizor
pozostają ustawieniami użytkownika — nie są zmieniane przez paczkę.

Podgląd SVG zapisuje rzeczywiste fill-opacity, a renderer PNG składa kolory
z zachowaniem alfa. Test odczytuje piksele wygenerowanego PNG nad różnymi
kolorami tła oraz w polu pikony; poprzedni podgląd pomijał kanał alfa.

PluginBrowserGrid ma cztery kolumny 448 px i trzy wiersze 228 px. Wewnętrzne
karty i powiększone ikony zachowują odstępy, opis jest pod siatką. Prostokąt
karty korzysta z natywnego MultiContentEntryRectangle, a oryginalne konwertery
trzech wersji nadal przyjmują 15 kombinacji szablonów/stylów z C++ zastąpionym.

Panel wybranej audycji pod PIG ma wyższe pole opisu i osobną podpowiedź INFO.
Długie opisy nadal mają dostęp do pełnego widoku pod INFO; nie gwarantujemy
zmieszczenia całego EPG w panelu. VERSION jest dołączony do obu archiwów,
a skrypty końcowe podają faktycznie zainstalowany numer. Przebudowane testy
sprawdzają wersję w IPK oraz w komunikatach instalacji. Test sprzętowy oczekuje.

## Ustawienia skórki 0.4.3

Dodano SkinSelection oraz jego natywne nazwy rezerwowe setup_Skin i SetupSkin
(łącznie 59 definicji). Sterownik to Screens/SkinSelection.py z powyższych
przypiętych commitów. Dziedziczy Setup, ale wymaga też Pixmap `preview`:
layoutFinished bezwarunkowo odczytuje rozmiar jej instancji. Podgląd ma warstwę 1,
aby dekoracje utworzone później przez Screen nie zasłoniły miniatury.

`python3 scripts/check_upstream_skinselection.py --download` wykonuje oryginalne
fragmenty Setup i readSkin, sprawdza pierwszeństwo wszystkich trzech nazw oraz
oryginalne layoutFinished/loadPreview. Test potwierdza ładowanie TvSat/prev.png,
wymiary dekodera 608×342 i ukrywanie podglądu po wybraniu opcji czcionki.
C++ ePicLoad/Pixmap jest zastąpione atrapami; test nie potwierdza renderowania
na odbiorniku. Nie uruchamia createItems, keySave ani przeładowania GUI.
Pasek zachowuje ciemny kolor i 40% przezroczystości z 0.4.2.

## Powrót do pierwotnych kolorów 0.4.4

Kolory powierzchni pochodzą z CanalPL/skin.xml z pierwszego wydania,
commit 9ce5d21c37bf031c92dbf4ef6adf2ef461e3dcc9: tło #000c0e10,
panel #0017191c, linia #00303438 i nakładka #180c0e10.
Enigma2 traktuje bajt alpha jako przezroczystość: 0x18/255 = 9,41%,
czyli 90,59% krycia, zamiast 40% w 0.4.2–0.4.3. Zmiana dotyczy InfoBar,
SecondInfoBar i MoviePlayer; menu pozostają nieprzezroczyste. Pikony zachowują
przezroczyste tło i nie mają osobnej powierzchni.

Te same kolory paneli i linii mają natywne szablony kart wtyczek oraz PNG.
Test mieszania kolorów SVG/PNG sprawdza wynik także w obszarze pikony,
a test ustawień kontrast tekstu na białym, czarnym, czerwonym i niebieskim obrazie.
Zmiana nie ingeruje w Python dekodera, ustawienia użytkownika ani układy.

## Korekta przezroczystości 0.4.5

Nakładka ma kolor #260c0e10. Bajt 0x26 daje 38/255 = 14,90%
przezroczystości i 85,10% krycia w InfoBar, SecondInfoBar i MoviePlayer.
Pierwotne kolory tła i paneli z 0.4.4 pozostają bez zmian. Menu pozostają
nieprzezroczyste. Istniejące testy sprawdzają mieszanie SVG/PNG także pod pikoną
oraz kontrast napisów na różnych kolorach obrazu telewizyjnego.
