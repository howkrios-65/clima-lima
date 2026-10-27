const pptxgen=require('pptxgenjs');const fs=require('fs');
const SK='/root/.claude/skills/synced/7fd509e0-a6d1-4387-9ddc-c3e2303bdaa3_ca63f8bb-a2bd-43d4-be0f-2a8f777623d1/pptx/scripts/apply_theme.js';
const {applyTheme}=require(SK);
const D=JSON.parse(fs.readFileSync('data.json','utf8'));
const THEME={name:'Confiabilidad baby',headFontFace:'Cambria',bodyFontFace:'Calibri',colors:{dk1:'22313F',lt1:'FFFFFF',dk2:'3E5871',lt2:'EAF3F8',accent1:'5B9FCF',accent2:'6FB98D',accent3:'F0B784',accent4:'C8AAD6',accent5:'86BCB6',accent6:'ECD27A',hlink:'3B7FB5',folHlink:'7A6FA0'}};
const pres=new pptxgen();pres.layout='LAYOUT_WIDE';pres.theme={headFontFace:'Cambria',bodyFontFace:'Calibri'};pres.title='Falla de la chumacera de polea de faja transportadora';pres.author='HOWK RIOS - CONFIABILIDAD';
const C=pres.SchemeColor;
pres.defineSlideMaster({title:'CONTENIDO',background:{color:C.background1},objects:[
 {text:{text:'HOWK RIOS - CONFIABILIDAD  |  Chumacera de polea de faja transportadora',options:{x:0.5,y:7.08,w:9,h:0.3,fontSize:10,color:C.text2,margin:0,isTextBox:true}}}],
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

/* 1 portada */
sec('Inicio');
{const s=pres.addSlide({masterName:'PORTADA',sectionTitle:SEC});
 s.addText('Falla de la chumacera de polea de faja transportadora',{x:0.8,y:1.9,w:11.5,h:1.7,fontFace:'Cambria',fontSize:40,bold:true,color:C.background1,margin:0,valign:'top',isTextBox:true});
 s.addText('Dossier de confiabilidad con evidencia científica: causas raíz, pronóstico de vida útil y brechas',{x:0.8,y:3.75,w:11,h:0.9,fontSize:20,color:C.accent1,margin:0,isTextBox:true,valign:'top'});
 s.addText('HOWK RIOS - CONFIABILIDAD',{x:0.8,y:5.3,w:8,h:0.4,fontSize:16,bold:true,color:C.background1,charSpacing:3,margin:0,isTextBox:true});
 s.addText('Informe del 27 de octubre de 2026  |  Todo respaldado por fuente o declarado SIN DATOS PARA ARMARLO',{x:0.8,y:5.75,w:11.5,h:0.4,fontSize:12,color:C.accent5,margin:0,isTextBox:true});
 s.addNotes('Portada. El trabajo no inventa datos: cada afirmación lleva su fuente leída; lo que no la tiene queda como SIN DATOS PARA ARMARLO.')}
/* 2 resumen ejecutivo */
{const s=S('Lubricación, contaminación y desalineación son las causas más respaldadas, pero sin datos de planta no se pueden confirmar ni pronosticar la vida','Dossier del caso, 14 secciones; registro de evidencia con '+D.entradas+' entradas');
 card(s,0.5,1.4,4.0,5.2,'Qué sabemos',['Las fuentes leídas listan carga excesiva, desalineación, ajustes apretados, falla de lubricante, desgaste, corrosión y fretting como causas de daño de rodamientos','El defecto progresa en 4 etapas espectrales; la kurtosis detecta lo incipiente y luego vuelve a lo normal','En un banco de ensayo (carga más alta, 25 % de censura), un método de supervivencia pronostica el tiempo a la falla con MAE de 12,6 a 14,7 min','La exactitud de un diagnóstico cae de 97,58 % a 64,38 % según cómo se parte el conjunto'],C.accent2,{fs:14,hs:15});
 card(s,4.7,1.4,4.0,5.2,'Qué no sabemos',['Frecuencia de fallas por componente de poleas y fajas','Parámetros Weibull y curva de la bañera de chumaceras de polea','Costos de falla y de reemplazo, punto óptimo y LCC','Intervalo P-F y duración de cada etapa','Citas y cuartiles de las fuentes (bases bibliográficas bloqueadas)','Verificación oficial de las 43 normas identificadas'],C.accent3,{fs:14,hs:15});
 card(s,8.9,1.4,3.9,3.0,'Qué recomendamos',['Confirmar las 3 hipótesis con registros e inspección del activo','Evaluar vibración (envolvente) combinada con aceite y temperatura','Recolectar datos con definición de falla y censura'],C.accent1,{fs:13,hs:15});
 kpi(s,8.9,4.55,1.85,String(D.docs_leidos),'documentos leídos de '+D.docs_total,C.accent1);kpi(s,10.95,4.55,1.85,String(D.normas),'normas con estado visto',C.accent2);
 kpi(s,8.9,5.8,1.85,String(D.replicas),'réplicas de figuras y tablas',C.accent3);kpi(s,10.95,5.8,1.85,String(D.cifras),'cifras con su condición',C.accent4);
 s.addNotes('Mensaje principal: hay respaldo para plausibilidad de causas, no para su ocurrencia en este activo.')}
/* 3 contexto */
sec('Problema y método');
{const s=S('La literatura no trae estadística de fallas de chumaceras de polea; las cifras más cercanas son de rodillos y de bombas','Wijaya et al. (2021); Goode (1988); Kenworthy et al. (2023); Shanyavskiy y Soldatenkov (2022)');
 kpi(s,0.5,1.4,3.9,'> 50 %','de las fallas de fajas se debe a rodillos defectuosos (cita de segunda mano; no son poleas)',C.accent1);
 kpi(s,4.7,1.4,3.9,'90 %','de las fallas prematuras de rodamientos de bolas de bombas, por cuatro causas (resumen de 1988)',C.accent3);
 kpi(s,8.9,1.4,3.9,'L10','vida que alcanza o supera el 90 % de la población, solo en condiciones convencionales',C.accent2);
 card(s,0.5,2.8,6.1,3.8,'Causas de daño que listan las fuentes',['Lubricación impropia o falla del lubricante','Contaminación y corrosión asociada','Desalineación del eje y del soporte','Carga excesiva; ajustes apretados con sobrecalentamiento','Mala manipulación o instalación del rodamiento','Desgaste y fretting (micro-movimiento)'],C.accent1,{fs:16,hs:16});
 card(s,6.8,2.8,6.0,3.8,'Por qué importa para la chumacera de polea',['La vida nominal L10 no cubre estas causas: solo fatiga bajo condiciones convencionales','Los resultados publicados vienen de bancos y de otros activos, desde 600 rpm','Una polea lenta de faja no está representada: los valores no se trasladan','Todo lo que sigue se presenta como hipótesis posible hasta tener datos del activo'],C.accent3,{fs:16,hs:16});
 s.addNotes('Las cifras de rodillos y de bombas son de segunda mano y no deben leerse como frecuencia de chumaceras de polea.')}
/* 4 método */
{const s=S('Un equipo de 20 agentes con ficha de ocho bloques y compuertas de evidencia produce el dossier','Protocolo del equipo; kit de cálculo con pruebas automáticas');
 const pasos=[['1 Intake','La persona nombra el modo de falla; el líder pregunta'],['2 Búsqueda','5 frentes en paralelo: modos, monitoreo, vida, lubricación, normas'],['3 Lectura','Lectores de texto completo extraen tablas con extracto literal'],['4 Análisis','ACR, árbol, Ishikawa, FMECA, vida, predictivo, costos'],['5 Compuertas','Todo número debe estar literal en su fuente'],['6 Verificación','Verificador independiente, 4 rondas'],['7 Entrega','HTML, mapa de agentes, guía y presentación']];
 pasos.forEach((p,i)=>{const x=0.5+i*1.78;s.addShape(pres.ShapeType.roundRect,{x,y:1.45,w:1.6,h:1.75,rectRadius:0.08,fill:{color:i%2?C.background2:C.accent1},line:{color:C.accent1,width:1},objectName:'paso '+p[0]});
  s.addText(p[0],{x:x+0.08,y:1.5,w:1.44,h:0.4,fontSize:13,bold:true,color:i%2?C.text1:C.background1,margin:0,isTextBox:true});
  s.addText(p[1],{x:x+0.08,y:1.92,w:1.44,h:1.25,fontSize:11,color:i%2?C.text1:C.background1,margin:0,isTextBox:true,valign:'top'});
  if(i<6)s.addText('›',{x:x+1.6,y:2.0,w:0.18,h:0.4,fontSize:20,color:C.text2,margin:0,isTextBox:true,align:'center'})});
 card(s,0.5,3.5,4.0,3.1,'Reglas del equipo',['Nada se inventa','Sin evidencia: SIN DATOS PARA ARMARLO','Referencias en APA 7 con enlace','Sin nombres de empresas','Cálculos con el kit, no a mano'],C.accent2,{fs:14,hs:15});
 card(s,4.7,3.5,4.0,3.1,'Compuertas automáticas',['El nivel de lectura se deriva del acceso real','Cifras y réplicas: número literal en el extracto','Hipótesis nunca pasan de posible sin caso real','Ítems sin fuente válida se eliminan y se listan'],C.accent1,{fs:14,hs:15});
 card(s,8.9,3.5,3.9,3.1,'Aprendizaje continuo',['Cada corrección queda en el historial','Reglas candidatas en cuarentena','La persona aprueba lo permanente','Los 4 agentes nuevos (papers, réplicas, ranking, diseño) se suman al próximo caso'],C.accent3,{fs:14,hs:15});
 s.addNotes('El líder envía a cada agente un encargo con ROL, TAREA, CONTEXTO, RAZONAMIENTO, CONDICIONES DE CIERRE, FEEDBACK, ALMACENAMIENTO Y MEMORIA y SALIDA.')}
/* 5 evidencia */
{const s=S('Se leyeron '+D.docs_leidos+' documentos de '+D.docs_total+' registrados, sobre todo preprints recientes: falta lectura de libros y tesis','Registro de evidencia del caso; nivel de lectura derivado del acceso');
 const tl={paper:'Artículos arbitrados',preprint:'Preprints',repositorio:'Datos y repositorios',tesis:'Tesis',libro:'Libros',norma:'Normas'};
 const ks=Object.keys(D.tipos);s.addChart(pres.charts.BAR,[{name:'Documentos leídos',labels:ks.map(k=>tl[k]||k),values:ks.map(k=>D.tipos[k])}],Object.assign({},chartBase,{x:0.5,y:1.4,w:6.1,h:3.4,barDir:'bar',chartColors:['5B9FCF'],title:'Documentos leídos por tipo de fuente',showLegend:false,dataLabelPosition:'outEnd'}));
 const ys=Object.keys(D.anios);s.addChart(pres.charts.BAR,[{name:'Documentos',labels:ys,values:ys.map(k=>D.anios[k])}],Object.assign({},chartBase,{x:6.8,y:1.4,w:6.0,h:3.4,barDir:'col',chartColors:['6FB98D'],title:'Documentos leídos por año de publicación',showLegend:false,dataLabelPosition:'outEnd'}));
 kpi(s,0.5,5.0,2.9,String(D.entradas),'entradas en el registro',C.accent1);kpi(s,3.6,5.0,2.9,String(D.extractos_leidos),'extractos literales con localizador',C.accent2);
 kpi(s,6.7,5.0,2.9,String(D.niveles['SOLO-SNIPPET']),'pistas de buscador: no respaldan afirmaciones',C.accent3);kpi(s,9.8,5.0,3.0,'0','libros y tesis leídos en texto completo',C.accent4);
 s.addNotes('Los libros y tesis siguen pendientes: los repositorios universitarios y de libros están bloqueados en este entorno.')}
/* 6 ACR */
sec('Análisis de causa raíz');
{const s=S('Cada hipótesis se explica con una cadena de cinco porqués que va de la causa física a la humana y a la latente','Análisis del equipo con fuentes citadas (síntesis); a confirmar con registros del activo');
 const cut=t=>String(t).replace(/^[^?]*\?\s*/,'').replace(/^Posible respuesta[^:]*:\s*/,'').slice(0,210);
 const rows=[[hdr('Hipótesis'),hdr('Causa física'),hdr('Causa humana (práctica o decisión)'),hdr('Causa latente (gestión)')]];
 const nom={H1:'H1 Lubricación inadecuada',H2:'H2 Contaminación',H3:'H3 Desalineación'};
 ['H1','H2','H3'].forEach(h=>{const c=D.pq[h];rows.push([cell(nom[h],{bold:true}),cell(cut(c[1])),cell(cut(c[2])),cell(cut(c[4]))])});
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[2.0,3.4,3.5,3.4],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:[0.4,1.35,1.35,1.35]});
 s.addText('Las otras seis hipótesis (carga excesiva, ajustes, instalación, fatiga normal, detección tardía y mecanismos secundarios) quedan en estado posible. Ninguna está confirmada: no hay caso real.',{x:0.5,y:6.05,w:12.3,h:0.55,fontSize:13,color:C.text1,margin:0,isTextBox:true,valign:'top'});
 s.addNotes('La clasificación en física, humana y latente sigue el marco de análisis de causa raíz; el contenido de cada eslabón es síntesis con fuentes citadas.')}
/* 7 arbol */
{const s=S('El árbol de fallas separa el inicio del daño de su progreso sin detección, con causas físicas, humanas y latentes','Árbol del caso (nodos N0 a N18); borde continuo = respaldo directo, discontinuo = síntesis');
 const box=(x,y,w,h,t,col,dash,fs)=>{s.addShape(pres.ShapeType.roundRect,{x,y,w,h,rectRadius:0.06,fill:{color:C.background1},line:{color:col,width:1.25,dashType:dash?'dash':'solid'},objectName:'nodo '+t.slice(0,20)});s.addText(t,{x:x+0.06,y:y+0.03,w:w-0.12,h:h-0.06,fontSize:fs||11,color:C.text1,margin:0,isTextBox:true,valign:'middle'})};
 box(0.5,3.3,2.2,1.1,'N0 Falla funcional de la chumacera: pérdida de soporte y giro  (AND)',C.text2,true);
 box(3.2,1.6,2.6,1.0,'N1 Se inicia un daño en el rodamiento o su montaje  (OR)',C.accent1,true);box(3.2,5.0,2.6,1.0,'N12 El daño progresa sin detección oportuna  (OR)',C.accent3,true);
 const f=[['N2 Fatiga normal (fin de vida)',C.accent1,false],['N3 Causas fuera de lo convencional: lubricación, contaminación, desalineación, carga, ajustes, instalación',C.accent1,false],['N16 Causas latentes de gestión',C.accent4,true]];
 f.forEach((t,i)=>box(6.3,1.2+i*0.95,3.4,0.85,t[0],t[1],t[2]));
 box(10.0,3.1,2.8,0.85,'N17 Prácticas sin control suficiente (latente)',C.accent4,true);box(10.0,4.05,2.8,0.85,'N18 Selección basada solo en L10 (latente)',C.accent4,true);
 const g=[['N13 Indicador poco sensible o tardío (humana)',C.accent3,false],['N14 Umbrales sin sustento o modelos que no generalizan (humana)',C.accent3,false],['N15 Monitoreo sin combinar técnicas (latente)',C.accent4,true]];
 g.forEach((t,i)=>box(6.3,4.3+i*0.85,3.4,0.75,t[0],t[1],t[2]));
 const elbow=(x1,y1,x2,y2)=>{const m=(x1+x2)/2,ln=(a,b,c,d)=>s.addShape(pres.ShapeType.line,{x:Math.min(a,c),y:Math.min(b,d),w:Math.abs(c-a)||0.001,h:Math.abs(d-b)||0.001,line:{color:C.text2,width:0.75}});ln(x1,y1,m,y1);ln(m,y1,m,y2);ln(m,y2,x2,y2)};
 [[2.7,3.85,3.2,2.1],[2.7,3.85,3.2,5.5],[5.8,2.1,6.3,1.625],[5.8,2.1,6.3,2.575],[5.8,2.1,6.3,3.525],[5.8,5.5,6.3,4.675],[5.8,5.5,6.3,5.525],[5.8,5.5,6.3,6.375],[9.7,3.525,10.0,3.525],[9.7,3.525,10.0,4.475]].forEach(l=>elbow(l[0],l[1],l[2],l[3]));
 s.addText('Borde azul: causa física',{x:10.0,y:5.5,w:2.5,h:0.3,fontSize:12,bold:true,color:C.accent1,margin:0,isTextBox:true});s.addText('Borde naranja: causa humana',{x:10.0,y:5.8,w:2.5,h:0.3,fontSize:12,bold:true,color:C.accent3,margin:0,isTextBox:true});s.addText('Borde lila: causa latente',{x:10.0,y:6.1,w:2.5,h:0.3,fontSize:12,bold:true,color:C.accent4,margin:0,isTextBox:true});
 s.addNotes('El diagrama completo, con zoom, mano de desplazamiento e impresión en A4 o A3, está en la pestaña Modos y causas del informe HTML.')}
/* 8 ishikawa */
{const s=S('El Ishikawa reúne '+Object.values(D.ish).reduce((a,v)=>a+v.EVIDENCIA+v.SINTESIS,0)+' causas en seis ramas; solo '+Object.values(D.ish).reduce((a,v)=>a+v.EVIDENCIA,0)+' tienen respaldo directo','Ishikawa del caso; ramas Mano de obra y Medio ambiente con SIN DATOS PARA ARMARLO parcial');
 const cats=Object.keys(D.ish),cols=[C.accent1,C.accent3,C.accent2,C.accent4,C.accent5,C.accent6];
 cats.forEach((c,i)=>{const x=0.5+(i%3)*4.15,y=1.4+Math.floor(i/3)*2.65;card(s,x,y,4.0,2.5,c+'  |  '+D.ish[c].EVIDENCIA+' con respaldo, '+D.ish[c].SINTESIS+' síntesis',D.ish_txt[c].map(t=>t.length>88?t.slice(0,86)+'…':t),cols[i],{fs:11,hs:13})});
 s.addNotes('Cada causa del HTML dice por qué podría ocurrir y cómo verificarla.')}
/* 9 FMECA */
{const s=S('El FMECA lista 8 modos de falla con detección y tarea propuesta; severidad, ocurrencia y detección quedan para un experto','FMECA del caso; escalas S-O-D: SIN DATOS PARA ARMARLO');
 const rows=[[hdr('Id'),hdr('Modo de falla'),hdr('Detección propuesta'),hdr('Tarea RCM propuesta (síntesis)')]];
 D.fmeca.forEach(m=>rows.push([cell(m.id,{bold:true}),cell(m.modo.slice(0,70)),cell(m.det.slice(0,100)+'…',{fontSize:10}),cell(m.tarea.slice(0,115)+'…',{fontSize:10})]));
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[0.7,3.4,4.0,4.2],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.55});
 s.addNotes('Los puntajes S, O y D no se inventan: los asigna quien conozca el activo.')}
/* 10 degradacion */
sec('Detección y pronóstico');
{const s=S('El defecto progresa en cuatro etapas y cada técnica de monitoreo ve solo parte de ellas','Lillelund et al. (2024); Jayaswal et al. (2008); Burda et al. (2022); Lillelund et al. (2025)');
 const et=[['Etapa 1 Ultrasónica','Frecuencias ultrasónicas solo con sensores especializados; sin defectos visibles',C.accent1],['Etapa 2 Resonancia natural','Señales alineadas con la resonancia de las piezas; primeros defectos en inspección',C.accent2],['Etapa 3 Frecuencias de defecto','BPFO, BPFI, BSF y FTF con armónicos: el defecto se extiende',C.accent3],['Etapa 4 Final','Precede a la falla total; ruido de fondo aleatorio',C.accent4]];
 et.forEach((e,i)=>card(s,0.5+i*3.1,1.4,3.0,1.6,e[0],[e[1]],e[2],{fs:11,hs:13}));
 const rows=[['Ultrasonido y alta frecuencia',0,2],['Kurtosis (vuelve a lo normal al extenderse)',0,2],['Envolvente (banda impulsiva)',0.7,3],['Espectro de velocidad y RMS (síntesis)',2.4,4]],x0=4.2,w1=8.6/4;
 rows.forEach((r,i)=>{const y=3.45+i*0.55;s.addText(r[0],{x:0.5,y,w:3.6,h:0.4,fontSize:12,color:C.text1,margin:0,isTextBox:true,valign:'middle'});s.addShape(pres.ShapeType.roundRect,{x:x0+r[1]*w1,y:y+0.05,w:(r[2]-r[1])*w1,h:0.3,rectRadius:0.15,fill:{color:[C.accent1,C.accent3,C.accent2,C.accent4][i]},line:{color:C.background1,width:0.5},objectName:'ventana '+r[0]})});
 s.addText('Aceite, temperatura y termografía: SIN DATOS PARA ARMARLO sobre su etapa; combinar técnicas mejora la confianza',{x:0.5,y:5.65,w:8.6,h:0.5,fontSize:12,color:C.text1,margin:0,isTextBox:true,valign:'top'});
 s.addText('Intervalo P-F y duración de las etapas: SIN DATOS PARA ARMARLO. Esquema cualitativo.',{x:0.5,y:6.15,w:12.3,h:0.4,fontSize:12,bold:true,color:C.text2,margin:0,isTextBox:true});
 s.addNotes('Las barras indican en qué etapas cada técnica tiene respaldo de ver el defecto; no son duraciones.')}
/* 11 RUL */
{const s=S('En un banco de ensayo, en la condición de mayor carga, los modelos de supervivencia pronostican el tiempo a la falla con error de 12,6 a 18,5 minutos','Lillelund et al. (2025), banco XJTU-SY, condición C1 (12,0 kN, 2100 rpm), 25 % de censura; error absoluto medio');
 s.addChart(pres.charts.BAR,[{name:'MAE (min)',labels:D.mae.map(m=>m[0]),values:D.mae.map(m=>m[1])}],Object.assign({},chartBase,{x:0.5,y:1.4,w:7.4,h:5.1,barDir:'col',chartColors:['5B9FCF'],title:'MAE del tiempo a la falla por modelo (min)',showLegend:false,dataLabelPosition:'outEnd',dataLabelFormatCode:'0.0'}));
 card(s,8.1,1.4,4.7,2.6,'Qué muestra',['CoxPH 14,7 min (IC 95 %: 13,6 a 15,8)','Bosques de supervivencia aleatorios 12,6 min (11,8 a 13,4)','LASSO sin censura 18,5 min (17,4 a 19,6)','Más censura empeora el error'],C.accent2,{fs:14,hs:15});
 card(s,8.1,4.15,4.7,2.4,'Por qué no se traslada',['15 rodamientos de bolas con carga de 10 a 12 kN y vidas de minutos','Censura simulada, no de flota real','Los minutos no son precisión en planta'],C.accent3,{fs:14,hs:15});
 s.addNotes('Las desviaciones de la tabla son desviaciones estándar; el resumen del paper da intervalos de confianza. No se mezclan.')}
/* 12 generalizacion */
{const s=S('La exactitud de un diagnóstico depende de cómo se parte el conjunto: de 97,58 % con pliegues por carga a 64,38 % por severidad','Sehri et al. (2025), CWRU; exactitud balanceada media; Leyva-Vazquez et al. (2026), resumen');
 const lab=D.vib_carga.map(v=>v[0]);
 s.addChart(pres.charts.BAR,[{name:'Pliegues por carga',labels:lab,values:D.vib_carga.map(v=>v[1])},{name:'Pliegues por severidad',labels:lab,values:D.vib_sev.map(v=>v[1])}],Object.assign({},chartBase,{x:0.5,y:1.4,w:8.0,h:5.1,barDir:'col',barGrouping:'clustered',chartColors:['5B9FCF','F0B784'],title:'Exactitud balanceada media (%) según la partición',dataLabelFormatCode:'0.00',showLegend:true,legendPos:'b',legendFontSize:11,legendColor:'22313F',dataLabelPosition:'outEnd'}));
 card(s,8.7,1.4,4.1,2.5,'Lectura',['La partición decide el resultado','Con los mismos métodos la exactitud baja unos 33 puntos','Desviaciones de hasta 21 puntos entre pliegues'],C.accent2,{fs:14,hs:15});
 card(s,8.7,4.05,4.1,2.5,'Otro ejemplo',['Retener una condición completa: 100 % en CWRU y 40,64 % en JNU a 1000 rpm','Una regresión logística llegó a 57,91 % en ese caso'],C.accent3,{fs:14,hs:15});
 s.addNotes('Validar por activo y por tiempo es condición para cualquier modelo propio.')}
/* 13 sensores */
{const s=S('Ninguna fuente recomienda un sensor para chumaceras de polea; hay resultados publicados en otros activos y bancos','Lectura de papers del equipo; costos, alcance y batería: SIN DATOS PARA ARMARLO');
 const rows=[[hdr('Técnica o sensor'),hdr('Resultado publicado'),hdr('Condición y límite')],
 [cell('Micrófono y autoencoder convolucional',{bold:true}),cell('AUC 0,875 frente a 0,518 del bosque de aislamiento'),cell('Cepilladora industrial; no es rodamiento ni faja')],
 [cell('Detección acústica no supervisada',{bold:true}),cell('AUC 65,92 % (dominio fuente) y 55,75 % (objetivo) en la máquina «bearing» de un desafío'),cell('Sonido de laboratorio con ruido añadido')],
 [cell('Ampliación de datos con difusión',{bold:true}),cell('CNN en CWRU de 78,665 % a 94,033 % de exactitud'),cell('Clasificación en banco, no vida remanente')],
 [cell('CNN embebida en microcontrolador',{bold:true}),cell('Exactitud 98,9 % y 19 ms por diagnóstico en CWRU'),cell('Sin sensor inalámbrico en el ensayo')],
 [cell('Ultrasonido y alta frecuencia',{bold:true}),cell('El defecto incipiente excita frecuencias desde unos 10 kHz'),cell('Sin resultado en polea lenta')],
 [cell('Vibración con aceite y termografía',{bold:true}),cell('Combinar técnicas mejora la confianza del diagnóstico'),cell('Sin etapa ni anticipación declaradas')]];
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[3.6,4.6,4.1],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.6});
 s.addText('Siguiente paso: evaluar en piloto qué técnica detecta a tiempo en una polea lenta, con datos propios y línea base por activo.',{x:0.5,y:5.85,w:12.3,h:0.6,fontSize:14,bold:true,color:C.text2,margin:0,isTextBox:true,valign:'top'});
 s.addNotes('Detalle en la pestaña Monitoreo y ML, Sensores y técnicas.')}
/* 14 banera */
{const s=S('La curva de la bañera ilustra cómo la forma β cambia la estrategia, pero no hay parámetros publicados de chumaceras de polea','Burke et al. (2019), definición de forma de bañera y familia Weibull; valores del gráfico: simulación ilustrativa');
 const xs=[],h1=[],h2=[],h3=[],ht=[];for(let i=1;i<=24;i++){const t=i*600;const hz=(t,b,e)=>b/e*Math.pow(t/e,b-1)*1000;xs.push(String(t));const a=hz(t,0.5,2500),b=1000/20000,c=hz(t,3.5,9000);h1.push(+a.toFixed(3));h2.push(+b.toFixed(3));h3.push(+c.toFixed(3));ht.push(+(a+b+c).toFixed(3))}
 s.addChart(pres.charts.LINE,[{name:'Total',labels:xs,values:ht},{name:'Mortalidad infantil',labels:xs,values:h1},{name:'Azar',labels:xs,values:h2},{name:'Desgaste',labels:xs,values:h3}],Object.assign({},chartBase,{x:0.5,y:1.4,w:7.6,h:5.1,chartColors:['22313F','F0B784','6FB98D','C8AAD6'],lineSize:2,lineDataSymbol:'none',showValue:false,title:'Simulación ilustrativa: tasa de falla por 1000 h',showLegend:true,legendPos:'b',legendFontSize:11,legendColor:'22313F'}));
 card(s,8.3,1.4,4.5,2.35,'Cómo leerla',['β menor que 1: la tasa baja con la edad','β igual a 1: tasa constante','β mayor que 1: la tasa sube (desgaste)','Suma de tres riesgos = forma de bañera'],C.accent1,{fs:12});
 card(s,8.3,3.9,4.5,2.6,'Qué falta (SIN DATOS PARA ARMARLO)',['β y η de chumaceras de polea','Tasas de falla por fase','Costos para decidir reemplazo por edad','Simulador interactivo disponible en el informe HTML'],C.accent3,{fs:12});
 s.addNotes('Los valores son de simulación y no representan el activo.')}
/* 15 normas */
sec('Normas, brechas y plan');
{const s=S('Se identificaron '+D.normas+' normas y guías aplicables al monitoreo y al pronóstico, todas pendientes de verificación oficial','Resúmenes de buscador (SOLO-SNIPPET); ninguna página oficial pudo abrirse; no hay norma específica de aprendizaje automático para mantenimiento');
 const og=Object.keys(D.org).sort((a,b)=>D.org[b]-D.org[a]);
 s.addChart(pres.charts.BAR,[{name:'Normas',labels:og,values:og.map(k=>D.org[k])}],Object.assign({},chartBase,{x:0.5,y:1.4,w:5.6,h:5.1,barDir:'bar',chartColors:['86BCB6'],title:'Normas con estado visto por organismo',showLegend:false,dataLabelPosition:'outEnd'}));
 const rows=[[hdr('Norma (edición vista)'),hdr('Uso según lo visto')],[cell('ISO 13381-1 (2025)',{bold:true}),cell('Pronóstico, base del RUL; los resúmenes dicen que reemplaza la edición 2015 (sin verificar)')],[cell('ISO 13373-1 y -3',{bold:true}),cell('Monitoreo de vibración y guía de diagnóstico')],[cell('ISO 17359 (2018)',{bold:true}),cell('Programa de monitoreo de condición')],[cell('ISO 20816-3 (2022)',{bold:true}),cell('Evaluación de vibración; reemplaza ISO 10816-3')],[cell('ISO 281 (2007)',{bold:true}),cell('Vida nominal L10; 3.ª edición en borrador')],[cell('ISO 15243 (2017)',{bold:true}),cell('Modos de falla de rodamientos y sus causas')],[cell('ISO 14224 (2016)',{bold:true}),cell('Datos de falla y mantenimiento (sector petróleo y gas)')],[cell('VDI 3832 (2013)',{bold:true}),cell('Ruido estructural de rodamientos')],[cell('ISO 23247-1, ISO/IEC 30173',{bold:true}),cell('Marco de gemelo digital')]];
 s.addTable(rows,{x:6.3,y:1.4,w:6.5,colW:[2.4,4.1],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.45});
 s.addNotes('Sin resultado: NTP, NOM, ABNT, NCh-ISO 281 y 14224, ISA y BS específicas.')}
/* 16 brechas */
{const s=S('Siete brechas de información impiden pasar de hipótesis a conclusiones; cada una indica qué la cerraría','Dossier del caso, secciones SIN DATOS PARA ARMARLO');
 const rows=[[hdr('Brecha'),hdr('Estado'),hdr('Qué la cerraría')],
 [cell('Historial de la chumacera (fechas, horas, causa)',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Órdenes de trabajo con definición de falla y censura')],
 [cell('Weibull y punto óptimo de reemplazo',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Tiempos hasta la falla del activo y costos de falla y reemplazo')],
 [cell('Top real de fallas por componente',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Leer los textos de rodillos, tesis minera y conjunto de averías (hoy solo pistas)')],
 [cell('Intervalo P-F y duración de etapas',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Mediciones periódicas con vibración, aceite y temperatura')],
 [cell('Severidad, ocurrencia y detección del FMECA',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Panel de expertos con el historial del activo')],
 [cell('Citas y cuartiles de las fuentes',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Acceso a Crossref, OpenAlex o Scopus')],
 [cell('Verificación de normas y lectura de libros y tesis',{bold:true}),cell('SIN DATOS PARA ARMARLO'),cell('Habilitar dominios de organismos y repositorios universitarios')]];
 s.addTable(rows,{x:0.5,y:1.4,w:12.3,colW:[4.2,2.8,5.3],border:{type:'solid',color:'DDE9EE',pt:0.75},fontFace:'Calibri',rowH:0.6});
 s.addNotes('Estas brechas son las que justifican las preguntas finales a la persona.')}
/* 17 hoja de ruta */
{const s=S('Propuesta de hoja de ruta en tres horizontes: confirmar causas, medir y recién entonces decidir el reemplazo y el modelo','Propuesta del equipo (síntesis); requiere validación y datos propios; no son resultados de las fuentes');
 card(s,0.5,1.4,4.0,5.1,'Inmediato: confirmar',['Inspeccionar el lubricante, los sellos y la huella del rodamiento retirado','Medir alineación del eje y del soporte','Registrar contaminación, humedad y temperatura del soporte','Definir falla funcional y censura en el sistema de órdenes'],C.accent1,{fs:15,hs:16});
 card(s,4.7,1.4,4.0,5.1,'Corto plazo: medir',['Piloto de vibración con envolvente y kurtosis más aceite y temperatura','Línea base por activo antes de fijar umbrales','Bitácora de intervenciones con el mismo punto de medición','Panel de expertos para severidad, ocurrencia y detección'],C.accent2,{fs:15,hs:16});
 card(s,8.9,1.4,3.9,5.1,'Mediano plazo: decidir',['Con tiempos hasta la falla: Weibull con censura y reemplazo por edad','Con costos: LCC y punto óptimo','Probar detección de anomalías si no hay etiquetas; validar por activo y tiempo','Repetir el dossier con las fuentes hoy bloqueadas'],C.accent3,{fs:15,hs:16});
 s.addNotes('Los valores numéricos de umbrales, intervalos y costos son SIN DATOS PARA ARMARLO hasta contar con datos propios.')}
/* 18 equipo */
{const s=S('El equipo de agentes aprende de cada corrección y deja todo en el historial del repositorio','Mapa de agentes y guía de comandos del proyecto');
 card(s,0.5,1.4,3.0,2.7,'A Investigación y lectura',['Investigador de literatura','Investigador de normas','Buscador de datos','Analista de papers'],C.accent1,{fs:14,hs:14});
 card(s,3.7,1.4,3.0,2.7,'B Análisis',['Auditor de datos','Estadística de vida','Causa raíz y FMECA','Predictivo, economía, réplicas, ranking'],C.accent2,{fs:14,hs:14});
 card(s,6.9,1.4,3.0,2.7,'C Entrega y calidad',['Integrador','Verificador independiente','Redactor','Diseñador de la interfaz'],C.accent3,{fs:14,hs:14});
 card(s,10.1,1.4,2.7,2.7,'D Memoria',['Historiador de casos','Curador de memoria','Aprendizaje por feedback'],C.accent4,{fs:14,hs:14});
 card(s,0.5,4.3,6.0,2.3,'Comandos',['/modo-de-falla  investiga un modo de falla y arma el dossier','/confiabilidad  lanza al líder y los especialistas sobre una solicitud','Mapa interactivo: docs/agentes/mapa_agentes.html'],C.accent1,{fs:14,hs:14});
 card(s,6.7,4.3,6.1,2.3,'Cómo aprende',['La persona corrige o da una regla','El agente de feedback la registra con fecha y alcance','Queda en cuarentena hasta que la persona la apruebe'],C.accent2,{fs:14,hs:14});
 s.addNotes('El líder, llamado ESTRATEGA, entrega a cada agente un encargo con la ficha de ocho bloques.')}
/* 19 decisiones */
{const s=S('Cuatro decisiones de la persona desbloquean el siguiente nivel de análisis','Preguntas finales del equipo');
 [['1','¿Habilita los dominios académicos?','Crossref, OpenAlex, arXiv directo y repositorios permitirían citas, cuartiles, libros y tesis en texto completo.',C.accent1],['2','¿Aporta el historial de la chumacera?','Fechas, horas, causa y definición de falla permiten Weibull con censura y el reemplazo por edad.',C.accent2],['3','¿Qué costos usamos?','Solo los hallados en papers o tesis; la persona puede aportar los propios si lo decide.',C.accent3],['4','¿Qué falla analizamos después?','Con los 4 agentes nuevos activos: analista de papers, replicador, rankeador y diseñador.',C.accent4]].forEach((q,i)=>{const x=0.5+(i%2)*6.25,y=1.4+Math.floor(i/2)*2.65;
  s.addShape(pres.ShapeType.roundRect,{x,y,w:6.05,h:2.5,rectRadius:0.08,fill:{color:C.background2},line:{color:q[3],width:1},objectName:'decisión '+q[0]});
  s.addShape(pres.ShapeType.ellipse,{x:x+0.2,y:y+0.2,w:0.6,h:0.6,fill:{color:q[3]},line:{color:q[3],width:0.5},objectName:'número '+q[0]});
  s.addText(q[0],{x:x+0.2,y:y+0.2,w:0.6,h:0.6,fontSize:20,bold:true,color:C.text1,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q[1],{x:x+1.0,y:y+0.2,w:4.9,h:0.7,fontSize:18,bold:true,color:C.text1,margin:0,isTextBox:true,valign:'middle'});
  s.addText(q[2],{x:x+0.2,y:y+1.05,w:5.65,h:1.35,fontSize:14,color:C.text1,margin:0,isTextBox:true,valign:'top'})});
 s.addNotes('Cada decisión tiene un efecto concreto en lo que el equipo puede afirmar.')}
/* 20-21 referencias */
{const refs=D.refs;const half=Math.ceil(refs.length/2);[refs.slice(0,half),refs.slice(half)].forEach((lst,k)=>{const s=S('Referencias principales en APA 7 ('+(k+1)+' de 2)','Registro de evidencia del caso; enlaces completos en la pestaña Referencias del informe');
 s.addText(lst.map((t,i)=>({text:t,options:{breakLine:i<lst.length-1,paraSpaceAfter:8}})),{x:0.5,y:1.3,w:12.3,h:5.3,fontSize:11,color:C.text1,margin:0,isTextBox:true,valign:'top'})})}
(async()=>{await pres.writeFile({fileName:'deck.pptx'});await applyTheme('deck.pptx',THEME);console.log('ok')})();
