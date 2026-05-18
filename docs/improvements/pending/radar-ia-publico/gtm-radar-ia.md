# Go-to-Market: Radar IA como servicio de inteligencia

Estrategia comercial para lanzar el OPENLAB Radar como producto vendible: servicio de inteligencia continua sobre IA personalizado para empresas.

**Estado:** pendiente de ejecución
**Última actualización:** 2026-04-09
**Contexto:** Empresa pequeña (2-3 personas), base en España, sin gran presupuesto de marketing
**Doc complementario:** [implementacion-tecnica.md](implementacion-tecnica.md) — plan técnico multi-perfil

---

## Modelo de negocio

### El Radar público como demo viva

El Radar público (`radar-ia.openlabstudio.com`) no es un "freemium" — es una demostración continua del producto. El cliente lo consume, ve el valor, y cuando quiere eso mismo para su sector, habla con OPENLAB. Es el mejor argumento de venta posible: producto funcionando en producción.

### Funnel de captación

1. **Web pública** con el Radar de IA → contenido gratuito → atrae audiencia
2. **Registro email** → digest semanal gratuito vía Beehiiv → nutre la relación
3. **CTA en el digest** → "¿Quieres un Radar personalizado para tu sector/empresa? Hablemos"
4. **Venta** → Radar a medida para el cliente

### Modalidades de venta

- **Implementación + personalización**: Se monta un Radar adaptado al dominio del cliente (su industria, sus fuentes, sus keywords) y se le entrega
- **Servicio gestionado**: OPENLAB opera el Radar del cliente de forma continua, personalizado a su dominio

---

## Pricing del Radar como servicio

### Modelo escalonado

| Tier | Descripción | Precio |
|---|---|---|
| **Newsletter gratuita** | Digest semanal del Radar público de IA | 0 EUR |
| **Radar Personalizado Basic** | Radar adaptado al sector del cliente: canales, keywords y briefs diarios personalizados. KB Viewer en subdominio propio. | 500-800 EUR/mes |
| **Radar Personalizado Pro** | Basic + digest semanal ejecutivo + insights mensuales + cross-referencing con KB propia del cliente | 1.000-1.500 EUR/mes |
| **Servicio Gestionado** | OPENLAB opera el Radar del cliente end-to-end: setup, curación de fuentes, ajuste continuo de filtros, reporting mensual | 1.500-2.500 EUR/mes |

### Setup fee (one-time)

| Concepto | Precio |
|---|---|
| Configuración inicial del perfil (canales, keywords, prompts, tags) | 2.000-4.000 EUR |
| Integración con sistemas del cliente (email, Slack, Teams) | 1.000-2.000 EUR |
| Formación del equipo del cliente | 500-1.000 EUR |

### Unit economics

- Coste real de operar un perfil adicional: ~50-100 EUR/mes (Claude API + VPS marginal)
- Margen bruto por cliente: 80-90%
- Breakeven: 1-2 clientes de pago cubren el coste total de la infraestructura

---

## Canales de distribución

### Canal 1 — LinkedIn: distribución B2B principal

LinkedIn es el canal #1 para B2B de nicho: el 40% de los marketers B2B lo califican como el canal más efectivo para leads de calidad. Los perfiles personales generan 8× más engagement que las páginas de empresa.

**A) Founder-led content (coste: 0 EUR, 5-8h/semana)**

- Los founders publican 3-5 posts/semana desde sus perfiles personales, NO desde la página de empresa
- Formato estrella: carruseles (generan 11,2× más impresiones que texto)
- Temas que funcionan para IA empresarial:
  - "Lo que cambió esta semana en IA para empresas"
  - "3 errores que veo en la adopción de IA en PYMEs"
  - "Caso real: cómo [sector] está usando IA para [resultado]"
  - Resúmenes visuales de tendencias del Radar
- Vídeo vertical: genera 71% más impresiones que horizontal
- Longitud ideal: Posts de 1.200-1.500 caracteres con hook fuerte en primera línea

**B) Grupos de LinkedIn relevantes (coste: 0 EUR, 2-3h/semana)**

Grupos específicos donde participar activamente (no spamear):

1. **Artificial Intelligence, Machine Learning, Data Science & Robotics** — grupos grandes de IA
2. **Digital Transformation** — decisores en proceso de transformación
3. **CIOs / CTOs / CDOs** — C-levels de tecnología
4. **Innovación Empresarial España** — red española de innovación
5. **PYME Digital** — PYMEs en transformación digital
6. **AI in Enterprise** — foco empresarial

Táctica: Aportar valor genuino en 2-3 grupos durante 4-6 semanas antes de mencionar el servicio.

**C) LinkedIn Sales Navigator (coste: ~110 EUR/mes, desde mes 3)**

- Filtrar por: cargo (Director de Innovación, CTO, CDO, Responsable de Transformación Digital), sector, tamaño de empresa, ubicación España/Europa
- ROI reportado: 312% en 3 años (estudio Forrester)
- Crear listas de 200-500 prospects cualificados
- Mensajes personalizados (NO InMail masivo) referenciando algo específico de la empresa

**Timeline y conversión:**
- Mes 1-2: Construir audiencia con contenido (0 clientes, pero 500-1.000 seguidores cualificados)
- Mes 3-4: Primeras conversaciones de venta originadas por contenido
- Conversión esperada: 1-3% de los contactos cualificados que interactúan

### Canal 2 — Newsletter + Lead Magnets

El 81% de los marketers B2B consideran las newsletters su formato de content marketing más utilizado.

**A) Newsletter semanal gratuita vía Beehiiv (coste: 0 EUR)**

- Resumen semanal de lo más relevante en IA para empresas (generado por el Radar público)
- Formato: 3-5 noticias clave + 1 análisis profundo + 1 recurso útil
- Frecuencia: semanal (martes o miércoles por la mañana)
- Beehiiv: gratis hasta 1.000 suscriptores, tier de pago integrado
- **Objetivo:** 500 suscriptores en 6 meses, 1.000 en 12 meses

**B) Lead magnets de alta conversión**

El contenido interactivo convierte al 70% vs 36% del contenido pasivo.

- **Lead magnet #1:** "Checklist: ¿Tu empresa está aprovechando la IA?" — quiz interactivo que evalúa el nivel de madurez en IA (conversión esperada: 20-40%)
- **Lead magnet #2:** "Guía rápida: 10 casos de uso de IA por sector en España" — PDF descargable
- **Lead magnet #3:** "Mapa de herramientas IA empresariales 2026" — infografía descargable
- **Lead magnet #4:** Muestra gratuita de un briefing diario real del Radar (7 días de prueba del servicio completo)

**C) Conversión newsletter → cliente**

- Tasa de conversión típica de newsletter gratuita a servicio de pago: 1-5%
- Con 500 suscriptores cualificados: 5-25 leads calientes
- Con 1.000 suscriptores: 10-50 leads calientes
- **Clave:** El contenido gratuito (digest semanal) debe ser genuinamente útil pero incompleto — el Radar personalizado añade profundidad, personalización y la KB con cross-referencing

### Canal 3 — Partnerships con consultoras

Las consultoras que ya tienen clientes en transformación digital necesitan inteligencia actualizada sobre IA pero no tienen tiempo de generarla. El Radar es un "ingrediente" que mejora su oferta.

**Targets prioritarios en España:**

**A) Consultoras de innovación y transformación digital (mejor fit)**

- Consultoras boutique de innovación y estrategia digital
- Firmas de advisory tecnológico que asesoran a PYMEs y corporaciones
- Aceleradoras e incubadoras con portfolio de empresas en fase de adopción IA

**Modelo de partnership:**
- **White-label**: La consultora ofrece el Radar como parte de su servicio (OPENLAB cobra 200-400 EUR/mes por cliente, ellos marcan su precio)
- **Referral**: La consultora refiere clientes y recibe 15-20% de comisión recurrente
- Coste: 0 EUR iniciales, solo tiempo de negociación

**B) Despachos de abogados con práctica tech/propiedad intelectual**

- Despachos que asesoran en regulación de IA, protección de datos, compliance
- El Radar les mantiene actualizados sin esfuerzo
- Modelo: Suscripción directa del despacho (500-1.000 EUR/mes)

**C) Asociaciones sectoriales**

- Ofrecer el servicio como beneficio para miembros de asociaciones empresariales
- Modelo: precio especial para asociados, la asociación recibe comisión o lo incluye en cuota premium

**Timeline:** 3-6 meses hasta primer acuerdo operativo
**Conversión:** 1 de cada 5-8 conversaciones resulta en partnership

### Canal 4 — Cold Outreach

**Benchmarks realistas:**
- Tasa de respuesta media: 3,43% (los mejores: 10-15%)
- Tasa de conversión cold email: 1-5% (>5% = excepcional)
- C-levels responden al 6,4% cuando el outreach demuestra conocimiento real de la cuenta
- Longitud óptima: 50-125 palabras (50% más respuestas que formatos largos)
- Multi-canal (email + LinkedIn + teléfono): 40% más engagement que un solo canal

**Template de cold email para el Radar IA:**

**Asunto:** [Nombre empresa] + inteligencia IA para [sector] (personalizado)

**Cuerpo (80-100 palabras):**

> Hola [Nombre],
>
> Vi que [empresa] está [contexto: explorando IA / lanzando proyecto de automatización / contratando perfiles tech]. El ritmo al que cambia la IA hace difícil separar ruido de señal.
>
> Hemos creado un servicio de inteligencia continua sobre IA que genera briefings personalizados para empresas como la vuestra — tendencias, casos de uso en [sector], herramientas relevantes.
>
> ¿Te envío un briefing de ejemplo de esta semana? Sin compromiso.
>
> [Firma]

**Compliance legal:**
- GDPR permite cold email B2B bajo "interés legítimo" (legitimate interest)
- Obligatorio: dirección física real, opción clara de darse de baja, remitente identificable

**Volumen ejecutable por equipo pequeño:**
- 5 minutos de research por cuenta = 3-5× más respuestas que templates genéricos
- Target: 20-30 emails personalizados/semana (no más, para mantener calidad)
- Resultado esperado: 1-2 respuestas positivas/semana → 1-2 demos/mes → 1 cliente cada 2-3 meses

### Canal 5 — El propio Radar público como canal

**Este es el canal más potente y el más diferencial.** Ningún competidor tiene su producto funcionando como demo pública continua.

**A) radar-ia.openlabstudio.com como landing permanente**
- SEO orgánico: contenido fresco diario sobre IA empresarial
- CTA de registro de newsletter siempre visible
- Ejemplo de briefing real que demuestra la calidad
- Meta tags y Open Graph optimizados para compartir

**B) Cada brief publicado en Telegraph = SEO adicional**
- Los briefs públicos se indexan en Google
- Cada uno es un mini-artículo con keywords de IA empresarial
- Backlinks naturales al KB Viewer

**C) Efecto compuesto**
- A más briefs publicados, más contenido indexado, más tráfico orgánico
- El Radar se alimenta a sí mismo: genera contenido → atrae audiencia → convierte a suscriptores → convierte a clientes

---

## Estrategia Freemium: "Reverse Trial"

En lugar de un tier gratuito permanente:

**Modelo recomendado — Newsletter gratuita + Reverse Trial:**

1. **Newsletter semanal gratuita** para construir audiencia (meses 1-6) — resumen del Radar público
2. Cuando un suscriptor muestra interés, ofrecer **trial de 14 días** del servicio completo (briefings diarios personalizados a su sector)
3. Después del trial, conversión a plan de pago

**Benchmarks:**
- Tasa de conversión freemium B2B SaaS: 2-5% (top: 5-10%)
- Free trials convierten al 15-20% (mejor que freemium permanente)
- El 66% de las conversiones B2B vienen de free trials

---

## Plan de ejecución comercial: primeros 6 meses

### Mes 1-2: Fundamentos

| Acción | Horas/semana | Coste/mes |
|---|---|---|
| Lanzar newsletter semanal gratuita en Beehiiv | 4h | 0 EUR |
| Publicar 3-5 posts/semana en LinkedIn (perfiles personales) | 5h | 0 EUR |
| Crear 2 lead magnets (checklist madurez IA + guía casos de uso) | 6h (solo mes 1) | 0 EUR |
| Unirse a 3 grupos LinkedIn IA/transformación digital | 2h | 0 EUR |
| Enviar 20 cold emails personalizados/semana | 4h | 0-50 EUR |
| **Total** | **~15-20h/semana** | **0-50 EUR** |

### Mes 3-4: Aceleración

| Acción | Horas/semana | Coste/mes |
|---|---|---|
| Continuar newsletter + LinkedIn | 8h | 0 EUR |
| Activar LinkedIn Sales Navigator | 3h | ~110 EUR |
| Contactar 10 consultoras de innovación para partnership | 4h | 0 EUR |
| Primeros reverse trials de 14 días a leads calientes | 2h | 0 EUR |
| **Total** | **~17h/semana** | **~110 EUR** |

### Mes 5-6: Primeros clientes

| Acción | Horas/semana | Coste/mes |
|---|---|---|
| Continuar todo lo anterior | 12h | ~110 EUR |
| Cerrar primeros partnerships con consultoras | 3h | 0 EUR |
| Onboarding primeros clientes de pago | 5h | 0 EUR |
| **Total** | **~20h/semana** | **~110 EUR** |

### Objetivos realistas a 6 meses

- 500-1.000 suscriptores de newsletter
- 1.000-3.000 seguidores LinkedIn (founders)
- 3-8 clientes de pago
- 1-2 partnerships con consultoras activas
- Pipeline de 10-20 leads en diferentes fases

### Inversión total primeros 6 meses: 500-1.500 EUR + ~80-100h/mes de trabajo comercial

---

## Priorización: dónde poner energía primero

**Impacto alto + esfuerzo bajo (hacer YA):**
1. Newsletter semanal gratuita (el activo más importante a largo plazo)
2. LinkedIn founder-led content (3-5 posts/semana)
3. Lead magnet "Checklist madurez IA" (capitalizar el interés actual)

**Impacto alto + esfuerzo medio (mes 2-3):**
4. Cold outreach personalizado (20-30/semana)
5. Partnerships con 2-3 consultoras de innovación
6. Reverse trial de 14 días como mecanismo de conversión

**Impacto medio + esfuerzo medio (mes 3-6):**
7. LinkedIn Sales Navigator para prospecting
8. SEO con contenido del Radar público (efecto compuesto)

**Evitar por ahora (no rentable para equipo pequeño):**
- Publicidad de pago (LinkedIn Ads, Google Ads) — demasiado caro para el volumen
- Stands en ferias — ROI muy bajo
- Webinars propios — hasta tener audiencia de +500

---

## Riesgos comerciales y mitigaciones

| Riesgo | Mitigación |
|---|---|
| SEO del KB Viewer público tarda en posicionar | Distribución activa: LinkedIn, newsletter cross-promo, link en firma email |
| Pocos suscriptores en los primeros meses | Normal — el contenido se acumula y el efecto es compuesto. Foco en calidad, no volumen |
| Competencia de newsletters de IA genéricas | Diferenciación: el Radar es un producto demostrable, no solo una newsletter. El CTA es "monta uno para tu empresa" |
| Ciclo de venta largo para servicio gestionado | El reverse trial de 14 días acorta el ciclo. El cliente ya consume el producto antes de pagar |

---

## Sources (benchmarks comerciales)

- [LinkedIn Trends 2026 for B2B](https://donemaker.com/linkedin-trends-to-watch-for-2026-what-b2b-marketers/)
- [B2B LinkedIn Marketing Trends 2025](https://www.informatechtarget.com/blog/b2b-linkedin-marketing-9-trends-leading-brands-to-organic-success-in-2025/)
- [LinkedIn Marketing Strategy 2026](https://lagrowthmachine.com/linkedin-marketing-strategy-2026/)
- [13+ Data-driven LinkedIn Tactics](https://cxl.com/blog/linkedin-for-b2b-marketing/)
- [B2B Cold Email Statistics 2026](https://martal.ca/b2b-cold-email-statistics-lb/)
- [Cold Outreach Best Practices 2026](https://salesmotion.io/blog/cold-outreach-best-practices)
- [Freemium SaaS Strategy](https://softwarepricing.com/blog/freemium-saas/)
- [Lead Magnet Statistics 2025](https://mycodelesswebsite.com/lead-magnet-statistics/)
- [LinkedIn Sales Navigator ROI (Forrester)](https://www.givemeleads.io/blog/how-much-linkedin-sales-navigator-cost)
