# OpenATV — zakres zgodności 0.6.6

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
definicji. Mogą mieć inny układ niż 62 ekrany TvSat.

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

## UI/UX 0.5.0 — Standard, Large i własne moduły

Oba warianty mają po 62 definicje. Nowe: TvSatSettings (pasywna wtyczka pakietu),
ConflictTimerOverview i TimerSanityConflict (natywny ConflictTimerOverview).
TvSatLarge ma większe fonty, wyższe wiersze, mniej wpisów i własną miniaturę.
Ma również kopię ikon, ponieważ natywne komponenty szukają ich względem aktywnej
skórki. Nazwy fontów bazują na czcionkach dostarczanych przez OpenATV.

Szablony serviceList używają native index Number/ServiceName/Title1/Picon/Progress,
zapewniają pełny układ w modes services i bouquets. Używają horizontalAlignment,
verticalAlignment, wrap=ellipsis i scale=scaleCenter — atrybutów prawdziwego
TemplateParser, nie aliasów zwykłego Label. Nowy test
`python3 scripts/check_upstream_service_ui.py --download` wykonuje oryginalne
TemplateParser, parseScale i ServiceListTemplateParser z trzech przypiętych wersji;
geometry/fonts/colors/C++ są zastąpione atrapami. Sprawdza indeksy, obie listy,
wyśrodkowanie, wielokropek i flagi skalowania pikon. Nie sprawdza dekodera C++.

Starszy silnik nadpisuje wysokość wiersza na podstawie ustawień. Profil Standard
stosuje osiem wierszy (natywne minimum dla jednej linii), a Large sześć w dwóch
liniach. Kolumna nazwy ma 425 px, wartość dozwoloną przez natywne wybory co 25 px.
Progress type to barright. Zalecany nowszy szablon ma siedem / sześć wierszy.
Ustawienia EPG itemsperpage=0 pozwalają zadziałać skórkowej liczbie wierszy.

Własne moduły runtime:
- Plugins/Extensions/TvSatSettings: jedyne wejście WHERE_PLUGINMENU, bez autostartu.
  Sam import i Anuluj nie modyfikują ustawień. Dopiero Zapisz ustawia profil,
  zapisuje configfile i proponuje restart GUI. Nie zmienia bukietów ani timerów.
- Components/Converter/TvSatEventRemaining.py: odpytuje czas co 30 s, liczy
  pozostałe minuty z rzeczywistego początku i długości audycji, pomija brak EPG,
  audycje przyszłe i zakończone. Nie używa zależnego od preferencji RemainingToText.
- Components/Renderer/TvSatSummary.py: mierzy wysokość zawiniętego tekstu przez
  eLabel.calculateSize, skraca do pełnych słów i wielokropka. Nie zmienia źródła
  opisu, więc INFO nadal ma pełny tekst. Test pomiaru C++ używa atrapy.

Wyniki instalacji i błędy nadal pochodzą z natywnego Opkg. Odmienne stany pokazano
na podglądach z przykładowymi danymi. Istniejące akcje OK/EXIT pozostają natywne;
nie deklarujemy zmiany globalnej mapy klawiszy Enigma2. Timery i konflikty są
obsługiwane przez OpenATV, z czytelnym układem i różnymi ikonami.

IPK zawiera obie skórki i własne moduły Pythona. Nie nadpisuje modułów systemowych.
Manualny instalator przygotowuje wszystkie kopie, zachowuje poprzednie pliki
i przywraca je przy błędzie, co sprawdza test z wymuszoną awarią zapisu.
Oba warianty przechodzą walidację kontraktów i geometrii. Niezbędna jest jeszcze
próba na fizycznym odbiorniku, szczególnie renderowania fontów, pomiaru opisu,
przełączania profilu i restartu GUI podczas nagrywania.

## Fade i detale 0.6.0

InfoBar, SecondInfoBar i MoviePlayer mają przezroczyste okno oraz statyczną
warstwę PNG z zPosition=-10. Gradient alpha rośnie od 0 do 217 na pierwszych
64 pikselach, następnie pozostaje równy 217 (około 85% krycia). Okno jest wyższe
o 64 px i zaczyna się o tyle wcześniej; bezwzględne pozycje treści na ekranie
pozostają zachowane. Wszystkie pola tekstu znajdują się poniżej przejścia fade.
To gradient tła; animacja pojawiania okna pozostaje po stronie ustawień OpenATV.

Maska ma szerokość jednego piksela i jest rozciągana przez natywny ePixmap.
Oddzielne niskie warstwy mieszczą zanikający akcent, delikatną poświatę i podkład
TERAZ. Picon i napisy pozostają nad nimi. Standard i Large używają tych samych
masek i natywnej obsługi alpha. Nie dodano modułów runtime ani stałego timera.

Testy sprawdzają monotoniczny gradient, 15% przezroczystości pod tekstem i pikoną,
bezpieczną kolejność warstw oraz kompozycję SVG/PNG na kolorowym obrazie testowym.
Podgląd PNG składa obrazy przez alpha_composite w RGBA. Test na fizycznym
odbiorniku jest nadal wymagany, szczególnie poprawności mieszania alpha w OSD.

## Margines pikon i fade EventView — 0.6.1

W InfoBar przesunięto całą siatkę tekstu o 40 px w prawo i dopasowano szerokości,
aby zachować prawy margines. Separator ma x=320, koniec pola pikony x=284,
początek nazwy x=360, a początek podkładu TERAZ x=348. Testy obejmują odstępy
po obu stronach linii, podkład TERAZ i wspólne wyrównanie postępu z nazwą.

EventView i InfoBarEventView mają przezroczyste okno oraz ePixmap z zPosition=-10.
Maska 1920×1 jest skalowana natywnie na pełny ekran. Na bocznych 64 px alpha
rośnie od 0 do 217; cały obszar napisów ma alpha=217, czyli około 85% krycia.
Kolor pozostaje #0c0e10. Native epg_description pozostaje GUI ScrollLabel;
nie zmieniono zawartości EPG, przewijania ani akcji klawiszy.

Obie zmiany dotyczą Standard i Large. Kontrole sprawdzają również, że żadne
pole tekstowe nie wchodzi w przezroczyste obrzeże maski. Wizualizacje korzystają
z przykładowego opisu audycji. Potrzebny pozostaje test efektu OSD na odbiorniku.

## Równe marginesy EventView — 0.6.2

EventView i InfoBarEventView używają wspólnego marginesu 128 px. Obszar opisu
ma x=128, szerokość 1664 px i prawy koniec x=1792. Nagłówek, linie i przyciski
kolorowe korzystają z tego samego obszaru. Cztery kolumny stopki mają po 416 px;
zegar i czas trwania kończą się na prawej granicy treści.

Maska fade rośnie do alpha=217 na pierwszych 128 px i jest symetryczna po prawej.
W polu tekstu pozostaje 85% krycia. Wszystkie pozostałe ekrany zachowują swoje
marginesy. Nie zmieniono źródła ani przewijania opisu. Istniejący test obu wariantów
sprawdza obustronne granice wszystkich pól tekstowych, symetrię opisu, wyrównanie
zegara i czasu trwania oraz pełne krycie maski pod tekstem.

## Długi fade informacji o audycji — 0.6.3

Maska EventView / InfoBarEventView ma teraz jeden kierunkowy gradient od x=0
do x=1824 (95% szerokości FHD). Funkcja smoothstep zmienia alpha od 240 do 184,
po czym utrzymuje prawą wartość do końca obrazu. To około 94% → 72% krycia.
Kolor pozostaje #0c0e10. Maska nadal ma 1920×1 pikseli i jest skalowana natywnie.
Nie dodano animacji, rozmywania obrazu ani nowych modułów runtime.

Marginesy 128 px i wszystkie kontrolki pozostają bez zmian. Test sprawdza
monotoniczny spadek alpha, stopniową zmianę na dużej części ekranu i minimalny
kontrast 4,5:1 dla white/muted/green na najjaśniejszym białym obrazie wideo.
InfoBar, SecondInfoBar i MoviePlayer zachowują poprzednie maski i 15% przezroczystości.
Potrzebna jest jeszcze ocena efektu na fizycznym dekoderze i telewizorze.

## Czytelność wyboru kanału — 0.6.4

Oba szablony serviceList mają dwie niezależne linie: ServiceName na x=204,
szerokość 860 px; Title1 pod spodem, szerokość 748 px. Pole postępu zaczyna się
na x=980, czyli 28 px za końcem tekstu audycji. Wszystkie pola tekstowe używają
natywnego wrap=ellipsis. Nazwa kanału ma TvSatStrong 32/36 px, audycja TvSatText
27/30 px; kolor opisu muted pozostaje także na zaznaczeniu.

Jawny selectionPixmap ma jednolity kolor #25473a, 1088×116 px, i jest przycinany
przez natywną listę do wysokości wiersza. Wyłącza odziedziczony wygląd zaznaczenia
z bazowej skórki. Kolor tła listy pozostaje #0c0e10.

apply_profile ustawia servicelist_twolines=True również dla Standard. Native
ServiceListLegacy nadpisuje serviceItemHeight liczbą pozycji z konfiguracji,
więc zapis ustawia serviceitems_per_page_twolines na 7/6. Procedura wtyczki nadal
nie działa przy starcie i nie zmienia ustawień podczas instalacji ani Anuluj.
Nowy układ wymaga Zapisz w TvSat — wygląd i restartu GUI, jeśli działa Legacy.
check_upstream_service_ui wykonuje oryginalny setItemsPerPage z 7.5, 7.6 i 8.0,
weryfikując 100/116 px oraz pełne 7/6 pozycji (wywołania C++ zastąpione).

Panel PIG zachowuje podgląd 608×342. Tytuł ma 88 px i renderer TvSatSummary,
który mierzy linie natywnie. Godziny zaczynają się 8 px niżej; skrót opisu ma
110 px i 8 px przerwy przed podpowiedzią INFO. Pełne źródło EPG jest zachowane.
Podglądy zawierają długie nazwy z raportowanego przykładu. Testy automatyczne
nie zastępują oceny wizualnej na fizycznym dekoderze.

## Historia kanałów — 0.6.5

Nowe ekrany HistoryZap i HistoryZapSelector mają 1920×1080 i natywny List/menu
z TemplatedMultiContent. OpenATV 8.0 szuka najpierw HistoryZap, starsze badane
wersje używają nazwy klasy HistoryZapSelector. Kontrakty widgetów dodano z AST
tych samych przypiętych źródeł ChannelSelection.py/Screen.py co dotychczas.
Mapowanie jest także częścią audit_openatv.py.

Natywny wiersz ma osiem pól. Szablon wyświetla marker (1), nazwę kanału (2),
tytuł audycji (3), godziny/czas (5) i pikonę (6); zachowuje referencję kanału (7)
wykorzystywaną przez keySelect. Opis (4) jest celowo pominięty w układzie.
W Standard mieści się 5×140 px, w Duże napisy 4×168 px. Pikona ma 144×80 lub
144×96 px z zachowaniem proporcji. Między pikoną a nazwą jest 32 px odstępu,
między nazwą a godzinami również 32 px. Nazwa i tytuł są w osobnych liniach.
Trzy pola tekstowe używają RT_ELLIPSIS. Jawna grafika zaznaczenia ma ciemne,
jednolite tło. Przy powiększaniu szablonu linie 1 px pozostają cienkie i mieszczą
się w dolnej krawędzi wiersza.

check_upstream_history_ui uruchamia oryginalną klasę HistoryZapSelector oraz
TemplatedMultiContent z OpenATV 7.5/7.6/8.0. Sprawdza oba porządki historii,
indeks początkowego zaznaczenia, dane z brakującym EPG/pikoną, pustą historię,
wybór każdej referencji, Anuluj i oba rozmiary/aliasy skórki. C++ i usługi tunera
są zastąpione; ocena wyglądu na fizycznym dekoderze pozostaje do wykonania.
Natywny kod i ustawienia odbiornika nie są zmieniane. Do wczytania nowych nazw
ekranów potrzebny jest restart GUI.

## Gęstsze listy i boczna historia — 0.6.6

Wszystkie tryby serviceList (services, bouquets, other) mają 76 px wysokości.
Obszar listy 1136×760 na x=40/y=168 mieści dokładnie 10 pozycji. Profile Standard
oraz Duże napisy zachowują tę samą liczbę. Nazwa kanału ma 28/30 px, audycja
23/25 px i własną linię, numer 24/26 px. Przy 76 px pozostają pełne dwie linie
z minimalnym odstępem 2 px. Audycja kończy się 32 px przed paskiem postępu.
Ustawienia serviceitems_per_page oraz serviceitems_per_page_twolines zapisują
10, ponieważ starszy silnik nadpisuje serviceItemHeight konfiguracją.

Inny tryb listy (foldery/bukiety) wyświetla natywne FolderImage/MarkerImage
zastąpione ikonami konturowymi z katalogu aktywnej skórki. Oddzielne
BouquetSelector/EPGBouquetSelector także mają 10×76 px. Nagłówek i stopka tej
grupy ekranów mają 40 px marginesu. Podgląd Pig ma nadal 608×342, przesunięty
na x=1272/y=168. Pozostałe ekrany zachowują dotychczasowy rozmiar pisma.

HistoryZap oraz HistoryZapSelector mają pozycję 40,80 i rozmiar 704×920.
Menu zajmuje 664×672, czyli 6×112 px. Oba profile używają tego samego obszaru,
Duże napisy ma większą czcionkę bez skalowania całego panelu. Nazwa, audycja
i godziny są w trzech osobnych liniach. Referencja (7), indeks pikony (6),
marker (1) i natywne przyciski nie zmieniają znaczenia. Tło panelu używa overlay;
poza jego obszarem nie ma widgetów, które zasłaniałyby wideo.

Testy oryginalnych parserów OpenATV 7.5/7.6/8.0 obejmują także otherFolder i jego
indeks FolderImage, rozmiar starszej listy 10×76 oraz zmniejszone szablony historii.
Nowe ikony mają przezroczyste tło, kontury w kolorze muted i zielony akcent.
Testy geometrii sprawdzają zmieszczenie obu linii w większej czcionce i odstępy
od pikon oraz pasków postępu. Nadal nie zastępują testu na fizycznym dekoderze.
