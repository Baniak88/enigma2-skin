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
if [ -e "$TARGET" ]; then
    BACKUP="${TARGET}.backup-$(date +%Y%m%d-%H%M%S)-$$"
    cp -R "$TARGET" "$BACKUP"
    echo "Kopia poprzedniej wersji: $BACKUP"
fi
mkdir -p "$TARGET"
cp "$SOURCE/CanalPL/skin.xml" "$TARGET/skin.xml"
chmod 755 "$TARGET"
chmod 644 "$TARGET/skin.xml"
echo "Zainstalowano: $TARGET/skin.xml"
echo 'Wybierz CanalPL w ustawieniach interfejsu/skórek, następnie uruchom ponownie GUI.'
