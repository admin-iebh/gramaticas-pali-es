# Instrucciones del proyecto

Si hay conflicto entre este archivo y `comun/convenciones.md`, manda
`comun/convenciones.md`.

## Qué es este repositorio

Traducciones al español de gramáticas clásicas pāḷi. Público lector:
estudiantes hispanohablantes de pāḷi con formación budista.

## Reglas

- Registro formal y doctrinal; no coloquial.
- Términos técnicos pāḷi sin traducir, con diacríticos completos
  (nibbāna, saṅkhāra, kāraka); cursiva en la primera aparición de cada sección.
- Consultar `comun/glosario.md` antes de fijar la traducción de un término.
  Si no está, proponerlo y añadirlo — no improvisar caso por caso.
- Ante duda gramatical o de lectura, decirlo explícitamente en lugar de
  suponer. Marcar con `<!-- DUDA: ... -->`.
- Dar la referencia (sutta, obra, edición) al afirmar algo sobre el texto.
- No reescribir secciones ya revisadas sin que se pida.
- Nunca añadir, quitar ni cambiar nada más allá de lo que da estrictamente la
  edición base sin avisar explícitamente y dejar que Angel decida. Esto incluye
  las expansiones morfológicas (pasos de elisión o sustitución que Nandisena no
  menciona). Lo tomado de Ven. A. Thitzana se señala siempre como suyo.

## Cómo se publica

El markdown es la fuente; el HTML de `site/` es salida generada. **Nunca se
edita nada dentro de `site/`.** El hook de pre-commit lo reconstruye entero en
cada commit, así que un cambio hecho ahí desaparece sin avisar y sin dejar
rastro. Lo que se edita está en `kaccayana/`, `recursos/` y `comun/`.

Cada `git push` a `main` despliega en
<https://gramaticas.buddha-dhamma.net> (Cloudflare Workers, ver
`wrangler.jsonc`).

    # capítulo de una gramática
    python3 herramientas/generar_capitulo.py kaccayana/02-nama-kappa.md

    # documento en prosa (reglas, glosarios, tablas)
    python3 herramientas/generar_recurso.py recursos/<archivo>.md

o todo de una vez, que es lo habitual:

    python3 herramientas/generar_todo.py

Un hook de git lo ejecuta en cada commit y añade el HTML regenerado, de modo
que no hace falta acordarse. Los hooks no viajan con el clon: en una copia
nueva del repositorio hay que instalarlo una vez con

    sh herramientas/instalar-hooks.sh

Detalles del formato del markdown y de lo que el generador deduce solo:
`comun/convenciones.md`, secciones 2, 3, 3 bis y 3 ter.

## Estado de recursos/sandhi

La referencia interactiva de sandhi (`/recursos/sandhi/`, v3.5) se arma con
`herramientas/generar_sandhi.py` a partir de tres piezas:
`recursos/sandhi/plantilla.html` (maquetado y lógica),
`recursos/sandhi/reglas.json` (49 reglas y 266 formas) y
`kaccayana/01-sandhi-kappa.md` (los 51 aforismos).

### Procedencia de cada secuencia

Las 266 formas salen del documento de Bhikkhu Nandisena, que da componentes,
resultado y referencia canónica, pero **no** los pasos intermedios. Cada forma
lleva un campo que dice de dónde sale su secuencia:

| Campo        | Formas | De dónde viene |
| ------------ | -----: | -------------- |
| `verificada` |     49 | Copiada de la traducción del Sandhi-kappa |
| `derivada`   |    175 | Calculada y comprobada contra la forma atestiguada |
| `aforismo`   |     42 | Construida a partir del propio aforismo |

La regla que hace fiable lo calculado: se genera una secuencia candidata, se
aplica, y sólo se conserva si reproduce **exactamente** la forma atestiguada
—ignorando apóstrofos, espacios y guiones—. Lo que no cuadra no se publica.
Nunca se inventa un paso para rellenar un hueco.

### Lo que conviene saber antes de tocarlo

- **El Sandhi-kappa está agotado.** Contiene 164 secuencias y las aprovechables
  ya están puestas: son las 49 `verificada`. No vale la pena volver a buscar
  ahí. El resto de las formas de Nandisena son ejemplos canónicos suyos, no de
  Kaccāyana.
- **13 formas tienen un solo paso**, todas de pakati-sandhi. No es que les
  falte la secuencia: es que en pakati no ocurre nada, y ése es el sentido de
  la sección. No hay que «arreglarlas».
- **9 formas llevan `nota`.** Cinco explican qué ilustra la forma; las otras
  cuatro avisan de que los datos de la fuente parecen erróneos —`icc antaṃ`,
  `nicchayo`, `esa ābhogho` y `jamb’ īritā vatena`—. Ésas son para cotejar con
  el PDF, no para corregir a ojo.

### Comprobaciones

    python3 herramientas/auditar_secuencias.py     # coherencia paso ↔ aforismo
    python3 herramientas/reconstruir_sandhi.py     # rehace reglas.json desde el documento

La auditoría sólo comprueba que el aforismo citado haga esa *clase* de
operación. Que un paso la pase no demuestra que la cita sea la correcta.

## Capítulo nuevo: qué hace falta

1. El markdown en `kaccayana/NN-nombre-kappa.md`, con el mismo formato que
   `01-sandhi-kappa.md`: `**[Kacc]. [Rū]. Texto pāḷi ([Sad]).** \[desglose, n]`,
   bloques separados por `---`, notas `[^n]`, fórmula de cierre de cada kaṇḍa
   en negrita, glosas emergentes como `{término|glosa}`.
2. Su entrada en el diccionario `CAPITULOS` de `herramientas/generar_capitulo.py`
   (slug, títulos pāḷi y español, capítulo anterior y siguiente).
3. Ejecutar el generador y revisar el aviso final de referencias §N sin
   enlazar: `Rū. §49`, `Sad. §139` y similares remiten a otras obras y no
   deben enlazarse a suttas de este capítulo.
4. Añadir el capítulo a `comun/concordancia.json`.
5. Cambiar en `site/kaccayana/index.html` la tarjeta «en preparación» por un
   enlace real.
