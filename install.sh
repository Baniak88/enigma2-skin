#!/bin/sh
# Uruchom w katalogu rozpakowanej paczki. Nie aktywuje skórki automatycznie.
set -eu
SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=${DESTDIR:-}
TARGET="$ROOT/usr/share/enigma2/CanalPL"
if [ ! -f "$SOURCE/CanalPL/skin.xml" ]; then
    echo 'Brak CanalPL/skin.xml obok install.sh.' >&2
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
STAGE="$PARENT/.CanalPL-install-$$"
if [ -e "$STAGE" ] || [ -L "$STAGE" ]; then
    echo 'Katalog tymczasowy już istnieje.' >&2
    exit 1
fi
mkdir "$STAGE"
trap 'rm -rf "$STAGE"' EXIT HUP INT TERM
cp -R "$SOURCE/CanalPL/." "$STAGE/"
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
echo "Zainstalowano: $TARGET/skin.xml"
echo 'Wybierz CanalPL w ustawieniach interfejsu/skórek, następnie uruchom ponownie GUI.'
