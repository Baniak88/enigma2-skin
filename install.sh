#!/bin/sh
# Uruchom w katalogu rozpakowanej paczki. Nie aktywuje skórki automatycznie.
set -eu
SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=${DESTDIR:-}
TARGET="$ROOT/usr/share/enigma2/TvSat"
if [ ! -f "$SOURCE/TvSat/skin.xml" ]; then
    echo 'Brak TvSat/skin.xml obok install.sh.' >&2
    exit 1
fi
if [ -z "$ROOT" ] && [ ! -d /usr/share/enigma2 ]; then
    echo 'To nie wygląda na dekoder Enigma2: brak /usr/share/enigma2.' >&2
    exit 1
fi
if [ -L "$TARGET" ]; then
    echo 'Katalog docelowy jest dowiązaniem. Instalacja przerwana.' >&2
    exit 1
fi
PARENT="$ROOT/usr/share/enigma2"
mkdir -p "$PARENT"
STAGE="$PARENT/.TvSat-install-$$"
if [ -e "$STAGE" ] || [ -L "$STAGE" ]; then
    echo 'Katalog tymczasowy już istnieje.' >&2
    exit 1
fi
mkdir "$STAGE"
trap 'rm -rf "$STAGE"' EXIT HUP INT TERM
printf '\n%s\n' 'TvSat: instalowanie plików skórki...'
cp -R "$SOURCE/TvSat/." "$STAGE/"
find "$STAGE" -type d -exec chmod 755 {} \;
find "$STAGE" -type f -exec chmod 644 {} \;
BACKUP=
if [ -e "$TARGET" ]; then
    BACKUP="${TARGET}.backup-$(date +%Y%m%d-%H%M%S)-$$"
    mv "$TARGET" "$BACKUP"
    echo "Kopia poprzedniej wersji: $BACKUP"
fi
if ! mv "$STAGE" "$TARGET"; then
    if [ -n "$BACKUP" ]; then mv "$BACKUP" "$TARGET"; fi
    exit 1
fi
printf '\n%s\n' '======================================================'
printf '%s\n' 'TvSat — INSTALACJA ZAKOŃCZONA POMYŚLNIE'
printf 'Pliki: %s/skin.xml\n' "$TARGET"
printf '%s\n' 'Wybierz TvSat w menu skórek, jeśli to pierwsza instalacja.'
printf '%s\n' 'Uruchom ponownie interfejs GUI, aby wczytać zmiany.'
printf '%s\n\n' '======================================================'
