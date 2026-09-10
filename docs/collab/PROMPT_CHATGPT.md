# Prompt para ChatGPT (adjuntar `main.pdf`)

---

Te adjunto `main.pdf`, un manuscrito de cosmología teórica de 57 páginas. Quiero
que trabajemos juntos en **el programa matemático y de simulación que viene
después**, no en el manuscrito actual, que ya pasó por cuatro rondas de revisión
adversarial y está en fase de release candidate.

## Tu rol

Actúa simultáneamente como:

- físico matemático (GR, teoría de campos clásica, solitones);
- analista de EDP y singularidades;
- especialista en procesos estocásticos y sistemas abiertos;
- especialista en métodos numéricos para sistemas rígidos y formación de estructura;
- referee hostil de una revista seria.

**Tu incentivo no es validar el paper.** Es encontrar qué falta, qué está mal
planteado, y qué cálculo concreto haría avanzar el programa. Si algo que te
propongo abajo es una mala idea, dilo y explica por qué. Si crees que una línea
entera es un callejón sin salida, dilo.

No me elogies el trabajo. No empieces con "este es un trabajo impresionante".
Ve directo al contenido.

## Qué es este paper y qué no

**Lo que es:** una cinética efectiva de absorción auto-reforzada con memoria para
el sector oscuro, acoplada a GR bajo hipótesis explícitas, con consecuencias
estructurales y cosmográficas demostradas, perturbaciones lineales bajo una
realización geodésica concreta, y una confrontación con datos públicos.

**Lo que explícitamente no es, y no debe convertirse en:**

- no explica la materia oscura ni la energía oscura;
- no unifica GR con mecánica cuántica;
- no afirma que los defectos *sean* materia oscura (eso es conjetura declarada);
- el resultado observacional es **nulo**: ΛCDM es preferido por evidencia
  bayesiana sobre las cinco variantes ajustadas (ln B entre −1.4 y −1.9).

**El objetivo declarado del proyecto** es dar las herramientas matemáticas y
físicas que permitirían esa identificación, dejando el matcheo con las
observaciones para trabajo posterior. Trabaja bajo esa premisa. No propongas
reforzar los claims observacionales.

## Estado verificado — no lo rehagas

Esto ya está demostrado, testeado y verificado independientemente. Dalo por
hecho salvo que encuentres un error concreto:

**Cinética y estocástico**
- La ley de memoria τ_M Ṁ = f − M es exactamente el promedio de una ley de
  relajación por unidad con tiempo de relajación **común** (hipótesis más
  fuerte, no más débil).
- Límite determinista con convergencia en probabilidad (Kurtz).
- Teorema de histéresis: con a(t) **prescrito**, dos soluciones que alcanzan la
  misma f\* con M₁ > M₂ satisfacen f₁ ≥ f₂ después, estrictamente, y acumulan
  distinto vacío. Sistema cooperativo, Kamke–Müller. Verificado: 0 violaciones
  en 2000 combinaciones aleatorias de (α, β, τ, Γ₀, f\*, M₁, M₂).
- Cambio de tiempo por hazard acumulado: ley binomial **exacta** sólo si Γ es
  independiente del estado. La ley reforzada no lo es.
- Capa límite del residuo: s\* = N^{−1/g}.

**Cosmología homogénea**
- Positividad estructural (cada flujo de salida proporcional a la densidad del
  sector donante). Criterio donante-vs-receptor.
- Atractor de de Sitter sin que H crezca nunca.
- j ≥ 1 + 2Ω_r, con neutrinos masivos incluidos (su contribución es no negativa
  y refuerza la cota).
- Fórmula del snap verificada contra diferencias finitas del jerk a 1.6×10⁻⁶.
- La cota déficit→jerk **no aplica** a este modelo: su hipótesis (q no
  decreciente hasta hoy) falla en 400 de 400 sorteos del prior, porque q tiene
  su máximo exactamente en z_act y decae desde ahí.

**Cáusticas (§11.5)** — resultado negativo, ya establecido:
- Solución local exacta ρ_I(τ) = ρ_I(τ₀) exp[−∫(Θ+Γ)ds].
- **Teorema A**: una tasa acotada no puede cambiar el exponente de una
  compresión no integrable, sólo la amplitud. La tasa del modelo es acotada, así
  que la conjetura original es **falsa** para el modelo publicado.
- **Teorema B**: con Θ ~ −c/(T−t) y Γ ~ g/(T−t): ρ_I finito sii g ≥ c; el vacío
  converge sii g > c estricto; ρ_D diverge para todo g si b > 0. T_μν finito sii
  g > c y b = 0.
- **Obstrucción**: b = 0 es lo que exige la regularidad, b > 0 lo que exige una
  abundancia relicta. Contradicción declarada, no resuelta.
- **Teorema C**: dicotomía covariante. La opción de tensor anisótropo sin traza
  queda subdeterminada (falta un cierre).
- **Teorema D**: el canal κ[−Θ]₊ se anula puntualmente en {Θ>0}; el enunciado
  vale en L^∞ y **falla** en todo L^p finito y bajo coarse-graining, donde
  ⟨κ[−Θ]₊⟩ está suprimido sólo como e^{−9H²/2σ²}.

**Perturbaciones**
- Independencia de b en el crecimiento lineal.
- Eliminación de θ verificada re-derivando a mano y comparando con integración
  independiente del sistema de primer orden.
- La realización geodésica es una **elección de teoría**, no una consecuencia de
  la cinética. La ley local Γ(f,M,x) sobredetermina el sistema por uno.

## Dónde creo que está débil, y donde quiero tu trabajo

Ordénalas tú por dónde crees que hay más rendimiento.

### A. La obstrucción covariante (lo más importante)

El canal que regulariza cáusticas necesita una realización covariante y no la
tenemos. La opción de tensor anisótropo sin traza Π_μν que se anula donde el
vacío es comóvil-uniforme deja el sistema subdeterminado.

**Preguntas concretas:**
1. ¿Existe un cierre para Π_μν, derivable de un principio variacional, que sea
   consistente y no introduzca modos fantasma o inestabilidad de gradiente?
2. ¿Hay un teorema no-go que descarte todos esos cierres? Un no-go sería tan
   valioso como una construcción.
3. ¿Qué pasa si se abandona el vacío exacto (p = −ρ) y se permite un fluido con
   c_s² pequeño pero no nulo? ¿Se resuelve la dicotomía al precio de qué?

### B. Microfísica de la ley de tasa

Γ = Γ₀e^{αf+βM} es un **postulado** (nivel A en la escalera del paper). El paper
propone un puente con nucleación de membranas de una cuatro-forma
(Brown–Teitelboim) pero con el caveat honesto de tasas e^{−10¹²²}.

**Preguntas:**
1. ¿Hay algún sistema físico conocido (transiciones de fase, percolación,
   cinética KJMA, nucleación asistida) del que esta ley emerja como límite
   controlado en vez de postularse?
2. El auto-refuerzo e^{αf} — ¿tiene un análogo en nucleación con liberación de
   calor latente, o en sistemas con retroalimentación de volumen barrido?
3. ¿Se puede derivar el término de memoria de un embedding markoviano concreto
   (cadena de Prony) que sea físicamente motivado y no sólo matemáticamente
   posible?

### C. El sector de defectos (aquí está lo más flojo)

Sólo hay una solución numérica B=1 del hedgehog de Skyrme, por encima de su cota
de Bogomolny. Nada más.

**Falta todo esto, y quiero que priorices:**
1. Estabilidad no lineal — ¿es realmente estable o sólo un punto crítico?
2. Cuantización rotacional (Finkelstein–Rubinstein, π₄(S³)=ℤ₂) → ¿espín ½?
3. Sectores B>1, energías de ligadura, ¿hay estados ligados?
4. Cálculo de abundancia: densidad numérica a partir de la cinética, no
   postulada.
5. ¿Sobrevive la contradicción b=0/b>0 si el defecto se forma por un mecanismo
   distinto del canal que regulariza? Esa es la salida obvia — ¿funciona?

### D. Simulaciones: la parte más débil del paper

Lo que hay:
- **Pancake de Zel'dovich 1D**, con trayectorias **prescritas** (sin
  retro-reacción gravitatoria), que **nunca cruza** la cáustica: con el perfil
  fiducial J = 1 − D cos(kq) > 0 para D < 1. Los exponentes medidos coinciden
  con κ−1 a 3–4 decimales, pero el régimen multi-flujo está **sin tocar**.
- Gillespie exacto del proceso finito-N, tres décadas en N, con una deriva
  sistemática del 5% en √N·std(f_N) que el paper ahora declara.
- Lindblad exacto hasta N=8, con error de cierre de campo medio **medido** como
  N⁻¹, no acotado.

**Preguntas concretas:**
1. ¿Cómo se simula el post-shell-crossing correctamente? ¿Vale la pena un código
   de sheets Lagrangianas, un Vlasov–Poisson 1D, o hace falta N-body?
2. La retro-reacción: ¿cuánto cambia el resultado si la conversión afecta la
   trayectoria? ¿Hay un esquema auto-consistente barato en 1D?
3. La deriva del 5% en la ley N^{−1/2} — ¿es una corrección que se anula, o un
   exponente distinto? ¿Cuántas décadas más harían falta para distinguirlo, y
   hay una forma analítica de decidirlo sin simular?
4. ¿Se puede empujar el Lindblad más allá de N=8 con permutación-simetría
   (estados de Dicke) y verificar el N⁻¹ de forma convincente?
5. ¿Qué simulación produciría un **resultado falsable nuevo** en vez de verificar
   uno ya demostrado analíticamente? Esta es la pregunta que más me importa.

### E. ¿Qué otra predicción de signo existe?

El paper tiene tres predicciones de signo falsables (j ≥ 1+2Ω_r, no-sign-flip
del sector oscuro efectivo, crecimiento y velocidad en direcciones opuestas).
Todas están por debajo de la sensibilidad actual.

**Pregunta:** ¿hay alguna otra consecuencia estructural, de la clase "el signo de
X es forzado", que sea más accesible observacionalmente? Piensa en ISW, en el
plano (j₀, s₀), en la historia de reionización, en cualquier cosa donde la
memoria deje una huella que no se pueda absorber en una reparametrización.

## Reglas de trabajo

1. **No inventes referencias.** Si citas un paper, dame arXiv ID o DOI y di si
   lo has leído o si lo conoces de segunda mano.
2. **Distingue siempre** entre lo que es un teorema, lo que es evidencia
   numérica, lo que es analogía y lo que es especulación.
3. **Si algo ya está demostrado en el PDF, no lo re-derives.** Dime dónde está y
   sigue adelante.
4. **No propongas cosas vagas** del tipo "habría que estudiar la estabilidad".
   Dime *qué* ecuación, *qué* método, *qué* resultado esperado, *cuánto* cuesta.
5. **Prioriza.** Si me das quince líneas de trabajo, no me sirve. Dame tres, en
   orden, con la razón.

## Qué quiero de vuelta

1. **Tu lectura crítica** del programa: qué de lo de arriba está mal planteado.
2. **Una lista priorizada** de 3 a 5 cálculos concretos, cada uno con: qué se
   calcula, con qué método, qué resultado lo confirmaría o refutaría, qué coste
   computacional aproximado, y qué haría por el paper II.
3. **Un no-go que valga la pena intentar**: cuál de las obstrucciones abiertas es
   más probable que se cierre con un teorema negativo limpio, que es más
   publicable que una construcción a medias.
4. **Qué NO hacer**: qué línea de las que propongo arriba abandonarías.

Empieza leyendo el PDF y dime primero, en un párrafo, qué crees que es
realmente el resultado central del paper. Quiero comparar tu lectura con la mía
antes de seguir.
