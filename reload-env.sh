#!/bin/bash

# Użyj pierwszego argumentu jako nazwy pliku lub domyślnie '.env'.
ENV_FILE=${1:-.env}

# Sprawdź, czy plik istnieje.
if [ ! -f "$ENV_FILE" ]; then
    echo "Błąd: Plik '$ENV_FILE' nie został znaleziony."
    exit 1
fi

# Włącz opcję 'allexport', która automatycznie eksportuje wszystkie
# definiowane lub modyfikowane zmienne.
set -a

# Wczytaj plik w bieżącej powłoce.
# Dzięki 'set -a', wszystkie przypisania w pliku zostaną wyeksportowane.
source "$ENV_FILE"

# Wyłącz opcję 'allexport', przywracając domyślne zachowanie.
set +a

echo "Zmienne z pliku '$ENV_FILE' zostały wczytane i wyeksportowane."