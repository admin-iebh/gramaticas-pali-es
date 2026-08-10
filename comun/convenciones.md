# Convenciones de traducción

Documento normativo. Toda decisión que se repita va aquí.

## 1. Términos pāḷi

- Términos técnicos sin traducir. Unicode NFC, diacríticos completos.
- Equivalencia española entre paréntesis la primera vez:
  *kāraka* (relación sintáctica).

## 2. Numeración de suttas

- Edición base: Kaccāyana-vyākaraṇa, ed. y trad. Bhikkhu U Nandisena (ITBMU).
  La numeración de suttas de este repositorio sigue esta edición.
  <!-- PENDIENTE: precisar año / versión exacta que se está usando -->
- **Numeración triple**, tal como la presenta Nandisena:
  `**[Núm. Kaccāyana]. [Núm. Rūpasiddhi]. Texto del sutta ([Núm. Saddanīti-Suttamālā]).**`
  Ejemplo: `**30. 58. Aṃ byañjane niggahitaṃ (153).**`
- El **primer número** (Kaccāyana, secuencial) es el normativo. Se cita `§30`
  y fija el ancla del sutta: `id="s30"`, es decir la URL pública
  `…/kaccayana/sandhi/#s30`. **Las anclas no se cambian una vez publicadas.**
- El segundo número (Rūpasiddhi) y el número entre paréntesis
  (Saddanīti-Suttamālā, ausente en algunos suttas) son concordancias, no anclas.
- No renumerar.
- `comun/concordancia.json` registra los tres números de cada sutta, para quien
  llegue desde otra edición. Se actualiza al cerrar cada capítulo.

## 3. Estructura de los archivos

- Un archivo por kappa (capítulo), no uno por kaṇḍa ni por sutta:
  `kaccayana/01-sandhi-kappa.md` contiene las cinco kaṇḍas del capítulo.
  <!-- Corregido: la regla anterior decía "un archivo por kaṇḍa"; el texto ya
       traducido está organizado por kappa. -->
- Orden dentro de cada sutta: texto pāḷi, traducción, vutti, nota.

## 3 bis. Sitio publicado

- `site/` es lo único que se publica; ver `wrangler.jsonc` en la raíz.
- El HTML de `site/` es salida; la fuente es el markdown de `kaccayana/`.
- Dominio: `gramaticas.buddha-dhamma.net`. Un solo sitio, obras y capítulos
  en rutas: `/kaccayana/sandhi/`, `/kaccayana/nama/`, `/recursos/`.

## 4. Citas del canon

- Enlazar a https://buddha-dhamma.net en lugar de reproducir el pasaje.

## 5. Marcas de trabajo

- `<!-- DUDA: ... -->`      cuestión sin resolver
- `<!-- REVISAR: ... -->`   traducción provisional
