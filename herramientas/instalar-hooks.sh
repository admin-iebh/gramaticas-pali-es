#!/bin/sh
# Instala los hooks de git de este repositorio.
# Los hooks no viajan con el clon, así que hay que ejecutarlo una vez por copia.
RAIZ=$(git rev-parse --show-toplevel)
cp "$RAIZ/herramientas/hooks/pre-commit" "$RAIZ/.git/hooks/pre-commit"
chmod +x "$RAIZ/.git/hooks/pre-commit"
echo "Hook instalado: el sitio se regenerará en cada commit."
