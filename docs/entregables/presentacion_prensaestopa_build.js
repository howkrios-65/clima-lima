const pptxgen=require('pptxgenjs');const fs=require('fs');
const SK='/root/.claude/skills/synced/7fd509e0-a6d1-4387-9ddc-c3e2303bdaa3_ca63f8bb-a2bd-43d4-be0f-2a8f777623d1/pptx/scripts/apply_theme.js';
const {applyTheme}=require(SK);
const D=JSON.parse(fs.readFileSync('data.json','utf8'));
const THEME={name:'Confiabilidad baby',headFontFace:'Cambria',bodyFontFace:'Calibri',colors:{dk1:'22313F',lt1:'FFFFFF',dk2:'3E5871',lt2:'EAF3F8',accent1:'5B9FCF',accent2:'6FB98D',accent3:'F0B784',accent4:'C8AAD6',accent5:'86BCB6',accent6:'ECD27A',hlink:'3B7FB5',folHlink:'7A6FA0'}};
const pres=new pptxgen();pres.layout='LAYOUT_WIDE';pres.theme={headFontFace:'Cambria',bodyFontFace:'Calibri'};pres.title='Rodamientos de bombas con prensaestopa';pres.author='HOWK RIOS - CONFIABILIDAD';
const C=pres.SchemeColor;
pres.defineSlideMaster({title:'CONTENIDO',background:{color:C.background1},objects:[
 {text:{text:'HOWK RIOS - CONFIABILIDAD  |  Bomba con prensaestopa',options:{x:0.5,y:7.08,w:9,h:0.3,fontSize:10,color:C.text2,margin:0,isTextBox:true}}}],
 slideNumber:{x:12.3,y:7.08,w:0.6,h:0.3,fontSize:10,color:C.text2}});
pres.defineSlideMaster({title:'PORTADA',background:{color:C.text1},objects:[]});
let SEC='';
function sec(t){SEC=t;pres.addSection({title:t})}
function S(titulo,fuente){const s=pres.addSlide({masterName:'CONTENIDO',sectionTitle:SEC});s.addText(titulo,{x:0.5,y:0.3,w:12.3,h:0.95,fontFace:'Cambria',fontSize:24,bold:true,color:C.text1,margin:0,valign:'top',isTextBox:true});if(fuente)s.addText('Fuente: '+fuente,{x:0.5,y:6.72,w:12.3,h:0.3,fontSize:10,color:C.text2,italic:true,margin:0,isTextBox:true,valign:'top'});return s}
function card(s,x,y,w,h,head,lines,col,o){o=o||{};s.addShape(pres.ShapeType.roundRect,{x,y,w,h,rectRadius:0.08,fill:{color:o.fill||C.background2},line:{color:col,width:1},objectName:'tarjeta '+head});
 s.addText(head,{x:x+0.15,y:y+0.1,w:w-0.3,h:0.4,fontSize:o.hs||14,bold:true,color:C.text1,margin:0,isTextBox:true,valign:'top'});
 s.addText(lines.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<lines.length-1,paraSpaceAfter:4}})),{x:x+0.15,y:y+0.55,w:w-0.3,h:h-0.65,fontSize:o.fs||12,color:C.text1,margin:0,isTextBox:true,valign:'top'})}
function kpi(s,x,y,w,big,small,col){s.addShape(pres.ShapeType.roundRect,{x,y,w,h:1.15,rectRadius:0.08,fill:{color:C.background2},line:{color:col,width:1},objectName:'kpi '+big});
 s.addText(big,{x:x+0.1,y:y+0.05,w:w-0.2,h:0.6,fontSize:30,bold:true,color:col,fontFace:'Cambria',margin:0,isTextBox:true,align:'left'});
 s.addText(small,{x:x+0.1,y:y+0.65,w:w-0.2,h:0.48,fontSize:11,color:C.text1,margin:0,isTextBox:true,valign:'top'})}
const hdr=(t)=>({text:t,options:{bold:true,color:C.background1,fill:{color:C.text2},fontSize:12}});
const cell=(t,o)=>({text:t,options:Object.assign({fontSize:11,color:C.text1,valign:'top'},o||{})});
const chartBase={showTitle:true,titleFontSize:13,titleColor:'22313F',catAxisLabelFontSize:11,valAxisLabelFontSize:11,catAxisLabelColor:'3E5871',valAxisLabelColor:'3E5871',valGridLine:{color:'DDE9EE',size:0.5},catGridLine:{style:'none'},catAxisLabelFontFace:'+mn-lt',valAxisLabelFontFace:'+mn-lt',dataLabelFontFace:'+mn-lt',titleFontFace:'+mj-lt',dataLabelFontSize:11,dataLabelColor:'22313F',showValue:true};

const cut=(t,n)=>{t=String(t).replace(/^[^?]*\?\s*/,'').replace(/^Posible respuesta[^:]*:\s*/,'');return t.length<=n?t:t.slice(0,n).replace(/\s\S*$/,'')+'…'};
/* 1 portada */
sec('Inicio');
{const s=pres.addSlide({masterName:'PORTADA',sectionTitle:SEC});
 s.addText('Rodamientos de bombas con prensaestopa',{x:0.8,y:1.9,w:11.5,h:1.5,fontFace:'Cambria',fontSize:44,bold:true,color:C.background1,margin:0,valign:'top',isTextBox:true});
 s.addText('Dossier de confiabilidad con evidencia científica: lo respaldado, lo que no se pudo leer y lo que falta',{x:0.8,y:3.6,w:11,h:0.9,fontSize:20,color:C.accent1,margin:0,isTextBox:true,valign:'top'});
 s.addText('HOWK RIOS - CONFIABILIDAD',{x:0.8,y:5.3,w:8,h:0.4,fontSize:16,bold:true,color:C.background1,charSpacing:3,margin:0,isTextBox:true});
 s.addText('Informe del 27 de octubre de 2026  |  Todo respaldado por fuente o declarado SIN DATOS PARA ARMARLO',{x:0.8,y:5.75,w:11.5,h:0.4,fontSize:12,color:C.accent5,margin:0,isTextBox:true});
 s.addNotes('Caso de rodamientos en bombas con prensaestopa. La literatura de prensaestopa no se pudo leer desde este entorno; el dossier es honesto sobre ello.')}
/* 2 resumen */
{const s=S('Ninguna fuente de prensaestopa se pudo leer: solo los rodamientos tienen respaldo y el vínculo con la empaquetadura queda SIN DATOS PARA ARMARLO','Dossier del caso; registro de evidencia con '+D.entradas+' entradas');
 card(s,0.5,1.4,4.0,5.2,'Qué sabemos',['Los rodamientos de bombas se citan entre los componentes más propensos a fallar, por contaminación, mala lubricación y montaje inadecuado','Un resumen de 1988 atribuye el 90 % de las fallas prematuras de rodamientos de bolas de bombas a cuatro causas (no es estadística)','El defecto progresa en 4 etapas espectrales; la kurtosis no es monótona'],C.accent2,{fs:14,hs:15});
 card(s,4.7,1.4,4.0,5.2,'Qué no sabemos',['Si la fuga o el ajuste de la empaquetadura dañan el rodamiento, y cuánto','Efecto del agua en la vida del rodamiento (hay cifras de segunda mano sin leer)','Reparto de modos de falla, MTBF, Weibull y costos de bombas con prensaestopa','Datos de bombas con prensaestopa con tiempos hasta la falla','Citas y cuartiles de las fuentes','Verificación oficial de las '+D.normas+' normas'],C.accent3,{fs:14,hs:15});
 card(s,8.9,1.4,3.9,3.0,'Qué recomendamos',['Abrir las pistas prioritarias con acceso a las fuentes','Reunir el historial de fallas con fechas','Línea base por activo antes de cualquier modelo'],C.accent1,{fs:13,hs:15});
 kpi(s,8.9,4.55,1.85,String(D.docs_leidos),'documentos leídos de '+D.docs_total,C.accent1);kpi(s,10.95,4.55,1.85,String(D.normas),'normas en resúmenes de buscador',C.accent2);
 kpi(s,8.9,5.8,1.85,'0','fuentes leídas de prensaestopa o empaquetadura',C.accent3);kpi(s,10.95,5.8,1.85,String(D.n_hip),'hipótesis, todas posibles',C.accent4);
 s.addNotes('Mensaje principal: el análisis de rodamientos tiene respaldo; el prensaestopa solo tiene pistas de buscador.')}
/* 3 acceso */
sec('Alcance y método');
{const s=S('Los cinco frentes de búsqueda encontraron pistas, pero casi ninguna fuente de prensaestopa se pudo leer','Resultados de los agentes de investigación; red bloqueada para revistas, repositorios y organismos');
 const rows=[[hdr('Frente'),hdr('Entradas registradas'),hdr('Leídas con extracto'),hdr('Qué pasó')]];
 const nota={'Mecanismos y causas':'Solo pistas de buscador; ninguna cifra utilizable','Empaquetadura y contaminación':'11 pistas, ninguna leída; cifras de agua y fuga contradictorias','Monitoreo y diagnóstico':'Se leyeron bancos de rodamientos; agua y P-F solo pistas','ML, RUL y datos abiertos':'Bancos de rodamientos leídos; ninguno de bombas con prensaestopa','Normas, vida y costos':'Normas de empaquetadura y tesis solo en resúmenes'};
 Object.keys(D.frentes).forEach(k=>rows.push([cell(k,{bold:true}),cell(String(D.frentes[k].registradas)),cell(String(D.frentes[k].leidas)),cell(nota[k])]));
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[3.0,2.2,2.2,4.9],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.5});
 s.addText('Para compensar, se heredaron las 351 entradas del caso de la bomba centrífuga (rodamientos y vibración), que no tratan prensaestopa.',{x:0.5,y:5.7,w:12.3,h:0.7,fontSize:14,bold:true,color:C.text2,margin:0,isTextBox:true,valign:'top'});
 s.addNotes('El conector de texto completo no tiene cuota hasta el 1 de noviembre de 2026.')}
/* 4 método */
{const s=S('Un equipo de 20 agentes con ficha de ocho bloques y compuertas de evidencia produce el dossier','Protocolo del equipo; kit de cálculo con pruebas automáticas');
 const pasos=[['1 Intake','La persona nombra el modo de falla'],['2 Búsqueda','5 frentes en paralelo'],['3 Lectura','Lectura de textos con extracto literal'],['4 Análisis','ACR, árbol, Ishikawa, FMECA, predictivo'],['5 Compuertas','Todo número debe estar literal en su fuente'],['6 Verificación','Verificador independiente'],['7 Entrega','HTML, mapa de agentes, presentación']];
 pasos.forEach((p,i)=>{const x=0.5+i*1.78;s.addShape(pres.ShapeType.roundRect,{x,y:1.45,w:1.6,h:1.75,rectRadius:0.08,fill:{color:i%2?C.background2:C.accent1},line:{color:C.accent1,width:1},objectName:'paso '+p[0]});
  s.addText(p[0],{x:x+0.08,y:1.5,w:1.44,h:0.4,fontSize:13,bold:true,color:i%2?C.text1:C.background1,margin:0,isTextBox:true});
  s.addText(p[1],{x:x+0.08,y:1.92,w:1.44,h:1.25,fontSize:11,color:i%2?C.text1:C.background1,margin:0,isTextBox:true,valign:'top'});
  if(i<6)s.addText('›',{x:x+1.6,y:2.0,w:0.18,h:0.4,fontSize:20,color:C.text2,margin:0,isTextBox:true,align:'center'})});
 card(s,0.5,3.5,4.0,3.1,'Reglas del equipo',['Nada se inventa','Sin evidencia: SIN DATOS PARA ARMARLO','Referencias en APA 7 con enlace','Sin nombres de empresas','Cálculos con el kit'],C.accent2,{fs:14,hs:15});
 card(s,4.7,3.5,4.0,3.1,'Compuertas automáticas',['El nivel de lectura se deriva del acceso real','Cifras: número literal en el extracto','Hipótesis nunca pasan de posible sin caso real','Ítems sin fuente válida se eliminan y se listan'],C.accent1,{fs:14,hs:15});
 card(s,8.9,3.5,3.9,3.1,'Aprendizaje continuo',['Cada corrección queda en el historial','Reglas candidatas en cuarentena','La persona aprueba lo permanente'],C.accent3,{fs:14,hs:15});
 s.addNotes('Cada agente recibe ROL, TAREA, CONTEXTO, RAZONAMIENTO, CONDICIONES DE CIERRE, FEEDBACK, ALMACENAMIENTO Y MEMORIA y SALIDA.')}
/* 5 evidencia */
{const s=S('Se leyeron '+D.docs_leidos+' documentos de '+D.docs_total+' registrados, casi todos de rodamientos y vibración, ninguno de libros ni tesis','Registro de evidencia del caso (incluye fuentes heredadas); nivel de lectura derivado del acceso');
 const tl={paper:'Artículos arbitrados',preprint:'Preprints',repositorio:'Datos y repositorios',tesis:'Tesis',libro:'Libros',norma:'Normas'};
 const ks=Object.keys(D.tipos);s.addChart(pres.charts.BAR,[{name:'Documentos leídos',labels:ks.map(k=>tl[k]||k),values:ks.map(k=>D.tipos[k])}],Object.assign({},chartBase,{x:0.5,y:1.4,w:6.1,h:3.4,barDir:'bar',chartColors:['5B9FCF'],title:'Documentos leídos por tipo de fuente',showLegend:false,dataLabelPosition:'outEnd'}));
 const ys=Object.keys(D.anios);s.addChart(pres.charts.BAR,[{name:'Documentos',labels:ys,values:ys.map(k=>D.anios[k])}],Object.assign({},chartBase,{x:6.8,y:1.4,w:6.0,h:3.4,barDir:'col',chartColors:['6FB98D'],title:'Documentos leídos por año',showLegend:false,dataLabelPosition:'outEnd'}));
 kpi(s,0.5,5.0,2.9,String(D.entradas),'entradas en el registro',C.accent1);kpi(s,3.6,5.0,2.9,String(D.extractos_leidos),'extractos literales con localizador',C.accent2);
 kpi(s,6.7,5.0,2.9,String(D.niveles['SOLO-SNIPPET']),'pistas de buscador: no respaldan afirmaciones',C.accent3);kpi(s,9.8,5.0,3.0,'0','libros y tesis leídos en texto completo',C.accent4);
 s.addNotes('Las pistas de buscador se listan por si una persona puede abrirlas.')}
/* 6 causas */
sec('Análisis de causa raíz');
{const s=S('Lo respaldado se limita al rodamiento en general: contaminación, lubricación, ajustes, instalación y desalineación','Shanyavskiy y Soldatenkov (2022); Goode (1988); Lillelund et al. (2025); Kenworthy et al. (2023)');
 kpi(s,0.5,1.4,3.9,'90 %','de fallas prematuras de rodamientos de bolas de bombas, por cuatro causas (resumen de 1988, atribución del autor)',C.accent3);
 kpi(s,4.7,1.4,3.9,'L10','vida que alcanza o supera el 90 % de la población, solo en condiciones convencionales',C.accent2);
 kpi(s,8.9,1.4,3.9,'0','fuentes leídas sobre cavitación, sellos o recirculación',C.accent1);
 card(s,0.5,2.8,6.1,3.8,'Causas de daño que listan las fuentes',['Contaminación y corrosión asociada','Mala lubricación o falla del lubricante','Ajustes inadecuados con sobrecalentamiento','Mala manipulación o instalación','Carga excesiva y desalineación','Desgaste y fretting'],C.accent1,{fs:16,hs:16});
 card(s,6.8,2.8,6.0,3.8,'Límites',['No hay estadística de la población de bombas','La cifra de 90 % es de un resumen y no trae base de datos','El efecto del prensaestopa en el rodamiento está solo como pista','Todo se presenta como hipótesis posible'],C.accent3,{fs:16,hs:16});
 s.addNotes('El 90 % no debe leerse como frecuencia de modos de falla de bombas.')}
/* 7 porques */
{const s=S('Cada hipótesis se explica con cinco porqués que van de la causa física a la humana y a la latente','Análisis del equipo con fuentes citadas (síntesis); a confirmar con registros del activo');
 const rows=[[hdr('Hipótesis'),hdr('Causa física'),hdr('Causa humana'),hdr('Causa latente')]];
 ['H1','H2','H5'].forEach(h=>{const c=D.pq[h];rows.push([cell(h+' '+cut(D.pq_tit[h],40),{bold:true}),cell(cut(c[1],200)),cell(cut(c[2],200)),cell(cut(c[4],200))])});
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[2.2,3.4,3.4,3.3],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:[0.4,1.35,1.35,1.35]});
 s.addText('Hay '+D.n_hip+' hipótesis en total, todas posibles; los modos propios de la bomba sin fuente leída no entran como hipótesis.',{x:0.5,y:6.05,w:12.3,h:0.55,fontSize:13,color:C.text1,margin:0,isTextBox:true,valign:'top'});
 s.addNotes('El informe HTML trae los siete encadenamientos.')}
/* 8 arbol e ishikawa */
{const s=S('El árbol y el Ishikawa separan el inicio del daño de su progreso sin detección; Mano de obra y Medio ambiente quedan sin datos','Árbol de fallas e Ishikawa del caso; clase de causa: física, humana o latente');
 const cats=Object.keys(D.ish),cols=[C.accent1,C.accent3,C.accent2,C.accent4,C.accent5,C.accent6];
 cats.forEach((c,i)=>{const x=0.5+(i%3)*4.15,y=1.4+Math.floor(i/3)*2.65;const v=D.ish[c],n=v.EVIDENCIA+v.SINTESIS;
  card(s,x,y,4.0,2.5,c+'  |  '+(n?v.EVIDENCIA+' con respaldo, '+v.SINTESIS+' síntesis':'SIN DATOS PARA ARMARLO'),n?D.ish_txt[c].map(t=>t.length>88?t.slice(0,86)+'…':t):['Datos que faltan: ver el informe HTML'],cols[i],{fs:11,hs:13})});
 s.addNotes('El árbol completo, con zoom e impresión en A4 o A3, está en el informe HTML.')}
/* 9 FMECA */
{const s=S('El FMECA lista '+D.fmeca.length+' modos de falla del rodamiento; el aporte del prensaestopa queda como vacío con la pista por leer','FMECA del caso; severidad, ocurrencia y detección: SIN DATOS PARA ARMARLO');
 const rows=[[hdr('Id'),hdr('Modo de falla'),hdr('Detección propuesta'),hdr('Tarea RCM propuesta (síntesis)')]];
 D.fmeca.forEach(m=>rows.push([cell(m.id,{bold:true}),cell(m.modo),cell(m.det,{fontSize:10}),cell(m.tarea,{fontSize:10})]));
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[0.7,3.2,4.1,4.3],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.62});
 s.addNotes('Los puntajes S, O y D los asigna quien conozca el activo.')}
/* 10 modos propios */
{const s=S('Lo propio del prensaestopa no se pudo respaldar: cada tema indica la pista que habría que leer','Pistas SOLO-SNIPPET del registro; ninguna respalda una afirmación');
 const rows=[[hdr('Modo o tema'),hdr('Estado'),hdr('Qué habría que leer')],
 [cell('Fuga de la empaquetadura que llega al soporte',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Guías de bombas con prensaestopa y drenaje del soporte (contenido comercial, sin abrir)')],
 [cell('Agua en el lubricante y vida del rodamiento',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Artículo de acceso abierto de 2020 sobre agua y fatiga de contacto; Cantley (1977), sin verificar')],
 [cell('Desgaste de la camisa del eje',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Artículo de revista minera y estudio de simulación de desgaste de empaquetadura')],
 [cell('Sobreapriete: fricción, calor y flexión del eje',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Guías de mantenimiento del prensaestopa (pistas) y ensayos de torque de empaquetadura')],
 [cell('Fuga permitida (gotas por minuto)',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Las pistas de fabricantes difieren entre sí; ninguna se usa')],
 [cell('Empaquetadura frente a sello mecánico: vida y costo',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Tesis chilenas y mexicanas listadas, sin abrir; los costos de planta los aporta la persona')]];
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[3.6,2.7,6.0],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.62});
 s.addText('Las cifras de reparto que traen las pistas (sellos 60 % a 69 %, rodamientos 22 % a 45 %) se contradicen entre sí y no se usan.',{x:0.5,y:6.0,w:12.3,h:0.6,fontSize:14,bold:true,color:C.text2,margin:0,isTextBox:true,valign:'top'});
 s.addNotes('Abrir estas fuentes requiere habilitar los dominios académicos o aportar los PDF.')}
/* 11 estrategia */
sec('Monitoreo, datos y normas');
{const s=S('Hoy no se justifica ningún modelo entrenado: procede definir, medir una línea base y detectar anomalías en sombra','Estrategia del caso (síntesis del equipo); sin datos propios ni etiquetas; resultados de bancos de rodamientos no se trasladan');
 const cols=[C.accent1,C.accent2,C.accent3,C.accent4,C.accent5,C.accent6];
 D.estrategia.forEach((e,i)=>{const x=0.5+(i%3)*4.15,y=1.4+Math.floor(i/3)*2.65;card(s,x,y,4.0,2.5,e.etapa,[cut('x? '+e.accion,300)],cols[i],{fs:12,hs:13})});
 s.addNotes('Cada etapa indica su condición para avanzar en el informe HTML.')}
/* 12 datos */
{const s=S('No hay datos abiertos de bombas con prensaestopa con tiempos hasta la falla; solo audio de bombas y bancos de rodamientos','Registro de datos abiertos del caso; MIMII (Purohit et al., 2019) y reempaquetados');
 const rows=[[hdr('Conjunto'),hdr('Contenido'),hdr('Aptitud'),hdr('Límite')],
 [cell('MIMII y reempaquetados',{bold:true}),cell('Sonidos de bombas y otras máquinas, normal y con anomalías provocadas'),cell('Diagnóstico acústico'),cell('Sin vibración, presión ni caudal; no define la bomba')],
 [cell('Conjuntos de rodamientos a la falla de banco',{bold:true}),cell('XJTU-SY (15), PRONOSTIA (16) y Paderborn (17) rodamientos de bolas'),cell('RUL y diagnóstico de rodamientos'),cell('Sin bomba ni prensaestopa; etiquetas de RUL construidas por los autores')],
 [cell('Rodamientos a la falla de banco',{bold:true}),cell('17 rodamientos de bolas con carga y velocidad variables'),cell('Analogía de vida del rodamiento'),cell('No es bomba ni campo')],
 [cell('Vida de bombas con censura',{bold:true}),cell('No se encontró'),cell('Ninguna'),cell('Weibull y RUL de la bomba no son admisibles')]];
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[3.2,3.9,2.4,2.8],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.75});
 s.addText('Sin tiempos hasta la falla no se ajusta distribución de vida; lo primero es reunir el historial de fallas con fechas y censura.',{x:0.5,y:5.5,w:12.3,h:0.7,fontSize:14,bold:true,color:C.text2,margin:0,isTextBox:true,valign:'top'});
 s.addNotes('Se podría usar el banco de rodamientos como analogía si la persona lo decide.')}
/* 13 normas */
{const s=S('Se identificaron '+D.normas+' normas y guías; las de empaquetadura tienen ediciones en conflicto y todas están pendientes de verificación oficial','Resúmenes de buscador (SOLO-SNIPPET); ninguna página oficial pudo abrirse');
 const og=Object.keys(D.org).sort((a,b)=>D.org[b]-D.org[a]);
 s.addChart(pres.charts.BAR,[{name:'Normas',labels:og,values:og.map(k=>D.org[k])}],Object.assign({},chartBase,{x:0.5,y:1.4,w:5.6,h:5.1,barDir:'bar',chartColors:['86BCB6'],title:'Normas con estado visto por organismo',showLegend:false,dataLabelPosition:'outEnd'}));
 const rows=[[hdr('Norma (según resumen)'),hdr('Uso y estado visto')],[cell('API 610 (12.ª ed., 2021) e ISO 13709',{bold:true}),cell('Bombas centrífugas; ya no son equivalentes')],[cell('EN 16752 e ISO 3069',{bold:true}),cell('Ensayo de empaquetaduras y cavidades; edición no verificada')],[cell('API 682 e ISO 21049',{bold:true}),cell('Sellos; estado en conflicto en ISO 21049')],[cell('ISO 20816-1 y -3; ANSI/HI 9.6.4',{bold:true}),cell('Vibración; ISO 10816-1 está retirada')],[cell('ISO 281 e ISO 15243',{bold:true}),cell('Vida L10 y modos de falla de rodamientos')],[cell('ISO 13373, 17359, 13379-1, 13381-1',{bold:true}),cell('Monitoreo, diagnóstico y pronóstico')],[cell('ISO 14224',{bold:true}),cell('Datos de falla (sector petróleo y gas)')],[cell('ANSI/HI 9.6.3 y 9.6.5',{bold:true}),cell('Márgenes de operación; edición en conflicto')]];
 s.addTable(rows,{x:6.3,y:1.4,w:6.5,colW:[2.9,3.6],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.5});
 s.addNotes('No hay norma específica de aprendizaje automático para mantenimiento en lo visto.')}
/* 14 brechas */
{const s=S('Siete brechas impiden pasar de hipótesis a conclusiones; cada una indica qué la cerraría','Dossier del caso, secciones SIN DATOS PARA ARMARLO');
 const rows=[[hdr('Brecha'),hdr('Estado'),hdr('Qué la cerraría')],
 [cell('Literatura de prensaestopa y empaquetadura',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Habilitar dominios académicos y de fabricantes o aportar PDF de tesis y artículos')],
 [cell('Historial de fallas con fuga y ajuste del prensaestopa',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Órdenes de trabajo con fechas, causa, definición de falla y censura')],
 [cell('Weibull y punto óptimo de reemplazo',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Tiempos hasta la falla y costos de falla y reemplazo')],
 [cell('Top real de modos de falla',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Leer las fuentes con reparto por componente (hoy pistas contradictorias)')],
 [cell('Agua en el soporte: señales y umbrales',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Leer el trabajo de vibración y aceite para agua en rodamientos (solo título visto)')],
 [cell('Severidad, ocurrencia y detección del FMECA',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Panel de expertos con el historial del activo')],
 [cell('Citas, cuartiles y verificación de normas',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Acceso a bases bibliográficas y a las páginas de los organismos')]];
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[4.2,2.8,5.3],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.6});
 s.addNotes('Estas brechas justifican las preguntas finales a la persona.')}
/* 15 hoja de ruta */
{const s=S('Propuesta en tres horizontes: abrir las fuentes y confirmar causas, medir y recién entonces modelar','Propuesta del equipo (síntesis); requiere validación y datos propios');
 card(s,0.5,1.4,4.0,5.1,'Inmediato: abrir y confirmar',['Habilitar dominios o aportar PDF de tesis y artículos de prensaestopa','Repetir los cinco frentes con acceso','Inspeccionar agua en el lubricante, camisa del eje y huella del rodamiento retirado','Medir alineación del eje y del soporte'],C.accent1,{fs:15,hs:16});
 card(s,4.7,1.4,4.0,5.1,'Corto plazo: medir',['Línea base por punto de operación con vibración, temperatura y corriente','Bitácora de intervenciones con el mismo punto de medición','Detección de anomalías en sombra','Panel de expertos para S, O y D'],C.accent2,{fs:15,hs:16});
 card(s,8.9,1.4,3.9,5.1,'Mediano plazo: decidir',['Con tiempos hasta la falla: supervivencia con censura','Con costos: LCC y reemplazo por edad','Diagnóstico supervisado solo con fallas etiquetadas propias','Recalibrar en planta, no importar parámetros de banco'],C.accent3,{fs:15,hs:16});
 s.addNotes('Los valores numéricos de umbrales, intervalos y costos son SIN DATOS PARA ARMARLO.')}
/* 16 decisiones */
{const s=S('Cuatro decisiones de la persona desbloquean el análisis de bombas con prensaestopa','Preguntas finales del equipo');
 [['1','¿Habilita los dominios académicos?','arXiv directo, Crossref, MDPI, Frontiers, Springer, repositorios universitarios y organismos de normas permitirían leer la literatura de empaquetaduras y de agua en rodamientos.',C.accent1],['2','¿Aporta PDF de tesis o artículos de prensaestopa?','Se registran como datos aportados y se leen completos, sin esperar a los dominios.',C.accent2],['3','¿Aporta el historial de fallas de sus bombas?','Fechas, horas, causa y definición de falla permiten Weibull con censura y reemplazo por edad.',C.accent3],['4','¿Autoriza guardar el dossier en el historial?','Ya está en historial/dossiers/bomba_prensaestopa_rodamientos/ de la rama de trabajo.',C.accent4]].forEach((q,i)=>{const x=0.5+(i%2)*6.25,y=1.4+Math.floor(i/2)*2.65;
  s.addShape(pres.ShapeType.roundRect,{x,y,w:6.05,h:2.5,rectRadius:0.08,fill:{color:C.background2},line:{color:q[3],width:1},objectName:'decisión '+q[0]});
  s.addShape(pres.ShapeType.ellipse,{x:x+0.2,y:y+0.2,w:0.6,h:0.6,fill:{color:q[3]},line:{color:q[3],width:0.5},objectName:'número '+q[0]});
  s.addText(q[0],{x:x+0.2,y:y+0.2,w:0.6,h:0.6,fontSize:20,bold:true,color:C.text1,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q[1],{x:x+1.0,y:y+0.2,w:4.9,h:0.7,fontSize:18,bold:true,color:C.text1,margin:0,isTextBox:true,valign:'middle'});
  s.addText(q[2],{x:x+0.2,y:y+1.05,w:5.65,h:1.35,fontSize:14,color:C.text1,margin:0,isTextBox:true,valign:'top'})});
 s.addNotes('Cada decisión tiene un efecto concreto en lo que el equipo puede afirmar.')}
/* 17-18 referencias */
{const refs=D.refs;const half=Math.ceil(refs.length/2);[refs.slice(0,half),refs.slice(half)].forEach((lst,k)=>{const s=S('Referencias principales en APA 7 ('+(k+1)+' de 2)','Registro de evidencia del caso; enlaces completos en la pestaña Referencias del informe');
 s.addText(lst.map((t,i)=>({text:t,options:{breakLine:i<lst.length-1,paraSpaceAfter:8}})),{x:0.5,y:1.3,w:12.3,h:5.3,fontSize:11,color:C.text1,margin:0,isTextBox:true,valign:'top'})})}
(async()=>{await pres.writeFile({fileName:'deck.pptx'});await applyTheme('deck.pptx',THEME);console.log('ok')})();
