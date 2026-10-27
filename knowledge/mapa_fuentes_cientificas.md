# Mapa de fuentes científicas y su acceso real

**Medido el 2026-10-27 desde el entorno de nube en que corre el equipo.** Se probó una petición a cada sitio. Un sitio "bloqueado" no
significa que el contenido no exista: significa que ESTE entorno no puede abrirlo. Ningún agente intenta rodear el bloqueo.

## 1. Vías que sí funcionan hoy

| Vía | Qué entrega | Nivel de lectura máximo | Límites |
|---|---|---|---|
| Conector de texto completo de artículos arbitrados (`search_wiley_fulltext`) | Pasajes de texto completo con DOI, autores, revista, año y resumen | Fragmento de texto completo | Solo cubre una editorial; plan gratuito con **30 consultas hasta el 2026-11-01** (revisar con `getUsageLimit` antes de gastar) |
| Lector de papers de Hugging Face (`hf://papers/<id>/paper.md`) | Texto de un preprint cuyo identificador ya se conoce | Texto completo | Su búsqueda es débil para descubrir (trae temas ajenos); sirve para LEER un identificador conocido |
| Búsqueda web (`WebSearch`) | Títulos, URL y resúmenes de buscador | Snippet | No se puede abrir casi ninguna página; todo lo que entrega es SOLO-SNIPPET |
| API de libros de Google | Metadatos de libros | Referencia | Responde 429 (límite de tasa) |
| PyPI, archivos raw de GitHub, documentación de Claude Code | Paquetes, archivos, documentación | Texto completo | No son literatura científica |

## 2. Fuentes que el equipo debe usar cuando la red lo permita

Acceso medido en este entorno:

| Región | Fuente | Dominio | Estado medido |
|---|---|---|---|
| global | BASE | `www.base-search.net` | bloqueado por la política de red (403 al abrir el túnel) |
| global | CORE API | `api.core.ac.uk` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Crossref API | `api.crossref.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | DOAJ | `doaj.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | DOI resolver | `doi.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Europe PMC | `www.ebi.ac.uk` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Google Books API | `www.googleapis.com` | alcanzable, con límite de tasa (429) |
| global | Google Scholar | `scholar.google.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | HAL (Francia) | `api.archives-ouvertes.fr` | bloqueado por la política de red (403 al abrir el túnel) |
| global | IEEE Xplore | `ieeexplore.ieee.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Internet Archive | `archive.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | LinkedIn | `www.linkedin.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | MDPI | `www.mdpi.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | NDLTD | `ndltd.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | OATD (tesis) | `oatd.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Open Library | `openlibrary.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | OpenAlex API | `api.openalex.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | ResearchGate | `www.researchgate.net` | bloqueado por la política de red (403 al abrir el túnel) |
| global | ScienceDirect | `www.sciencedirect.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Scimago (cuartiles) | `www.scimagojr.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Scribd | `www.scribd.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Semantic Scholar API | `api.semanticscholar.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Springer | `link.springer.com` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Unpaywall | `api.unpaywall.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Wikipedia | `en.wikipedia.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | Zenodo | `zenodo.org` | bloqueado por la política de red (403 al abrir el túnel) |
| global | arXiv | `export.arxiv.org` | bloqueado por la política de red (403 al abrir el túnel) |
| EEUU | Colorado School of Mines | `repository.mines.edu` | bloqueado por la política de red (403 al abrir el túnel) |
| EEUU | DTIC | `apps.dtic.mil` | bloqueado por la política de red (403 al abrir el túnel) |
| EEUU | Harvard DASH | `dash.harvard.edu` | bloqueado por la política de red (403 al abrir el túnel) |
| EEUU | MIT DSpace | `dspace.mit.edu` | bloqueado por la política de red (403 al abrir el túnel) |
| EEUU | NASA NTRS | `ntrs.nasa.gov` | bloqueado por la política de red (403 al abrir el túnel) |
| EEUU | OSTI (DOE) | `www.osti.gov` | bloqueado por la política de red (403 al abrir el túnel) |
| Canadá | Library and Archives (tesis) | `www.bac-lac.gc.ca` | bloqueado por la política de red (403 al abrir el túnel) |
| Canadá | UAlberta ERA | `era.library.ualberta.ca` | bloqueado por la política de red (403 al abrir el túnel) |
| Canadá | UBC cIRcle | `open.library.ubc.ca` | bloqueado por la política de red (403 al abrir el túnel) |
| Brasil | BDTD (IBICT) | `bdtd.ibict.br` | bloqueado por la política de red (403 al abrir el túnel) |
| Brasil | CAPES periódicos | `www.periodicos.capes.gov.br` | bloqueado por la política de red (403 al abrir el túnel) |
| Brasil | SciELO | `search.scielo.org` | bloqueado por la política de red (403 al abrir el túnel) |
| Brasil | USP Teses | `www.teses.usp.br` | bloqueado por la política de red (403 al abrir el túnel) |
| Chile | PUC Chile | `repositorio.uc.cl` | bloqueado por la política de red (403 al abrir el túnel) |
| Chile | Repositorio ANID | `repositorio.anid.cl` | bloqueado por la política de red (403 al abrir el túnel) |
| Chile | Repositorio U. de Chile | `repositorio.uchile.cl` | bloqueado por la política de red (403 al abrir el túnel) |
| Perú | ALICIA (CONCYTEC) | `alicia.concytec.gob.pe` | bloqueado por la política de red (403 al abrir el túnel) |
| Perú | PUCP Tesis | `tesis.pucp.edu.pe` | bloqueado por la política de red (403 al abrir el túnel) |
| Perú | RENATI (SUNEDU) | `renati.sunedu.gob.pe` | bloqueado por la política de red (403 al abrir el túnel) |
| Perú | UNI Cybertesis | `cybertesis.uni.edu.pe` | bloqueado por la política de red (403 al abrir el túnel) |
| Perú | UNMSM Cybertesis | `cybertesis.unmsm.edu.pe` | bloqueado por la política de red (403 al abrir el túnel) |
| México | CONAHCYT repositorio | `www.repositorionacionalcti.mx` | bloqueado por la política de red (403 al abrir el túnel) |
| México | TesiUNAM | `tesiunam.dgb.unam.mx` | bloqueado por la política de red (403 al abrir el túnel) |
| Australia | CSIRO | `publications.csiro.au` | bloqueado por la política de red (403 al abrir el túnel) |
| Australia | Trove | `trove.nla.gov.au` | bloqueado por la política de red (403 al abrir el túnel) |
| Australia | UQ eSpace | `espace.library.uq.edu.au` | bloqueado por la política de red (403 al abrir el túnel) |
| Finlandia | Aalto | `aaltodoc.aalto.fi` | bloqueado por la política de red (403 al abrir el túnel) |
| Finlandia | Doria | `www.doria.fi` | bloqueado por la política de red (403 al abrir el túnel) |
| Finlandia | LUT LUTPub | `lutpub.lut.fi` | bloqueado por la política de red (403 al abrir el túnel) |
| Alemania | BASE Bielefeld | `www.base-search.net` | bloqueado por la política de red (403 al abrir el túnel) |
| Alemania | KIT | `publikationen.bibliothek.kit.edu` | bloqueado por la política de red (403 al abrir el túnel) |
| Alemania | TU Munich mediaTUM | `mediatum.ub.tum.de` | bloqueado por la política de red (403 al abrir el túnel) |

Además, sin sonda propia: Scopus, Web of Science y las bases de pago (requieren suscripción); **Scribd y LinkedIn** (Scribd: documentos libres que la persona pidió considerar; hoy bloqueado) exigen sesión y sus
condiciones de uso no permiten extraer su contenido: se tratan como pistas (nunca como evidencia) o, si la persona sube el documento,
como dato aportado por ella.

## 3. Cuartiles de revista (Q1 y Q2)

El cuartil de una revista solo se registra con su fuente (por ejemplo el ranking de revistas del año). Hoy el sitio de rankings está
bloqueado: **el cuartil queda en `null` y se declara "no verificable en este entorno"**. Que una revista sea Q1 no demuestra que
un estudio sea correcto ni comparable con tu activo; son dos cosas distintas y el informe las separa.

## 4. Para que el equipo pueda leer la literatura abierta

Quien administra el entorno puede ampliar el acceso de red (menú del entorno en la barra de título de la sesión, luego Edit, y ahí el nivel de
acceso o la lista de dominios permitidos). Dominios a permitir, en orden de valor (primero las interfaces de metadatos y acceso abierto):

```
aaltodoc.aalto.fi
alicia.concytec.gob.pe
api.archives-ouvertes.fr
api.core.ac.uk
api.crossref.org
api.openalex.org
api.semanticscholar.org
api.unpaywall.org
apps.dtic.mil
archive.org
bdtd.ibict.br
cybertesis.uni.edu.pe
cybertesis.unmsm.edu.pe
dash.harvard.edu
doaj.org
doi.org
dspace.mit.edu
en.wikipedia.org
era.library.ualberta.ca
espace.library.uq.edu.au
export.arxiv.org
ieeexplore.ieee.org
link.springer.com
lutpub.lut.fi
mediatum.ub.tum.de
ndltd.org
ntrs.nasa.gov
oatd.org
open.library.ubc.ca
openlibrary.org
publications.csiro.au
publikationen.bibliothek.kit.edu
renati.sunedu.gob.pe
repositorio.anid.cl
repositorio.uc.cl
repositorio.uchile.cl
repository.mines.edu
scholar.google.com
search.scielo.org
tesis.pucp.edu.pe
tesiunam.dgb.unam.mx
trove.nla.gov.au
www.bac-lac.gc.ca
www.base-search.net
www.doria.fi
www.ebi.ac.uk
www.linkedin.com
www.mdpi.com
www.osti.gov
www.periodicos.capes.gov.br
www.repositorionacionalcti.mx
www.researchgate.net
www.sciencedirect.com
www.scimagojr.com
www.scribd.com
www.teses.usp.br
zenodo.org
```
Con ellos, el investigador puede buscar en bases de metadatos abiertas, resolver DOI, leer preprints y repositorios de tesis de
las universidades y países nombrados, y comprobar cuartiles.

## Prioridad geográfica indicada por la persona
Chile, Perú, Australia, Estados Unidos, México, Brasil, Finlandia, Reino Unido, Suiza, Alemania y Canadá. Además de universidades de Estados Unidos
(MIT, Harvard, Colorado School of Mines, Stanford) y todas las del Perú. Se incluyen tesis y libros de acceso libre. Scribd y redes sociales solo
como pista: se registran como `solo_referencia` o `snippet` y nunca respaldan una cifra. Cada fuente registra su país solo si la fuente lo declara.
Estado actual: la red del entorno bloquea casi todos estos repositorios; hasta que se habiliten los dominios, esta cobertura es VACÍO declarado.
