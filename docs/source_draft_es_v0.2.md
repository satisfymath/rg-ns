# Absorción geométrica autorreforzada y sector oscuro

## Fundamentos covariantes, demostraciones condicionales, límites cuánticos y pruebas cosmológicas

**Propuesta conceptual:** David Alexander Astudillo Muñoz  
**Desarrollo y redacción:** con asistencia de inteligencia artificial  
**Versión:** 0.2, revisión sustancial del manuscrito anterior  
**Fecha de revisión:** 8 de septiembre de 2026  
**Naturaleza del documento:** manuscrito de investigación teórica y propuesta de modelo efectivo; sin revisión por pares ni ajuste a observaciones.

---

## Resumen

Se desarrolla la hipótesis de que un sustrato geométrico puede generar excitaciones propagantes y configuraciones persistentes, y que la transición hacia estas últimas puede depender de la historia y reforzarse con la conversión acumulada. El objetivo es establecer qué consecuencias matemáticas admite esta idea y qué estructuras adicionales requiere para describir materia oscura, energía oscura y física cuántica.

La construcción separa cinco objetos que no deben confundirse: una fracción de configuraciones absorbidas, un campo dinámico de orden, una densidad de energía, un tensor de energía-momento y un estado cuántico reducido. Se obtiene un proceso de nacimientos irreversible con memoria, se demuestra su límite determinista bajo hipótesis explícitas y se derivan criterios de absorción acelerada y de amplificación de perturbaciones. En relatividad general se propone un modelo homogéneo con un precursor sin presión, defectos localizados y vacío interactuante. Se demuestran positividad, conservación total, una identidad entre supervivencia y densidad comóvil, la formación condicional de un régimen acelerado y un atractor de de Sitter sin divergencia futura del parámetro de Hubble.

Se presenta una familia analíticamente soluble con tasa proporcional a la expansión. Se identifica su restricción de positividad hacia el pasado y se deriva un criterio cosmográfico: en un universo plano compuesto por componentes sin presión, radiación conservada y vacío que recibe energía, el parámetro de tercera derivada de la expansión satisface \(j\geq1+2\Omega_r\). Se construye además una acción covariante con reloj y multiplicador de Lagrange que realiza exactamente un subconjunto de las soluciones de fondo, y se identifica la condición de integrabilidad que impide extender arbitrariamente su transferencia a perturbaciones espaciales.

La conexión cuántica se desarrolla mediante Madelung, Klein–Gordon y una realización de absorción con generadores de Lindblad. El sector geométrico silencioso se ilustra con una cuatro-forma, cuyo tensor es exactamente de vacío y que no posee polarizaciones propagantes locales en cuatro dimensiones. Para el sector localizado se calcula una configuración topológica de prueba con grado entero y energía finita. Se distinguen estas demostraciones de las afirmaciones todavía abiertas sobre el origen de la mecánica cuántica, la emergencia de electromagnetismo, el espín fermiónico y la gravedad cuántica.

El resultado es un programa efectivo con consecuencias comprobables, no una demostración de unificación fundamental. Se incluyen cálculos reproducibles y controles numéricos sintéticos; estos comprueban implementaciones e identidades particulares, sin sustituir las demostraciones ni proporcionar evidencia observacional.

**Palabras clave:** geometría emergente; procesos absorbentes; memoria; vacío interactuante; materia oscura; hidrodinámica cuántica; relatividad general; solitones.

## Abstract

We develop a self-reinforced absorbing-state hypothesis for an effective geometric substrate. The construction distinguishes a converted fraction, an order parameter, energy density, stress-energy and a reduced quantum state. We derive conditional mathematical results for a finite-population jump process, its deterministic limit, a memory-dependent conversion law and a spatially flat interacting-vacuum cosmology. Exact results include comoving survival identities, positivity, bounded future expansion, conditional de Sitter asymptotics, an analytically solvable benchmark and a cosmographic inequality for the jerk parameter. A constrained-clock action realizes a restricted background completion, while a four-form provides an explicit nonpropagating vacuum sector. We also derive quantum-hydrodynamic identities and evaluate a finite-energy topological trial configuration. These results define a testable effective research program; they do not establish quantum gravity, the Standard Model or an observationally confirmed unification. Reproducible synthetic calculations accompany the mathematical analysis.

## Guía de lectura

| Parte | Contenido |
|---|---|
| 1–4 | Hipótesis, relatividad general y realizaciones del vacío |
| 5–8 | Proceso absorbente, memoria y cosmología demostrable |
| 9–10 | Predicciones, perturbaciones y restricciones covariantes |
| 11–13 | Hidrodinámica, cuántica y electromagnetismo |
| 14–15 | Defectos y absorción cuántica |
| 16–18 | Navier–Stokes, resultados numéricos y programa científico |
| Apéndices | Derivaciones auxiliares, auditoría y código reproducible |

---

## 1. Problema, hipótesis y alcance lógico

### 1.1. La pregunta investigable

La intuición inicial puede formularse así: las regiones de un sustrato exploran configuraciones; algunas configuraciones son persistentes; la acumulación previa modifica las probabilidades de transición; y los productos de esa dinámica pueden gravitar aunque sean poco visibles electromagnéticamente.

La palabra «espacio» tiene aquí dos significados distintos. En la interpretación microscópica designa un sustrato todavía desconocido. En las ecuaciones macroscópicas designa una variedad con métrica lorentziana. No se identifica ambos objetos mediante una definición: el mapa de coarse-graining que los conectaría es precisamente parte del problema pendiente.

Llamaremos **absorción efectiva** a la ausencia de retorno en la escala temporal y en el conjunto de observables considerados. Un estado absorbente no tiene por qué ser un mínimo de energía absoluta, un vacío relativista o una partícula. Esas propiedades requieren cálculos separados.

### 1.2. Hipótesis mínimas

Se adoptan las siguientes hipótesis nuevas:

1. Existen unidades o configuraciones mesoscópicas identificables, activas o absorbidas.
2. La tasa de conversión es no negativa y puede depender de una variable de memoria.
3. La descripción macroscópica admite un precursor efectivo sin presión, un producto localizado sin presión y un producto de tipo vacío.
4. Una fracción de la energía transferida alimenta cada producto.
5. En el régimen estudiado se aplican las ecuaciones de Einstein y la conservación covariante del tensor total.

La tercera hipótesis no es consecuencia de las dos primeras. Justamente por eso se estudian realizaciones explícitas del tensor de vacío y de configuraciones localizadas. Tampoco se deriva la tasa de conversión de Einstein: se especifica una ley efectiva y se calculan sus consecuencias.

### 1.3. Tres niveles de afirmación

| Nivel | Qué significa | Ejemplo |
|---|---|---|
| Identidad o resultado estándar | Sigue de ecuaciones y condiciones matemáticas declaradas | Einstein implica Friedmann bajo simetría FLRW |
| Resultado condicional del modelo | Sigue de los nuevos postulados y del sistema especificado | El vacío creciente puede dominar sin que \(H\) crezca |
| Conjetura física | Requiere una microteoría y contraste experimental | Los defectos geométricos son la materia oscura real |

Las proposiciones de este manuscrito son demostraciones analíticas bajo hipótesis explícitas. No han sido formalizadas íntegramente en un asistente de pruebas. Los controles por ordenador se identifican por separado.

### 1.4. Qué significaría unificar

Una acción que contiene gravedad y campos cuánticos es una teoría acoplada. Para demostrar una unificación fundamental habría que obtener desde un mismo sistema microscópico la estructura causal, los grados de libertad gravitatorios, la dinámica cuántica y el contenido observado de partículas e interacciones.

En particular, postular Einstein–Hilbert no demuestra la emergencia de Einstein–Hilbert; comenzar con Schrödinger no demuestra el origen de Schrödinger; introducir una conexión \(U(1)\) no demuestra que esta provenga de fluctuaciones de una métrica cuadridimensional. Esta revisión convierte esas distinciones en problemas concretos de construcción.

### 1.5. Relación con antecedentes

El vacío interactuante y las descripciones conjuntas de materia oscura y energía oscura tienen antecedentes explícitos. La formulación covariante de vacío inhomogéneo fue desarrollada, por ejemplo, por Wands, De-Santiago y Wang; los modelos con restricciones y multiplicadores que se comportan como polvo con presión también preceden a esta propuesta. La posible contribución particular aquí es la combinación delimitada de memoria, absorción reforzada y reparto del producto oscuro. No se afirma prioridad sobre resultados estándar ni originalidad matemática sin una revisión bibliográfica específica. [Vacío inhomogéneo](https://arxiv.org/abs/1203.6776), [Dust of Dark Energy](https://arxiv.org/abs/1003.5751).

---

## 2. Relatividad general: acción, conservación y expansión

### 2.1. Convenciones

Usamos \(c=\hbar=k_B=1\), salvo restauración explícita, firma \((-+++)\) y

$$
M_{\rm Pl}^2=(8\pi G)^{-1},\qquad
[x^\mu]=-1,\quad [\rho]=[p]=4,\quad [H]=[\Gamma]=1.
$$

Los corchetes indican dimensión de masa. Las fracciones \(f,M\), la razón de reparto \(b\) y el factor de escala \(a\) son adimensionales. \(V\) designa **densidad de vacío**, no volumen; un volumen físico se denota \(\mathcal V\).

Para evitar ambigüedades se reserva \(Q\) para energía transferida por unidad de volumen y tiempo, de dimensión cinco. El potencial cuántico se denota \(U_Q\). El parámetro de desaceleración será \(q_{\rm dec}\), distinto de una carga eléctrica.

Definimos

$$
[\nabla_\mu,\nabla_\nu]X^\rho
=R^\rho{}_{\sigma\mu\nu}X^\sigma,\qquad
R_{\mu\nu}=R^\rho{}_{\mu\rho\nu}.
$$

Las convenciones geométricas pueden compararse con las notas de relatividad de Carroll. Las derivaciones siguientes se presentan completas para fijar signos. [Notas de relatividad general](https://arxiv.org/abs/gr-qc/9712019).

### 2.2. Variación métrica

Sea

$$
S=\int d^4x\sqrt{-g}
\left[\frac{M_{\rm Pl}^2}{2}R+\mathcal L_{\rm matter}\right]+S_{\rm borde}.
$$

Una constante cosmológica, si existe, se incluye en \(V\); no se contabiliza otra vez. Definimos

$$
T_{\mu\nu}=-\frac{2}{\sqrt{-g}}\frac{\delta S_{\rm matter}}{\delta g^{\mu\nu}}.
$$

Las identidades de variación son

$$
\delta\sqrt{-g}=-\frac12\sqrt{-g}\,g_{\mu\nu}\delta g^{\mu\nu},
$$

$$
\delta R=R_{\mu\nu}\delta g^{\mu\nu}
 +(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)\delta g^{\mu\nu}.
$$

El segundo sumando produce una contribución de frontera. Para variaciones de soporte compacto, o con el término de borde adecuado y condiciones de Dirichlet, queda

$$
\delta S=\frac12\int d^4x\sqrt{-g}
\left(M_{\rm Pl}^2G_{\mu\nu}-T_{\mu\nu}\right)\delta g^{\mu\nu}.
$$

La arbitrariedad de la variación da

$$
\boxed{M_{\rm Pl}^2G_{\mu\nu}=T_{\mu\nu}.}
\tag{2.1}
$$

La identidad de Bianchi y la compatibilidad métrica implican

$$
\boxed{\nabla_\mu T^{\mu\nu}=0.}
\tag{2.2}
$$

Esta es conservación **local covariante**. No implica que la energía dentro de un volumen comóvil sea constante, ni garantiza una energía global única en una cosmología sin simetría temporal.

### 2.3. Transferencia entre sectores

Para \(T=T_I+T_D+T_V+T_b+T_r\), las divergencias sectoriales pueden ser distintas de cero siempre que sumen cero. Una división del tensor también debe especificar cómo se reparte cualquier energía de interacción. La contabilidad de fondo que adoptaremos es una definición efectiva, no un resultado universal de cualquier acción con cinco campos.

El tensor de vacío exacto es

$$
T_V^{\mu\nu}=-Vg^{\mu\nu},\qquad
\boxed{\nabla_\mu T_V^{\mu\nu}=-\nabla^\nu V.}
\tag{2.3}
$$

Por tanto, un vacío espacial o temporalmente variable intercambia energía-momento. Su cuatro-vector de transferencia no puede elegirse independientemente de \(V\).

### 2.4. Derivación FLRW

En el caso espacialmente plano,

$$
ds^2=-dt^2+a^2(t)\delta_{ij}dx^idx^j,\qquad H=\dot a/a.
$$

Los símbolos de Christoffel no nulos relevantes son

$$
\Gamma^0{}_{ij}=a\dot a\,\delta_{ij}=Hg_{ij},
\qquad
\Gamma^i{}_{0j}=\Gamma^i{}_{j0}=H\delta^i{}_j.
$$

Al sustituirlos en la definición de Ricci:

$$
R_{00}=-3(\dot H+H^2),\qquad
R_{ij}=(\dot H+3H^2)g_{ij},\qquad
R=6(\dot H+2H^2).
$$

En consecuencia,

$$
G_{00}=3H^2,\qquad
G_{ij}=-(2\dot H+3H^2)g_{ij}.
$$

Con \(T_{00}=\rho\) y \(T_{ij}=pg_{ij}\):

$$
\boxed{3M_{\rm Pl}^2H^2=\rho,}
\qquad
\boxed{\dot H=-\frac{\rho+p}{2M_{\rm Pl}^2}.}
\tag{2.4}
$$

Sumar \(H^2\) a la segunda expresión da

$$
\boxed{\frac{\ddot a}{a}=-\frac{\rho+3p}{6M_{\rm Pl}^2}.}
\tag{2.5}
$$

La componente temporal de (2.2), usando los Christoffel anteriores, produce

$$
\dot\rho+3H(\rho+p)=0.
\tag{2.6}
$$

Para \(p=w\rho\) constante y sin interacción,
\(\rho a^{3(1+w)}\) es constante. Polvo, radiación y vacío se diluyen como
\(a^{-3},a^{-4},a^0\), respectivamente.

### 2.5. Comprobación mediante Raychaudhuri

Para una congruencia temporal normalizada \(u^\mu u_\mu=-1\), con expansión \(\Theta\), cizalla \(\sigma_{\mu\nu}\), vorticidad \(\omega_{\mu\nu}\) y aceleración \(A^\mu=u^\nu\nabla_\nu u^\mu\),

$$
u^\mu\nabla_\mu\Theta
=-\frac{\Theta^2}{3}
-\sigma_{\mu\nu}\sigma^{\mu\nu}
+\omega_{\mu\nu}\omega^{\mu\nu}
-R_{\mu\nu}u^\mu u^\nu+\nabla_\mu A^\mu.
$$

FLRW tiene \(\Theta=3H\) y los otros tres campos cinemáticos nulos. Entonces

$$
3(\dot H+H^2)=-R_{\mu\nu}u^\mu u^\nu.
$$

La traza de (2.1) implica

$$
R_{\mu\nu}u^\mu u^\nu
=\frac{\rho+3p}{2M_{\rm Pl}^2},
$$

recuperándose (2.5). La aceleración exige una contribución apropiada a Ricci; la invisibilidad electromagnética no establece esa contribución.

---

## 3. Cómo puede gravitar una fase sin ondas locales

### 3.1. Ausencia de modos no equivale a ausencia de tensor

Un término \(-V_0\sqrt{-g}\) en la acción produce \(T_{\mu\nu}=-V_0g_{\mu\nu}\). No necesita describir una colección de partículas propagantes. Este es el ejemplo algebraico más sencillo de un sector silencioso que afecta la expansión.

Pero escribir \(V_0>0\) simplemente introduce un valor de vacío. No explica su magnitud ni su origen microscópico. Tampoco demuestra irreversibilidad.

### 3.2. Proposición 1: cuatro-forma y tensor de vacío

Sea \(C_{\mu\nu\rho}\) un potencial de tres-forma y

$$
\mathcal H_{\mu\nu\rho\sigma}=4\nabla_{[\mu}C_{\nu\rho\sigma]},
\qquad
S_4=-\frac1{2\cdot4!}\int d^4x\sqrt{-g}\,
\mathcal H_{\alpha\beta\gamma\delta}\mathcal H^{\alpha\beta\gamma\delta}.
$$

En una región conectada sin fuentes, las ecuaciones implican

$$
\mathcal H_{\mu\nu\rho\sigma}=h\,\epsilon_{\mu\nu\rho\sigma},
\qquad \partial_\mu h=0,
\qquad T^{(4)}_{\mu\nu}=-\frac{h^2}{2}g_{\mu\nu}.
\tag{3.1}
$$

**Demostración.** La variación respecto de \(C\), seguida de integración por partes, da
\(\nabla_\mu\mathcal H^{\mu\nu\rho\sigma}=0\). En cuatro dimensiones toda cuatro-forma es proporcional a la forma de volumen. Como \(\nabla_\mu\epsilon^{\mu\nu\rho\sigma}=0\), la ecuación exige que \(h\) sea constante.

La variación métrica, realizada antes de imponer la solución, da

$$
T^{(4)}_{\mu\nu}
=\frac1{3!}\mathcal H_{\mu\alpha\beta\gamma}
\mathcal H_\nu{}^{\alpha\beta\gamma}
-\frac1{2\cdot4!}g_{\mu\nu}\mathcal H^2.
$$

Con firma \((-+++)\):

$$
\epsilon_{\mu\alpha\beta\gamma}\epsilon_\nu{}^{\alpha\beta\gamma}
=-3!g_{\mu\nu},\qquad
\epsilon_{\alpha\beta\gamma\delta}\epsilon^{\alpha\beta\gamma\delta}=-4!.
$$

Por sustitución, \(T_{\mu\nu}=-h^2g_{\mu\nu}+h^2g_{\mu\nu}/2\), que prueba (3.1). En particular, \(\rho_4=h^2/2\), \(p_4=-h^2/2\). \(\square\)

Una tres-forma gauge sin masa tiene \(\binom{D-2}{3}\) polarizaciones locales; para \(D=4\) este número es cero. Equivalentemente, su única amplitud de campo es la constante de integración \(h\), no una función de onda local independiente. Los flujos y las transiciones entre ellos tienen antecedentes en la literatura de cuatro-formas. [Bousso y Polchinski](https://arxiv.org/abs/hep-th/0004134).

**Alcance.** Este ejemplo demuestra que la ausencia de ondas locales es compatible con presión negativa. Para variar \(h\) hacen falta fuentes, acoplamientos o cambios de sector; la teoría libre no produce \(Q>0\). No se identifica esta cuatro-forma con la métrica de Einstein ni se ha derivado aquí su tasa de nucleación.

### 3.3. Obstrucción para un campo de orden canónico

Considérese un campo real \(\phi\) con

$$
S_\phi=\int\sqrt{-g}\left[-\frac12(\nabla\phi)^2-W(\phi)\right]d^4x.
$$

Su ecuación es \(\Box\phi-W_{,\phi}=0\). En FLRW:

$$
\ddot\phi+3H\dot\phi+W_{,\phi}=0,
$$

$$
\rho_\phi=\frac12\dot\phi^2+W,\qquad
p_\phi=\frac12\dot\phi^2-W,\qquad
\rho_\phi+p_\phi=\dot\phi^2.
$$

Para \(\rho_\phi>0\), la igualdad exacta \(w_\phi=-1\) exige \(\dot\phi=0\). Un campo canónico rodante solo puede aproximar un vacío cuando su energía cinética es pequeña.

Esto corrige una identificación demasiado fuerte del primer borrador: no se puede imponer simultáneamente
\(\phi=f_*\!f\), \(\dot f=(1-f)\Gamma>0\) y \(p_\phi=-\rho_\phi\) exacto, manteniendo un término cinético canónico no degenerado. En esta revisión, \(f\) será una fracción estadística; \(V\) será otra variable del modelo efectivo.

### 3.4. Energía de fase y energía acumulada

Un potencial de doble pozo para una variable adimensional \(s\) puede tomarse, por ejemplo, como

$$
W(s)=W_0+\lambda s^2(1-s)^2-\epsilon(3s^2-2s^3),
\quad \lambda>3\epsilon>0.
$$

Se tiene \(W'(0)=W'(1)=0\),
\(W''(0)=2\lambda-6\epsilon>0\),
\(W''(1)=2\lambda+6\epsilon>0\),
y \(W(1)-W(0)=-\epsilon\). La parte cuártica hace que \(W\) esté acotado inferiormente.

La transición al pozo más bajo libera energía. Por sí sola no aumenta la densidad de vacío. Si una conversión alimenta un vacío creciente, debe identificarse el donante y su balance. En las secciones siguientes ese donante es \(\rho_I\).

No se obtiene una tasa mediante el mero dibujo de una barrera. Una nucleación semiclásica requeriría calcular una configuración crítica, su acción y un prefactor; además, una tasa por cuatro-volumen debe convertirse en una tasa por región antes de compararla con \(\Gamma\), que tiene dimensión de tiempo inverso.

---

## 4. Una acción covariante concreta para polvo y vacío interactuante

### 4.1. Reloj con restricción

Introducimos un escalar \(T(x)\) de dimensión temporal y un multiplicador \(\lambda(x)\) de dimensión cuatro:

$$
S_{\rm reloj}=\int d^4x\sqrt{-g}\left[
\frac{M_{\rm Pl}^2}{2}R
-\frac{\lambda}{2}\left(g^{\mu\nu}\partial_\mu T\partial_\nu T+1\right)
-V(T)\right].
\tag{4.1}
$$

Es una realización particular de la familia de teorías de fluidos con restricción. Se utiliza como construcción de existencia para un subsector efectivo, sin atribuirle novedad histórica. [Lim, Sawicki y Vikman](https://arxiv.org/abs/1003.5751).

### 4.2. Proposición 2: ecuaciones y transferencia

En la rama con gradiente temporal futuro y \(\lambda\geq0\), la acción (4.1) produce

$$
u_\mu=-\partial_\mu T,\quad u^\mu u_\mu=-1,\quad
T_{\mu\nu}=\lambda u_\mu u_\nu-Vg_{\mu\nu},
\tag{4.2}
$$

$$
Du^\mu=0,\qquad
\nabla_\mu(\lambda u^\mu)=-V_{,T},
\qquad
\nabla_\mu T_V^{\mu\nu}=V_{,T}u^\nu.
\tag{4.3}
$$

**Demostración.** La variación en \(\lambda\) impone
\((\partial T)^2=-1\), de donde \(u^2=-1\). La variación métrica da un término \(\lambda\partial_\mu T\partial_\nu T\); al evaluar la restricción, el lagrangiano material vale \(-V\). Esto da (4.2).

La variación en \(T\) da

$$
\nabla_\mu(\lambda\nabla^\mu T)-V_{,T}=0.
$$

Como \(\nabla^\mu T=-u^\mu\), se obtiene la segunda ecuación de (4.3). La simetría de \(\nabla_\mu\nabla_\nu T\) implica

$$
u^\nu\nabla_\nu u_\mu=u^\nu\nabla_\mu u_\nu
=\frac12\nabla_\mu(u^\nu u_\nu)=0.
$$

Finalmente, \(-\nabla^\nu V=-V_{,T}\nabla^\nu T=V_{,T}u^\nu\). \(\square\)

En FLRW puede elegirse \(T=t\), y entonces

$$
\dot\lambda+3H\lambda=-\dot V,\qquad
3M_{\rm Pl}^2H^2=\lambda+V.
\tag{4.4}
$$

Hay una realización exacta de polvo que transfiere energía al vacío si se escoge \(V_{,T}\geq0\).

### 4.3. Lo que todavía no realiza esta acción

La función \(V(T)\) está especificada en la acción. Una reconstrucción de \(V(T)\) a partir de una solución deseada demuestra compatibilidad de esa trayectoria, pero no deriva una ley universal de memoria. Tampoco demuestra que la evolución microscópica sea fundamentalmente irreversible.

El campo reloj y el multiplicador siguen teniendo dinámica de tipo polvo; no son equivalentes a una cuatro-forma libre. El polvo puede formar cáusticas. La ausencia de presión y de ondas sonoras no prueba regularidad global de la teoría ni ausencia de problemas a escalas pequeñas.

Por tanto, se utilizarán tres construcciones relacionadas pero distintas:

| Construcción | Qué establece | Qué no establece |
|---|---|---|
| Cuatro-forma libre | Tensor de vacío sin polarizaciones locales | Conversión creciente espontánea |
| Acción de reloj | Intercambio covariante polvo–vacío para \(V(T)\) | Memoria microscópica y estructura espacial arbitraria |
| Modelo estadístico de absorción | Conversión con historia y refuerzo | Acción gravitatoria microscópica completa |

Una teoría fundamental tendría que unir estas construcciones con un único conjunto de grados de libertad y una única contabilidad de energía.

---

## 5. Proceso absorbente: de eventos discretos a una ecuación determinista

### 5.1. Estado y tasa condicional

Considérese una región mesoscópica con \(N\) unidades etiquetadas. Sea \(K_t\) el número ya convertido y

$$
f_N(t)=K_t/N,\qquad K_t\in\{0,\ldots,N\}.
$$

Un evento convierte una unidad y nunca la devuelve al estado activo. Se especifica la intensidad total

$$
\lambda_k(M,t)=(N-k)\Gamma(k/N,M,t),
\qquad \lambda_N=0.
\tag{5.1}
$$

La tasa \(\Gamma\) es una probabilidad por unidad de tiempo **condicionada al estado y la historia codificada**. No es una probabilidad que pueda superar uno en un paso finito. En un intervalo \(\Delta t\), la probabilidad de un salto es \(\lambda_k\Delta t+o(\Delta t)\).

Que la tasa dependa de \(f_N\) introduce interacción estadística entre unidades. Una dependencia adicional en \(M\) representa información del pasado que \(f_N\) solo no contiene. El proceso puede ser markoviano en el estado ampliado \((K,M)\), aun cuando su proyección \(K\) no lo sea.

Los procesos con estados absorbentes son una clase matemática conocida; ni la presencia de absorción ni una tasa dependiente del estado demuestran una nueva fase crítica. [Hinrichsen](https://arxiv.org/abs/cond-mat/0001070).

### 5.2. Memoria causal

Sobre una línea de flujo con tiempo propio \(\tau\),

$$
\tau_M\frac{dM}{d\tau}=f-M,\qquad \tau_M>0.
\tag{5.2}
$$

La solución exacta desde \(\tau_i\) es

$$
M(\tau)=M_i e^{-(\tau-\tau_i)/\tau_M}
+\frac1{\tau_M}\int_{\tau_i}^{\tau}
e^{-(\tau-s)/\tau_M}f(s)\,ds.
\tag{5.3}
$$

Solo interviene el pasado. Los pesos de \(M_i\) y del historial suman uno, de modo que \(0\leq M\leq1\) si \(0\leq f,M_i\leq1\).

La forma covariante es \(\tau_M DM=f-M\), con \(D=u^\mu\nabla_\mu\). La elección de \(u^\mu\) es una estructura física adicional: puede corresponder al estado cosmológico del sustrato. La tasa local no debe depender instantáneamente de un promedio universal fuera de su pasado causal. Los modelos homogéneos siguientes son una reducción por simetría, no un mecanismo de comunicación superlumínica.

### 5.3. Generador, momentos y ruido

Sin memoria, la ecuación maestra es

$$
\dot P_k=\lambda_{k-1}P_{k-1}-\lambda_kP_k,
$$

con los términos inexistentes eliminados en las fronteras. Para una función de prueba \(g(f,M)\), el generador ampliado es

$$
\mathcal L_Ng
=N(1-f)\Gamma(f,M)\,[g(f+N^{-1},M)-g(f,M)]
+\frac{f-M}{\tau_M}\partial_Mg.
\tag{5.4}
$$

Tomando \(g=f\) y \(g=f^2\), se obtienen los primeros momentos infinitesimales:

$$
\frac{\mathbb E[df_N\mid\mathcal H_t]}{dt}=(1-f_N)\Gamma(f_N,M),
$$

$$
\frac{\mathbb E[(df_N)^2\mid\mathcal H_t]}{dt}
=\frac{(1-f_N)\Gamma(f_N,M)}{N}.
\tag{5.5}
$$

Por tanto,

$$
\frac{d}{dt}\mathbb E[f_N]
=\mathbb E[(1-f_N)\Gamma(f_N,M)],
$$

que en general **no** es
\((1-\mathbb E[f_N])\Gamma(\mathbb E[f_N],\mathbb E[M])\).
El promedio de una función no lineal no es la función del promedio.

En el interior del intervalo, una aproximación de difusión tendría amplitud

$$
\sqrt{\frac{(1-f)\Gamma(f,M)}{N}}.
$$

Esto no coincide en general con un ruido escogido por conveniencia, como \(\sqrt f(1-f)\). Cerca de \(f=0\), una aproximación gaussiana puede producir pasos negativos que el proceso original no permite. Para preservar exactamente las fronteras debe simularse el proceso de saltos o justificar condiciones de frontera específicas.

### 5.4. Proposición 3: límite determinista bajo condiciones suficientes

Supóngase que \(\Gamma\) es no negativa, acotada y uniformemente Lipschitz en \((f,M)\) sobre \([0,1]^2\), y que las condiciones iniciales convergen. Entonces, en todo intervalo temporal finito, el proceso definido por (5.4) converge en probabilidad a

$$
\boxed{\dot f=(1-f)\Gamma(f,M),\qquad
\tau_M\dot M=f-M.}
\tag{5.6}
$$

**Demostración.** Escribamos

$$
f_N(t)=f_N(0)+\int_0^tF(f_N(s),M_N(s))\,ds+\mathcal M_N(t),
\quad F=(1-f)\Gamma.
$$

\(\mathcal M_N\) es una martingala de saltos. Si \(\Gamma\leq G\), su variación cuadrática predecible cumple

$$
\mathbb E\langle\mathcal M_N\rangle_T\leq GT/N.
$$

Por la desigualdad maximal \(L^2\) de Doob,

$$
\mathbb E\sup_{t\leq T}|\mathcal M_N(t)|^2\leq4GT/N.
$$

La diferencia de las ecuaciones integrales para \(f_N,M_N\) y \(f,M\), usando Lipschitz, satisface

$$
\sup_{s\leq t}|X_N(s)-X(s)|
\leq |X_N(0)-X(0)|+\sup_{s\leq t}|\mathcal M_N(s)|
+L_*\int_0^t\sup_{r\leq s}|X_N(r)-X(r)|\,ds.
$$

Gronwall acota el lado izquierdo por los dos primeros términos multiplicados por \(e^{L_*t}\). La cota de Doob y la convergencia inicial dan el resultado. \(\square\)

Las hipótesis de (5.1) son materiales. Si hay saltos colectivos de tamaño macroscópico o correlaciones cuya amplitud no disminuye con \(N\), el límite puede mantener ruido y no satisfacer (5.6).

### 5.5. Tiempo de absorción finito y límite de muchas unidades

Para una tasa dependiente de \(k/N\) sin memoria y \(\Gamma\geq g>0\), el tiempo medio hasta \(K=N\), partiendo de \(k_0\), es

$$
\mathbb E[T_N]=
\sum_{k=k_0}^{N-1}\frac1{(N-k)\Gamma(k/N)}
\leq \frac1g\sum_{j=1}^{N-k_0}\frac1j.
\tag{5.7}
$$

**Demostración.** El tiempo en el estado \(k\) es exponencial de media \(1/\lambda_k\); se visitan todos los estados sucesivos una vez. La linealidad de la esperanza y la cota inferior de la tasa producen (5.7). \(\square\)

La cadena finita alcanza el estado absorbente en tiempo finito casi seguramente. En la ecuación continua con tasa acotada, \(f=1\) solo se alcanza asintóticamente desde \(f<1\). Ambos hechos son compatibles: el tiempo de absorción completa crece aproximadamente como \(\log N\) cuando las tasas se mantienen comparables.

Con \(\Gamma_0>0\) no existe una fase activa estacionaria en este modelo cerrado. Para afirmar una transición crítica, percolación o exponentes universales habría que añadir dinámica espacial y demostrar el fenómeno.

---

## 6. Monotonía, autorrefuerzo y estabilidad de la absorción

### 6.1. Proposición 4: supervivencia e invariancia

Sea \(\Gamma\geq0\) continua, localmente Lipschitz en las variables dinámicas y localmente integrable a lo largo de la solución. Para \(f_i\in[0,1)\),

$$
\boxed{1-f(t)=(1-f_i)
\exp\!\left[-\int_{t_i}^{t}\Gamma(s)\,ds\right].}
\tag{6.1}
$$

Por tanto, \(f_i\leq f(t)<1\) en todo tiempo finito con integral finita. Si \(f_i=1\), la solución es \(f=1\).

**Demostración.** Defina \(y=1-f\). Entonces \(\dot y=-\Gamma y\), cuya solución por factor integrante es (6.1). El exponencial es positivo y no creciente. La unicidad evita que otra solución cruce la frontera estacionaria. \(\square\)

Además, \(f\to1\) si y solo si \(\int_{t_i}^{\infty}\Gamma(s)\,ds=\infty\). Una cota inferior \(\Gamma\geq g>0\) a lo largo de la trayectoria es suficiente. Una cota únicamente en el punto \(f=1\), sin control uniforme de un entorno ni de la historia temporal, no justifica una cota global de convergencia.

### 6.2. Proposición 5: aceleración de la fracción

Para \(\Gamma=\Gamma(f)>0\) de clase \(C^1\) y \(0\leq f<1\),

$$
\boxed{\ddot f=(1-f)\Gamma\big[(1-f)\Gamma_{,f}-\Gamma\big].}
\tag{6.2}
$$

En consecuencia,

$$
\boxed{\ddot f>0\iff(1-f)\Gamma_{,f}>\Gamma.}
\tag{6.3}
$$

**Demostración.** Derivar \(\dot f=(1-f)\Gamma\) produce
\(\ddot f=-\dot f\Gamma+(1-f)\Gamma_{,f}\dot f\). Factorizando y usando \((1-f)\Gamma>0\), se obtienen las dos expresiones. \(\square\)

Si la tasa también depende de memoria y tiempo,

$$
\boxed{\ddot f=(1-f)\Gamma
\left[-\Gamma+\frac{d}{dt}\log\Gamma\right].}
\tag{6.4}
$$

Por tanto, el criterio general es \(d\log\Gamma/dt>\Gamma\), con derivada total sobre la trayectoria.

### 6.3. Solución exponencial exacta

Para

$$
\Gamma=\Gamma_0e^{\alpha f},\qquad \Gamma_0>0,\quad\alpha>0,
$$

separar variables e integrar da

$$
t-t_i=\frac{e^{-\alpha}}{\Gamma_0}
\left[
\operatorname{Ei}\big(\alpha(1-f_i)\big)
-\operatorname{Ei}\big(\alpha(1-f)\big)
\right].
\tag{6.5}
$$

Para comprobarlo basta derivar el lado derecho respecto de \(f\), usando
\(d\operatorname{Ei}(x)/dx=e^x/x\); resulta
\(e^{-\alpha f}/[\Gamma_0(1-f)]\), inverso de \(\dot f\).

La absorción acelera mientras \(\alpha(1-f)>1\). La tasa individual aumenta, pero el número de unidades restantes se agota. Cerca de \(f=1\), la fracción desacelera incluso con refuerzo positivo.

### 6.4. Modelo con memoria que se usará en los ejemplos

Tomaremos

$$
\boxed{\Gamma(f,M)=\Gamma_0e^{\alpha f+\beta M},\qquad
\alpha,\beta\geq0,\quad \tau_M\dot M=f-M.}
\tag{6.6}
$$

En \([0,1]^2\):

$$
\Gamma_0\leq\Gamma\leq\Gamma_0e^{\alpha+\beta}.
$$

La memoria conserva el intervalo por (5.3), y la fracción lo conserva por (6.1). Si \(\Gamma_0>0\), entonces \(f\to1\), \(M\to1\) y \(\Gamma\to\Gamma_0e^{\alpha+\beta}\).

El criterio de aceleración es

$$
\alpha(1-f)\Gamma+\frac{\beta}{\tau_M}(f-M)>\Gamma.
\tag{6.7}
$$

La contribución de memoria puede reforzar o debilitar temporalmente la aceleración según la condición inicial \(M_i\). No basta con \(\beta>0\).

### 6.5. Amplificación de diferencias entre regiones

Al linealizar (5.6) alrededor de una trayectoria homogénea se obtiene

$$
\frac{d}{dt}
\begin{pmatrix}\delta f\\ \delta M\end{pmatrix}
=
\begin{pmatrix}
A&B\\ \tau_M^{-1}&-\tau_M^{-1}
\end{pmatrix}
\begin{pmatrix}\delta f\\ \delta M\end{pmatrix},
$$

$$
A=-\Gamma+(1-f)\Gamma_{,f},\qquad
B=(1-f)\Gamma_{,M}.
\tag{6.8}
$$

Si se congelan los coeficientes, el determinante es
\(-(A+B)/\tau_M\). Para \(B\geq0\), \(A+B>0\) produce un autovalor positivo; \(A+B<0\) implica \(A<0\), traza negativa y estabilidad de ese sistema congelado.

En el punto final \((f,M)=(1,1)\), los autovalores son
\(-\Gamma_*\) y \(-1/\tau_M\), ambos negativos. En una trayectoria cambiante, los autovalores instantáneos no sustituyen la integración del sistema lineal no autónomo.

Sin memoria, la sensibilidad es exactamente

$$
\frac{\partial f(t)}{\partial f_i}
=\frac{F(f(t))}{F(f_i)},\qquad F(f)=(1-f)\Gamma(f),
\tag{6.9}
$$

para \(F(f_i)>0\). Esto se comprueba porque ambas expresiones satisfacen
\(\dot J=F'(f(t))J\), \(J(t_i)=1\). La etapa de absorción acelerada amplifica diferencias iniciales; el agotamiento puede reducirlas después. Esa consecuencia debe examinarse antes de interpretar el producto como un vacío cosmológicamente homogéneo.

---

## 7. Modelo cosmológico con dos productos y teorema de futuro regular

### 7.1. Variables y cierre homogéneo

Denotamos:

$$
\rho_I:\text{precursor activo},\quad
\rho_D:\text{producto localizado},\quad
V:\text{producto de vacío}.
$$

Los dos primeros tienen presión despreciable en este cierre. El producto \(D\) representa energía en objetos que se mueven lentamente; «localizado» por sí solo no garantiza esa ecuación de estado.

Sea \(b\in[0,1]\) la fracción de la **energía convertida** que va al producto localizado. No debe identificarse con una probabilidad de producir un objeto si sus energías de formación son distintas. El resto \(1-b\) alimenta el vacío.

El modelo de fondo, con bariones y radiación conservados, es

$$
\begin{aligned}
\dot\rho_I+3H\rho_I&=-\Gamma\rho_I,\\
\dot\rho_D+3H\rho_D&=b\Gamma\rho_I,\\
\dot V&=(1-b)\Gamma\rho_I\equiv Q_V,\\
\dot\rho_b+3H\rho_b&=0,\\
\dot\rho_r+4H\rho_r&=0,\\
\dot f&=(1-f)\Gamma(f,M),\\
\tau_M\dot M&=f-M,\\
\dot a&=Ha,\\
3M_{\rm Pl}^2H^2&=\rho_I+\rho_D+\rho_b+\rho_r+V.
\end{aligned}
\tag{7.1}
$$

Se elige la raíz positiva de Friedmann. La presión total es
\(p=\rho_r/3-V\). En una misma realización, \(V\) ya representa todo el tensor efectivo del producto homogéneo: no se suma otra vez la energía de un supuesto campo \(f\).

### 7.2. Proposición 6: identidades exactas de supervivencia y producto

Con \(a_i=1\), \(b\) constante y \(f_i<1\), el sistema (7.1) satisface

$$
\boxed{\rho_I a^3=\rho_{I i}\frac{1-f}{1-f_i},}
\tag{7.2}
$$

$$
\boxed{\rho_Da^3=\rho_{D i}
+b\rho_{I i}\frac{f-f_i}{1-f_i}.}
\tag{7.3}
$$

Cuando \(\dot f>0\), también

$$
\boxed{\frac{dV}{df}
=\frac{(1-b)\rho_{I i}}{a^3(1-f_i)}.}
\tag{7.4}
$$

**Demostración.** La primera ecuación de (7.1) da
\(d\log(\rho_Ia^3)/dt=-\Gamma\), mientras
\(d\log(1-f)/dt=-\Gamma\). Su diferencia es constante, probando (7.2), con extensión por continuidad cuando \(\rho_{I i}=0\).

La segunda ecuación da
\(d(\rho_Da^3)/dt=b\Gamma\rho_Ia^3\).
Sustituyendo (7.2) y \(\dot f=(1-f)\Gamma\), se integra directamente y se obtiene (7.3).
Dividir \(\dot V\) por \(\dot f\) y usar (7.2) da (7.4). \(\square\)

La dependencia explícita en \(a^{-3}\) muestra por qué la fracción absorbida no determina por sí sola la densidad de vacío. Una misma cantidad de conversión ocurrida en épocas de distinta dilución produce una historia diferente de \(V\).

### 7.3. Fracción estadística frente a fracción energética

En el subcaso de dos sectores \(b=0\), sin \(D,b,r\), sea
\(x=V/(\rho_I+V)\). Entonces

$$
\boxed{\dot x=(1-x)\big(\Gamma+3Hx\big).}
\tag{7.5}
$$

**Demostración.** Use \(\dot V=\Gamma\rho_I\) y
\(\dot\rho_{\rm tot}=-3H\rho_I\) al derivar el cociente \(V/\rho_{\rm tot}\). \(\square\)

El término \(3Hx(1-x)\) no aparece en la ecuación de \(f\). Incluso sin conversión, un vacío preexistente aumenta su proporción energética mientras la materia se diluye. Por eso \(f=\Omega_V\) no es una identidad admisible.

Tampoco el número de regiones absorbidas fija directamente un volumen físico. En FLRW, \(\dot{\mathcal V}=3H\mathcal V\) sigue de la métrica. Una teoría que cree unidades geométricas deberá especificar cómo cambia la métrica y cómo se define ese conteo.

### 7.4. Teorema 1: positividad, conservación y cotas globales

Supóngase:

1. \(\rho_{I i},\rho_{D i},\rho_{b i},\rho_{r i},V_i\geq0\) y suma inicial positiva.
2. \(a_i=1\), \(0\leq f_i<1\), \(0\leq M_i\leq1\), \(0\leq b\leq1\), \(\tau_M>0\).
3. \(\Gamma\) es localmente Lipschitz y \(0<g\leq\Gamma\leq G<\infty\) en el dominio físico.
4. Se mantiene el cierre homogéneo (7.1), sin sectores adicionales de presión negativa.

Entonces existe una solución única para todo tiempo futuro finito. Todas las densidades permanecen no negativas, \(f,M\in[0,1]\), \(H>0\), y

$$
\dot\rho_{\rm tot}
=-3H\left(\rho_I+\rho_D+\rho_b+\frac43\rho_r\right)\leq0,
\tag{7.6}
$$

$$
\boxed{\dot H=-\frac{\rho_I+\rho_D+\rho_b+\frac43\rho_r}
{2M_{\rm Pl}^2}\leq0,}
\tag{7.7}
$$

$$
\boxed{0<H(t)\leq H_i,\quad 1\leq a(t)\leq e^{H_i(t-t_i)},}
\tag{7.8}
$$

$$
\boxed{V_i\leq V(t)\leq V_i+(1-b)\rho_{I i}.}
\tag{7.9}
$$

**Demostración.**

La solución de cada ecuación sin fuente es un exponencial positivo multiplicado por su condición inicial. Las ecuaciones de \(D\) y \(V\) tienen fuentes no negativas, y sus soluciones por factor integrante conservan el signo. Las ecuaciones de \(f,M\) conservan el cuadrado unidad por las proposiciones anteriores.

Al sumar las cinco ecuaciones de densidad, los términos
\(-\Gamma\rho_I+b\Gamma\rho_I+(1-b)\Gamma\rho_I\) se cancelan. Esto produce (7.6), que es exactamente la continuidad total con \(p=\rho_r/3-V\). Derivar Friedmann da (7.7). De ahí \(H\leq H_i\), y al integrar \(\dot a/a=H\) se obtiene la cota superior de (7.8).

Para (7.9), como \(a\geq1\),

$$
\begin{aligned}
V(t)-V_i
&=(1-b)\int_{t_i}^t\Gamma(s)\rho_I(s)\,ds\\
&\leq(1-b)\rho_{I i}
\int_{t_i}^t\Gamma(s)e^{-\int_{t_i}^s\Gamma(r)dr}\,ds\\
&=(1-b)\rho_{I i}
\left[1-e^{-\int_{t_i}^t\Gamma(s)ds}\right]
\leq(1-b)\rho_{I i}.
\end{aligned}
$$

La densidad total no puede llegar a cero en tiempo finito. En efecto,
\(\dot\rho_{\rm tot}\geq-4H_i\rho_{\rm tot}\), y por comparación
\(\rho_{\rm tot}(t)\geq\rho_{{\rm tot},i}e^{-4H_i(t-t_i)}>0\).
En cada intervalo finito las variables quedan acotadas y la raíz de Friedmann se mantiene alejada de cero. La existencia local por Lipschitz se prolonga, dando existencia global hacia el futuro. \(\square\)

La prueba es de un sistema de ecuaciones ordinarias homogéneo. No es una demostración de existencia global para Einstein con inhomogeneidades, turbulencia, cáusticas o singularidades gravitatorias.

### 7.5. Teorema 2: vacío positivo, aceleración y límite de de Sitter

Añádase al teorema anterior una de estas condiciones:
\(V_i>0\), o bien \(b<1\) y \(\rho_{I i}>0\).
Entonces

$$
V(t)\longrightarrow V_\infty>0,\qquad
\rho_I,\rho_D,\rho_b,\rho_r\longrightarrow0,
$$

$$
\boxed{H(t)\longrightarrow H_\infty
=\sqrt{\frac{V_\infty}{3M_{\rm Pl}^2}}>0,}
\tag{7.10}
$$

$$
\boxed{a(t)e^{-H_\infty(t-t_i)}\longrightarrow C,\quad0<C<\infty.}
\tag{7.11}
$$

La expansión acelera desde algún tiempo finito en adelante.

**Demostración.** Si \(V_i=0\), la fuente \(Q_V\) es estrictamente positiva al inicio bajo la segunda alternativa. Existe entonces \(t_1>t_i\) con \(V(t_1)>0\). Por monotonía de \(V\),
\(H(t)\geq h_1=\sqrt{V(t_1)/(3M_{\rm Pl}^2)}>0\) para \(t\geq t_1\).
Así \(a(t)\geq a(t_1)e^{h_1(t-t_1)}\).

Las identidades (7.2)–(7.3) muestran que la densidad comóvil total de polvo está acotada:

$$
(\rho_I+\rho_D+\rho_b)a^3
\leq \rho_{I i}+\rho_{D i}+\rho_{b i}.
$$

El polvo y la radiación decaen exponencialmente. \(V\) es monótona, acotada por (7.9) y positiva desde \(t_1\); por tanto tiene límite positivo. Friedmann produce (7.10).

Además, \(Q_V\leq(1-b)G\rho_{I i}a^{-3}e^{-g(t-t_i)}\), por lo que
\(V_\infty-V(t)\) también decrece al menos exponencialmente. La identidad
\(3M_{\rm Pl}^2(H^2-H_\infty^2)=\rho_{\rm polvo}+\rho_r-(V_\infty-V)\)
muestra que \(H-H_\infty\) es integrable. Integrar
\(d\log a/dt-H_\infty=H-H_\infty\) da (7.11).

Finalmente,

$$
\frac{\ddot a}{a}
=\frac{2V-\rho_I-\rho_D-\rho_b-2\rho_r}{6M_{\rm Pl}^2}
\longrightarrow H_\infty^2>0.
$$

La continuidad implica aceleración desde algún tiempo finito. \(\square\)

### 7.6. Corolario: a lo sumo una transición de desaceleración a aceleración

Defina \(\rho_m=\rho_I+\rho_D+\rho_b\) y \(\mathcal A=\ddot a/a\). Del sistema:

$$
\boxed{\dot{\mathcal A}
=\frac{3Q_V+3H\rho_m+8H\rho_r}{6M_{\rm Pl}^2}\geq0.}
\tag{7.12}
$$

**Demostración.** Derive
\(\mathcal A=(2V-\rho_m-2\rho_r)/(6M_{\rm Pl}^2)\), use
\(\dot\rho_m=-3H\rho_m-Q_V\) y \(\dot\rho_r=-4H\rho_r\), y reúna términos. \(\square\)

Cuando existe materia o radiación, la desigualdad es estricta. Si la solución parte con \(\mathcal A<0\) y satisface el teorema 2, cruza \(\mathcal A=0\) exactamente una vez. Un historial que exigiera varias alternancias tardías no pertenece a este cierre.

### 7.7. Expansión acelerada y apariencia phantom

Para \(V>0\), puede definirse un parámetro contable por
\(\dot V+3H(1+w_{V,\rm eff})V=0\). Entonces

$$
w_{V,\rm eff}=-1-\frac{Q_V}{3HV}\leq-1.
\tag{7.13}
$$

Pero el tensor físico del vacío sigue teniendo \(p_V=-V\); el total satisface \(\rho+p\geq0\), y (7.7) implica \(\dot H\leq0\). No hay superaceleración \(\dot H>0\) ni un Big Rip futuro dentro de las hipótesis del teorema.

Así pueden coexistir cuatro hechos: crece \(f\), crece \(V\), aumenta \(\ddot a/a\) y disminuye \(H\). Son variables diferentes, relacionadas por ecuaciones precisas.

La cantidad (7.13) no es automáticamente el \(w(z)\) que inferiría un ajuste observacional que también supusiera materia conservada: ese ajuste cambiaría la descomposición de densidades. Esta diferencia importa al comparar con parametrizaciones de energía oscura.

---

## 8. Una familia soluble y sus límites físicos

### 8.1. Conversión proporcional a la expansión

Como referencia analítica, sea

$$
\Gamma=\xi H,\qquad \xi\geq0,\qquad \mathcal N=\log a.
$$

No representa por sí sola autorrefuerzo con memoria; sirve para comprobar el núcleo cosmológico. Con \(a_i=1\), \(n=3+\xi\), las soluciones son

$$
\rho_I=\rho_{I i}a^{-n},
\tag{8.1}
$$

$$
\rho_D=a^{-3}\left[\rho_{D i}+b\rho_{I i}(1-a^{-\xi})\right],
\tag{8.2}
$$

$$
V=V_i+\frac{(1-b)\xi}{3+\xi}\rho_{I i}(1-a^{-n}),
\tag{8.3}
$$

$$
f=1-(1-f_i)a^{-\xi}.
\tag{8.4}
$$

**Demostración.** Dividir las ecuaciones por \(H\) transforma
\(\rho_I'=-(3+\xi)\rho_I\).
Después,
\((a^3\rho_D)'=b\xi\rho_{I i}a^{-\xi}\) y
\(V'=(1-b)\xi\rho_{I i}a^{-n}\). Integrar con las condiciones iniciales da las tres primeras expresiones. La cuarta sigue de \(f'=\xi(1-f)\). \(\square\)

Sea

$$
V_\infty=V_i+\frac{(1-b)\xi}{3+\xi}\rho_{I i}.
$$

La expansión exacta como función de \(a\) es

$$
3M_{\rm Pl}^2H^2
=V_\infty
+(\rho_{b i}+\rho_{D i}+b\rho_{I i})a^{-3}
+\frac{3(1-b)}{3+\xi}\rho_{I i}a^{-(3+\xi)}
+\rho_{r i}a^{-4}.
\tag{8.5}
$$

Se comprueba sumando las soluciones; los coeficientes son no negativos para datos iniciales físicos.

### 8.2. Positividad hacia el pasado

Para \(\xi>0\), \(b<1\), \(\rho_{I i}>0\), la expresión (8.3) resulta negativa suficientemente atrás si se prolonga sin modificación. La frontera \(V=0\) ocurre en

$$
\boxed{a_{\min}=
\left[1+\frac{(3+\xi)V_i}
{(1-b)\xi\rho_{I i}}\right]^{-1/(3+\xi)}.}
\tag{8.6}
$$

La rama con \(V\geq0\) exige \(a\geq a_{\min}\). Si además \(f_i\) se usa como fracción inicial, prolongar (8.4) hacia atrás exige
\(a\geq(1-f_i)^{1/\xi}\). Estos límites hacen explícito que una solución futura o tardía no constituye automáticamente una cosmología válida desde el universo temprano.

En un modelo global puede requerirse una activación tardía de \(\Gamma\) o una condición física distinta para el precursor. Tal modificación añade una hipótesis que debe fijarse antes del ajuste.

### 8.3. Solución temporal y acción de reloj reconstruida

En el subcaso \(b=0\), sin bariones, radiación ni \(D\), y con \(V_\infty>0\), defina

$$
H_\infty^2=\frac{V_\infty}{3M_{\rm Pl}^2},
\qquad y=\frac{nH_\infty}{2}(t-t_B).
$$

De (8.1)–(8.5):

$$
\rho_I=nM_{\rm Pl}^2(H^2-H_\infty^2),\qquad
\dot H=-\frac n2(H^2-H_\infty^2).
$$

Separar variables da

$$
\boxed{H=H_\infty\coth y,}
\qquad
\boxed{a^n=\frac{3\rho_{I i}}{nV_\infty}\sinh^2y,}
\tag{8.7}
$$

con \(t_i\) escogido de modo que \(a(t_i)=1\).

La función

$$
\boxed{V(T)=M_{\rm Pl}^2H_\infty^2
\left[3-\xi\,\operatorname{csch}^2
\left(\frac{nH_\infty}{2}(T-t_B)\right)\right]}
\tag{8.8}
$$

introducida en (4.1) reproduce esta trayectoria con \(T=t\) y
\(\lambda=nM_{\rm Pl}^2H_\infty^2\operatorname{csch}^2y\).

Para comprobar la transferencia,

$$
V_{,T}
=\xi nM_{\rm Pl}^2H_\infty^3
\operatorname{csch}^2y\,\coth y
=\xi H\lambda.
$$

Se ha exhibido una acción local covariante y una solución exacta. Su dominio físico es la parte con \(V\geq0\); \(t_B\) es un parámetro de la extensión matemática, no necesariamente el Big Bang físico de una historia completa.

### 8.4. Abundancias y coincidencia

Si \(f\to1\), (7.3) implica

$$
\rho_Da^3\longrightarrow \rho_{D i}+b\rho_{I i}.
$$

La abundancia depende del reparto y de las condiciones iniciales. Además, bajo el teorema 2,
\(\rho_D/V\to0\). El modelo no predice por sí mismo una razón tardía constante distinta de cero entre materia oscura y energía oscura. Por tanto, la coincidencia de sus abundancias en una época determinada permanece como problema de selección de parámetros, condiciones iniciales y momento de observación.

---

## 9. Una prueba cosmográfica independiente de la forma de la memoria

### 9.1. Reconstrucción geométrica del vacío

Manténganse la planitud, polvo, radiación conservada y vacío exacto. De (2.4):

$$
\rho_m=-2M_{\rm Pl}^2\dot H-\frac43\rho_r,
$$

$$
\boxed{V=M_{\rm Pl}^2(3H^2+2\dot H)+\frac13\rho_r.}
\tag{9.1}
$$

No hace falta conocer el reparto entre \(I,D,b\) para reconstruir el polvo total bajo estas hipótesis. Derivando y usando \(\dot\rho_r=-4H\rho_r\):

$$
\boxed{Q_V=2M_{\rm Pl}^2(\ddot H+3H\dot H)
-\frac43H\rho_r.}
\tag{9.2}
$$

Estas expresiones son reconstrucciones condicionales. Si se permite curvatura, presión adicional, gravedad modificada o radiación interactuante, cambian.

### 9.2. Teorema 3: desigualdad para la tercera derivada

Defina

$$
q_{\rm dec}=-\frac{\ddot a}{aH^2},\qquad
j=\frac{\dddot a}{aH^3},\qquad
\Omega_r=\frac{\rho_r}{3M_{\rm Pl}^2H^2}.
$$

Entonces el modelo satisface

$$
\boxed{j=1+2\Omega_r+\frac{Q_V}{2M_{\rm Pl}^2H^3}.}
\tag{9.3}
$$

En particular, para absorción hacia el vacío,

$$
\boxed{Q_V\geq0\quad\Longrightarrow\quad j\geq1+2\Omega_r.}
\tag{9.4}
$$

**Demostración.** Derivando \(\dot a=aH\) tres veces en total se obtiene

$$
\dddot a=a(H^3+3H\dot H+\ddot H),
\qquad
j=1+\frac{3\dot H}{H^2}+\frac{\ddot H}{H^3}.
$$

Sustituir esta última identidad en (9.2) da
\(Q_V=2M_{\rm Pl}^2H^3(j-1)-4H\rho_r/3\).
Dividir por \(2M_{\rm Pl}^2H^3\) y usar la definición de \(\Omega_r\) prueba (9.3) y (9.4). \(\square\)

La desigualdad no depende de \(\alpha,\beta,\tau_M\), sino del signo del intercambio y de las ecuaciones de estado. A bajo corrimiento al rojo, cuando la radiación es despreciable, se aproxima a \(j\geq1\). Sin intercambio se recupera \(j=1+2\Omega_r\), incluyendo la pequeña contribución de radiación.

### 9.3. Cómo se comprobaría

Como \(1+z=a_{\rm hoy}/a\),

$$
\dot H=-(1+z)H\frac{dH}{dz},\qquad
q_{\rm dec}=-1+(1+z)\frac{H_{,z}}{H},
$$

$$
j=q_{\rm dec}(2q_{\rm dec}+1)
+(1+z)\frac{dq_{\rm dec}}{dz}.
\tag{9.5}
$$

Una reconstrucción de \(H(z)\) permitiría contrastar estas condiciones, junto con
\(\rho_m\geq0\) y \(V\geq0\) obtenidas de (9.1). Pero derivar datos ruidosos amplifica incertidumbres; es necesario propagar la covarianza y declarar las hipótesis de suavizado. No se ha realizado tal reconstrucción en este trabajo.

Si datos robustos exigieran \(j<1+2\Omega_r\) en una época donde valen las hipótesis, esa versión del modelo quedaría excluida, aunque el autorrefuerzo estocástico pudiera seguir existiendo como fenómeno en otro contexto.

### 9.4. Reconstrucción de la tasa en un caso reducido

Sin radiación y con un único sector de polvo que dona energía,

$$
\rho_I=-2M_{\rm Pl}^2\dot H,\qquad
\boxed{\Gamma=-3H-\frac{\ddot H}{\dot H},}
\tag{9.6}
$$

si \(\dot H<0\). Con productos de polvo adicionales, la geometría determina \(Q_V\), pero no separa de manera única \(\Gamma,\rho_I,b\). Las observaciones de estructura y las hipótesis microfísicas se vuelven necesarias para romper esa degeneración.

No se demuestra novedad histórica de estas identidades cosmográficas. Su función aquí es convertir el mecanismo propuesto en un criterio de contraste que no dependa de ajustar libremente una tasa para cada dato.

---

## 10. Perturbaciones: la restricción que un modelo de fondo no puede omitir

### 10.1. Integrabilidad de la transferencia de vacío

Supóngase que un vacío exacto recibe energía sin fuerza espacial en el marco \(u^\mu\):

$$
-\nabla^\mu V=Q_Vu^\mu.
\tag{10.1}
$$

Bajando el índice, el lado izquierdo es un gradiente. Por tanto,

$$
\boxed{\nabla_{[\mu}(Q_Vu_{\nu]})=0.}
\tag{10.2}
$$

Esta ecuación es una condición de integrabilidad adicional; una expresión escalar para \(Q_V\) no basta.

En la realización de reloj, \(u_\mu=-\partial_\mu T\). Entonces (10.2) equivale localmente a

$$
dQ_V\wedge dT=0,
$$

es decir, \(Q_V\) depende solo de \(T\) en regiones donde el reloj es regular. También \(V=V(T)\). En hipersuperficies comóviles de \(T\) constante,

$$
\delta V_{\rm com}=0,\qquad \delta Q_{V,\rm com}=0.
\tag{10.3}
$$

En cambio, promover directamente el cierre de fondo a

$$
Q_V(x)=(1-b)\Gamma(f(x),M(x))\rho_I(x)
$$

produce en general gradientes espaciales de \(Q_V\). No puede imponerse simultáneamente con un reloj geodésico arbitrario y un vacío exacto sin satisfacer (10.2).

Para una extensión espacial hay que escoger y derivar una de estas posibilidades:

- imponer restricciones que hagan compatible la tasa local con (10.2);
- admitir transferencia de momento y la aceleración correspondiente del donante;
- reemplazar el vacío exacto por un sector con dinámica y presión propias;
- construir una acción abierta completa cuyo tensor y ecuaciones determinen la transferencia.

Son teorías diferentes. El modelo homogéneo es común a varias, pero sus perturbaciones no lo son. La ausencia de una cuatro-velocidad propia de un vacío exacto y la necesidad de especificar su interacción están tratadas en la formulación covariante de vacío inhomogéneo. [Wands, De-Santiago y Wang](https://arxiv.org/abs/1203.6776).

### 10.2. Proposición 7: crecimiento en la realización geodésica

Para un único polvo interactuante y vacío \(V(T)\), sin radiación ni bariones separados, considere perturbaciones escalares lineales en gauge síncrono comóvil. Defina

$$
\delta=\delta\rho_I/\bar\rho_I,\qquad
\vartheta=\delta\Theta,\qquad
\gamma_c=\bar Q_V/\bar\rho_I.
$$

Entonces

$$
\dot\delta=-\vartheta+\gamma_c\delta,
\qquad
\dot\vartheta+2H\vartheta=-\frac{\bar\rho_I}{2M_{\rm Pl}^2}\delta,
\tag{10.4}
$$

y

$$
\boxed{
\ddot\delta+(2H-\gamma_c)\dot\delta
-\left(\frac{\bar\rho_I}{2M_{\rm Pl}^2}
+\dot\gamma_c+2H\gamma_c\right)\delta=0.
}
\tag{10.5}
$$

**Demostración.** La conservación local del polvo es
\(D\rho_I+\Theta\rho_I=-Q_V(T)\).
Escriba \(\rho_I=\bar\rho_I(1+\delta)\),
\(\Theta=3H+\vartheta\), reste el fondo y use \(\delta Q_{V,\rm com}=0\):

$$
\bar\rho_I\dot\delta-\bar Q_V\delta+\bar\rho_I\vartheta=0.
$$

Esto da la primera ecuación de (10.4). La linealización de Raychaudhuri, con movimiento geodésico, cizalla y vorticidad que contribuyen cuadráticamente, y \(\delta V_{\rm com}=0\), da la segunda. Despeje
\(\vartheta=-\dot\delta+\gamma_c\delta\), derive y sustituya; se obtiene (10.5). \(\square\)

Cuando \(\gamma_c=0\), se recupera la ecuación habitual del polvo:
\(\ddot\delta+2H\dot\delta-4\pi G\bar\rho_I\delta=0\).
La interacción no consiste universalmente en sumar \(+\Gamma\) a la fricción. El signo y los otros términos dependen del cierre de perturbaciones.

La ecuación describe este sector y este gauge, con las restricciones gravitatorias y condiciones iniciales consistentes. No es una prueba de estabilidad no lineal ni un cálculo completo del CMB. En particular, el polvo sin presión puede desarrollar cáusticas.

### 10.3. Por qué el término de pérdida puede cancelarse

Como control algebraico, una ecuación de continuidad con pérdida local proporcional a la densidad da, a primer orden,

$$
\dot\delta=-\vartheta+\frac{\bar Q}{\bar\rho}\delta
-\frac{\delta Q}{\bar\rho}.
$$

Si \(\delta Q=\bar\Gamma\bar\rho\,\delta+\bar\rho\,\delta\Gamma\), los términos proporcionales a \(\bar\Gamma\delta\) se cancelan:
\(\dot\delta=-\vartheta-\delta\Gamma\).

Este ejemplo muestra por qué no puede deducirse una ecuación de crecimiento mirando solo la pérdida de densidad de fondo. Para un receptor que sea vacío exacto, además hay que satisfacer la condición covariante (10.2); el ejemplo de continuidad no la reemplaza.

### 10.4. Sonido, fantasmas y vacío exacto

Para un campo dinámico se estudian el coeficiente cinético y el gradiente en la acción cuadrática,

$$
S^{(2)}=\frac12\int d^4x\,a^3
\left[K\dot\chi^2-\frac{G_s}{a^2}(\nabla\chi)^2-\cdots\right].
$$

En un sector desacoplado regular, \(K>0\) evita un fantasma y
\(c_s^2=G_s/K\geq0\) evita una inestabilidad de gradiente. La causalidad exige estudiar las características del sistema completo.

Un vacío exacto no posee un marco de reposo único ni una velocidad de sonido material independiente. Su perturbación está determinada por la transferencia. Asignarle libremente \(c_s^2\), \(\delta V\) y \(\delta Q^\mu\) sobrecuenta la información.

---

## 11. Hidrodinámica relativista, Navier–Stokes y Reynolds

### 11.1. Proyecciones de la conservación

Defina

$$
\Delta^{\mu\nu}=g^{\mu\nu}+u^\mu u^\nu,\qquad
D=u^\mu\nabla_\mu,\qquad \Theta=\nabla_\mu u^\mu.
$$

Para un fluido perfecto,

$$
T^{\mu\nu}=\rho u^\mu u^\nu+p\Delta^{\mu\nu}.
$$

La contracción \(u_\nu\nabla_\mu T^{\mu\nu}=0\), usando
\(u_\nu\nabla_\mu u^\nu=0\), da

$$
D\rho+(\rho+p)\Theta=0.
$$

La proyección con \(\Delta^\alpha{}_\nu\) elimina la componente temporal y produce

$$
(\rho+p)Du^\alpha+\Delta^{\alpha\mu}\nabla_\mu p=0.
\tag{11.1}
$$

Einstein proporciona la conservación del tensor total; para obtener una ecuación de fluido particular se añade una descomposición de materia y relaciones constitutivas. La viscosidad no se determina a partir de \(G_{\mu\nu}\) por sí solo.

### 11.2. Signo correcto de la viscosidad

En el marco de Landau, sin flujo de calor separado,

$$
T^{\mu\nu}=\rho u^\mu u^\nu+(p+\Pi)\Delta^{\mu\nu}+\pi^{\mu\nu},
$$

con \(\pi^{\mu\nu}\) espacial, simétrico y sin traza. Tomamos

$$
\sigma_{\mu\nu}=
\Delta_\mu{}^\alpha\Delta_\nu{}^\beta
\left(\nabla_{(\alpha}u_{\beta)}-\frac13\Delta_{\alpha\beta}\Theta\right).
$$

Con esta definición y firma, el límite viscoso es

$$
\boxed{\Pi=-\zeta\Theta,\qquad \pi^{\mu\nu}=-2\eta\sigma^{\mu\nu},}
\quad \eta,\zeta\geq0.
\tag{11.2}
$$

El signo menos es material. En un flujo de cizalla produce difusión amortiguada, no crecimiento de gradientes.

Para un fluido sin cargas y en equilibrio termodinámico local,
\(\rho+p=Ts\), \(d\rho=Tds\). La proyección energética da

$$
T\nabla_\mu(su^\mu)=-\Pi\Theta-\pi^{\mu\nu}\sigma_{\mu\nu}
=\zeta\Theta^2+2\eta\sigma^{\mu\nu}\sigma_{\mu\nu}\geq0.
\tag{11.3}
$$

Esto comprueba simultáneamente el signo constitutivo y la producción de entropía en el régimen de validez.

### 11.3. Límite no relativista

Restaure \(c\), tome velocidades pequeñas, densidad de masa \(\rho_{\rm m}\), presión mucho menor que \(\rho_{\rm m}c^2\) y transporte lentamente variable. La conservación de masa y momento da

$$
\partial_t\rho_{\rm m}+\nabla\cdot(\rho_{\rm m}\mathbf v)=0,
$$

$$
\rho_{\rm m}(\partial_t+\mathbf v\cdot\nabla)\mathbf v
=-\nabla p+\eta\nabla^2\mathbf v
+\left(\zeta+\frac{\eta}{3}\right)\nabla(\nabla\cdot\mathbf v)
+\mathbf f_{\rm vol},
\tag{11.4}
$$

para coeficientes constantes. Si \(\nabla\cdot\mathbf v=0\) y \(\rho_{\rm m}\) es constante:

$$
\boxed{
\partial_t\mathbf v+(\mathbf v\cdot\nabla)\mathbf v
=-\frac{\nabla p}{\rho_{\rm m}}+\nu\nabla^2\mathbf v
+\frac{\mathbf f_{\rm vol}}{\rho_{\rm m}},
\quad \nu=\eta/\rho_{\rm m}.
}
\tag{11.5}
$$

Esta es Navier–Stokes incompresible. La fuerza por unidad de masa tiene dimensión de aceleración.

### 11.4. Reynolds y escalas adicionales

Con \(\mathbf x=L\hat{\mathbf x}\), \(t=(L/U)\hat t\),
\(\mathbf v=U\hat{\mathbf v}\) y \(p=\rho_{\rm m}U^2\hat p\), la ecuación tiene coeficiente viscoso
\(\nu/(UL)\). Por tanto,

$$
\boxed{\operatorname{Re}=\frac{UL}{\nu}=\frac{\rho_{\rm m}UL}{\eta}.}
\tag{11.6}
$$

Es la razón entre transporte inercial y difusión viscosa, o entre
\(L^2/\nu\) y \(L/U\). En unidades \(c=1\), una estimación relativista usa
\((\rho+p)UL/\eta\); con densidad de energía en SI aparece
\((\rho+p)UL/(\eta c^2)\).

Para el modelo de conversión también importan

$$
\operatorname{Da}=\Gamma L/U,\qquad
\operatorname{De}_M=\tau_MU/L,\qquad
\operatorname{Kn}=\ell_{\rm micro}/L.
$$

Una hidrodinámica local requiere una separación de escalas, usualmente
\(\operatorname{Kn}\ll1\). Un Reynolds grande no deriva cuantización, espín o materia oscura. El número de Reynolds es una clasificación dinámica, no una nueva ley fundamental.

### 11.5. Relajación y velocidad característica

En una realización simplificada de Müller–Israel–Stewart,

$$
\tau_\pi\Delta^{\mu\nu}{}_{\alpha\beta}D\pi^{\alpha\beta}
+\pi^{\mu\nu}=-2\eta\sigma^{\mu\nu}+\cdots,
\quad
\tau_\Pi D\Pi+\Pi=-\zeta\Theta+\cdots,
\tag{11.7}
$$

con tiempos positivos. Para una perturbación transversal \(v_y(t,x)\) en un fondo de entalpía \(h=\rho+p>0\):

$$
h\partial_tv_y+\partial_x\pi^{xy}=0,\qquad
\tau_\pi\partial_t\pi^{xy}+\pi^{xy}=-\eta\partial_xv_y.
$$

Eliminar \(\pi^{xy}\) produce

$$
\boxed{\tau_\pi\partial_t^2v_y+\partial_tv_y
-\frac{\eta}{h}\partial_x^2v_y=0.}
\tag{11.8}
$$

El modo principal tiene velocidad \(v_T^2=\eta/(h\tau_\pi)\). Para ese canal, \(v_T\leq1\) exige \(\tau_\pi\geq\eta/h\). En el límite \(\tau_\pi\to0\), se recupera una ecuación difusiva con propagador de soporte espacial instantáneamente extendido.

Esta comprobación de un canal no prueba causalidad del sistema completo. Los sectores longitudinales, el estado termodinámico y los acoplamientos introducen condiciones adicionales.

Tampoco es correcto afirmar que toda hidrodinámica relativista de primer orden sea acausal. Las formulaciones tradicionales de Eckart/Landau tienen ese problema, mientras que existen teorías de primer orden con elección de marco apropiada y resultados de causalidad e hiperbolicidad. [Bemfica, Disconzi y Noronha](https://arxiv.org/abs/2009.11388). Las construcciones de Schwinger–Keldysh permiten organizar ruido y disipación con restricciones adicionales. [Jain y Kovtun](https://arxiv.org/abs/2309.00511).

### 11.6. Transporte de absorción: alcance de un cierre causal

En un parche plano, un cierre de Cattaneo puede escribirse

$$
\partial_tf+\nabla\cdot\mathbf J=F(f),\qquad
\tau_f\partial_t\mathbf J+\mathbf J=-D_f\nabla f.
$$

Eliminando \(\mathbf J\):

$$
\tau_f\partial_t^2f+\big(1-\tau_fF'(f)\big)\partial_tf
=D_f\nabla^2f+F(f).
\tag{11.9}
$$

La velocidad principal es \(\sqrt{D_f/\tau_f}\). Pero una ecuación hiperbólica de este tipo no hereda automáticamente el principio del máximo de una reacción–difusión parabólica. No se ha probado que conserve \(0\leq f\leq1\) para todos los datos de \(f,\mathbf J\). Los teoremas de intervalo de las secciones 5–7 se refieren a la cadena y al sistema homogéneo, no a cualquier extensión espacial.

---

## 12. Mecánica cuántica e hidrodinámica: equivalencias exactas y datos que faltan

### 12.1. Derivación de Madelung

Partimos de una ecuación de Schrödinger ya postulada:

$$
i\hbar\partial_t\psi=
-\frac{\hbar^2}{2m}\nabla^2\psi+W\psi.
$$

En un dominio donde \(\psi\neq0\), escribimos
\(\psi=\sqrt n\,e^{iS/\hbar}\). Las derivadas son

$$
\partial_t\psi=e^{iS/\hbar}
\left(\frac{\dot n}{2\sqrt n}+\frac{i}{\hbar}\sqrt n\,\dot S\right),
$$

$$
\nabla^2\psi=e^{iS/\hbar}\left[
\nabla^2\sqrt n+\frac{2i}{\hbar}\nabla\sqrt n\cdot\nabla S
+\frac{i}{\hbar}\sqrt n\,\nabla^2S
-\frac{\sqrt n}{\hbar^2}|\nabla S|^2\right].
$$

Separando las partes imaginaria y real:

$$
\boxed{\partial_tn+\nabla\cdot\left(n\frac{\nabla S}{m}\right)=0,}
\tag{12.1}
$$

$$
\boxed{\partial_tS+\frac{|\nabla S|^2}{2m}+W+U_Q=0,}
\qquad
\boxed{U_Q=-\frac{\hbar^2}{2m}\frac{\nabla^2\sqrt n}{\sqrt n}.}
\tag{12.2}
$$

Si \(\mathbf v=\nabla S/m\), la identidad
\(\nabla(v^2/2)=(\mathbf v\cdot\nabla)\mathbf v+
\mathbf v\times(\nabla\times\mathbf v)\)
y la irrotacionalidad local producen

$$
m(\partial_t+\mathbf v\cdot\nabla)\mathbf v=-\nabla(W+U_Q).
\tag{12.3}
$$

Se trata de una reescritura exacta local. No hay término viscoso en esta ecuación y la evolución original conserva la norma y es reversible para un Hamiltoniano hermítico.

### 12.2. Formulación variacional de la presión cuántica

Las ecuaciones (12.1)–(12.2) también siguen de

$$
S_{\rm Mad}=\int dt\,d^3x\left[
-n\left(\partial_tS+\frac{|\nabla S|^2}{2m}+W\right)
-\frac{\hbar^2}{8m}\frac{|\nabla n|^2}{n}\right].
\tag{12.4}
$$

Variar \(S\) e integrar por partes da continuidad. Para comprobar la variación en \(n\), sea

$$
E_Q=\frac{\hbar^2}{8m}\int\frac{|\nabla n|^2}{n}\,d^3x.
$$

Entonces

$$
\frac{\delta E_Q}{\delta n}
=\frac{\hbar^2}{8m}
\left(-2\frac{\nabla^2n}{n}+\frac{|\nabla n|^2}{n^2}\right)
=-\frac{\hbar^2}{2m}\frac{\nabla^2\sqrt n}{\sqrt n}=U_Q.
$$

Esto exhibe la energía de gradientes que debe reproducir una microteoría para obtener Madelung. La simetría por sí sola no fija el coeficiente \(\hbar^2/(8m)\).

### 12.3. Circulación y equivalencia global

La monovaluación de \(\psi\) exige, alrededor de un lazo cerrado sin cruzar nodos,

$$
\boxed{\oint\nabla S\cdot d\boldsymbol\ell=2\pi\hbar n_{\rm w},
\qquad n_{\rm w}\in\mathbb Z.}
\tag{12.5}
$$

Las ecuaciones diferenciales locales no imponen por sí solas esa condición sobre todos los dominios.

Por ejemplo, en un anillo bidimensional sin el origen, tome
\(n=n_0>0\), \(S=\ell\theta-Et\) y
\(W(r)=E-\ell^2/(2mr^2)\).
Continuidad y Hamilton–Jacobi con \(U_Q=0\) se satisfacen para cualquier \(\ell\) real. Sin embargo,
\(\psi(\theta+2\pi)=\psi(\theta)\) exige \(\ell/\hbar\in\mathbb Z\).
Este contraejemplo local demuestra qué información topológica adicional se necesita.

En una métrica espacial estática se puede usar el laplaciano de Laplace–Beltrami. Si la métrica depende del tiempo, la conservación de norma debe escribirse con la medida \(\sqrt h\,d^3x\); no basta con cambiar únicamente el laplaciano.

### 12.4. Klein–Gordon y límite no relativista

Con firma \((-+++)\),

$$
\left(\Box-\frac{m^2c^2}{\hbar^2}\right)\Psi=0.
$$

Para \(\Psi=Ae^{iS/\hbar}\), \(A>0\), la misma separación da

$$
\boxed{\nabla_\mu(A^2\nabla^\mu S)=0,}
\qquad
\boxed{\nabla_\mu S\nabla^\mu S+m^2c^2
-\hbar^2\frac{\Box A}{A}=0.}
\tag{12.6}
$$

La corriente conservada de Klein–Gordon no es automáticamente una densidad de probabilidad positiva para toda solución. La interpretación relativista general requiere teoría cuántica de campos.

En Minkowski, poniendo
\(\Psi=e^{-imc^2t/\hbar}\psi\) se obtiene

$$
\frac{2im}{\hbar}\partial_t\psi+\nabla^2\psi
-\frac1{c^2}\partial_t^2\psi=0.
$$

Si \(|\partial_t^2\psi|/c^2\) es despreciable respecto de
\(|2m\partial_t\psi|/\hbar\), se recupera Schrödinger libre. Es un límite de bajas energías de una ecuación cuántica relativista, no una derivación de cuantización desde relatividad clásica.

### 12.5. Entrelazamiento, Born y gravedad cuántica

Para dos partículas genéricas, \(\psi=\psi(\mathbf x_1,\mathbf x_2)\) vive en un espacio de configuración de seis dimensiones. Una descripción de un fluido escalar local en el espacio físico tridimensional no representa automáticamente todos esos estados.

Una teoría de emergencia cuántica debe explicar la composición tensorial, superposición, entrelazamiento, probabilidades de medición y sus restricciones experimentales. Identificar \(n=|\psi|^2\) después de comenzar con Schrödinger adopta la estructura cuántica, no la deduce.

De igual forma, la ecuación semiclásica

$$
G_{\mu\nu}=M_{\rm Pl}^{-2}\langle\hat T_{\mu\nu}\rangle_{\rm ren}
$$

acopla un valor esperado cuántico a una métrica clásica. No cuantiza la métrica. Las fluctuaciones del tensor, la renormalización, las restricciones gravitatorias y los grados de libertad a energías altas siguen pendientes.

---

## 13. Electromagnetismo: qué deriva una fase y qué debe añadirse

### 13.1. Conexión gauge

Para un campo complejo \(\Psi\), supóngase la redundancia

$$
\Psi\mapsto e^{iq_*\alpha(x)}\Psi,\qquad
A_\mu\mapsto A_\mu+\partial_\mu\alpha.
$$

La derivada covariante \(\mathcal D_\mu=\nabla_\mu-iq_*A_\mu\)
satisface
\(\mathcal D_\mu\Psi\mapsto e^{iq_*\alpha}\mathcal D_\mu\Psi\).
El campo de curvatura gauge es

$$
F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu.
$$

Una acción mínima es

$$
S_{\rm EM}=\int\sqrt{-g}
\left[-\frac{Z_A}{4}F_{\mu\nu}F^{\mu\nu}
-Z_\Psi(\mathcal D_\mu\Psi)^*\mathcal D^\mu\Psi
-U(|\Psi|^2)\right]d^4x,
\quad Z_A,Z_\Psi>0.
\tag{13.1}
$$

Variar \(A_\nu\) produce

$$
\boxed{\nabla_\mu(Z_AF^{\mu\nu})=j^\nu,}
\quad
j^\nu=iq_*Z_\Psi\left[
\Psi^*\mathcal D^\nu\Psi-\Psi(\mathcal D^\nu\Psi)^*\right].
\tag{13.2}
$$

**Derivación.** El término cinético gauge varía como
\(-Z_AF^{\mu\nu}\nabla_\mu\delta A_\nu\), que tras integración por partes da
\(\nabla_\mu(Z_AF^{\mu\nu})\delta A_\nu\).
El término escalar produce \(-j^\nu\delta A_\nu\).
La variación arbitraria impone (13.2).
La identidad \(dF=0\) proporciona la otra mitad de Maxwell.

El signo de la carga asignada a una excitación depende de la convención de fase; las ecuaciones anteriores son internamente consistentes con \(\mathcal D=\nabla-iq_*A\).

Localidad, invariancia de Lorentz, simetría gauge y una expansión de bajas derivadas permiten un término de Maxwell. No obligan a que \(Z_A\) sea no nulo ni calculan su valor. La existencia de un campo gauge propagante sigue siendo un ingrediente que la microteoría debe generar.

### 13.2. Una fase pura no produce fotones

Si se define solamente

$$
A_\mu=q_*^{-1}\partial_\mu\theta
$$

en una región suave, entonces

$$
F_{\mu\nu}=q_*^{-1}
(\partial_\mu\partial_\nu\theta-\partial_\nu\partial_\mu\theta)=0.
\tag{13.3}
$$

La topología puede permitir holonomías no triviales y singularidades de fase, pero esa observación no crea por sí misma las dos polarizaciones propagantes de Maxwell. Hace falta una conexión con curvatura y dinámica independientes.

### 13.3. Flujo cuantizado no es carga eléctrica

Para \(\Psi=\sqrt n\,e^{i\theta}\), la combinación
\(\partial_\mu\theta-q_*A_\mu\) es gauge-invariante.
Si tiende a cero sobre un contorno lejano a un vórtice:

$$
q_*\oint A_i\,dx^i=\oint\partial_i\theta\,dx^i=2\pi N.
$$

Esto cuantiza el flujo magnético que atraviesa ese contorno, cuando se aplica Stokes. La carga eléctrica, en cambio, se obtiene de la integral de \(j^0\) o del flujo eléctrico de Gauss. Un vórtice puede portar flujo sin tener una carga eléctrica neta.

Por tanto, el enrollamiento no demuestra \(Q_{\rm electric}=Ne\), ni fija el valor de \(e\).

### 13.4. Condensado cargado y masa del fotón

Si el mismo campo cargado tiene \(\Psi=v/\sqrt2\) constante en gauge unitario, el término escalar de (13.1) contiene

$$
-\frac{Z_\Psi q_*^2v^2}{2}A_\mu A^\mu.
$$

Tras normalizar \(A_\mu^{\rm can}=\sqrt{Z_A}A_\mu\), corresponde a

$$
\boxed{m_A^2=\frac{Z_\Psi q_*^2v^2}{Z_A}.}
\tag{13.4}
$$

Así, un condensado que rompe precisamente ese \(U(1)\) no entrega automáticamente un fotón sin masa. Una realización electromagnética viable debe conservar el \(U(1)\) observado o mostrar cómo emerge otra combinación gauge sin masa.

### 13.5. Por qué la métrica de Einstein no basta por un cambio de variables

Alrededor de un fondo de Minkowski, la relatividad general de Einstein tiene dos modos gravitatorios físicos, de helicidades \(\pm2\). Maxwell tiene dos modos adicionales de helicidades \(\pm1\). Una transformación local invertible de los grados de libertad físicos de Einstein puro no aumenta su número.

Por tanto, un sistema con gravedad de Einstein y electromagnetismo independientes no se obtiene de Einstein puro simplemente renombrando componentes. Puede intentarse una teoría con grados microscópicos adicionales, geometría ampliada, variables no locales o un límite colectivo; en cada caso se debe exhibir el mapa y verificar sus restricciones.

También las ondas gravitatorias de alta frecuencia, tratadas como un gas isotrópico de modos sin masa, tienen presión media \(\rho/3\). Su tensor es proporcional a promedios de \(k_\mu k_\nu\), con \(k^2=0\), y la isotropía da tres presiones iguales. Por sí solas no producen el tensor \(p=-\rho\) requerido por el vacío. La transformación entre un régimen ondulatorio y otro de presión negativa necesita dinámica adicional.

---

## 14. Defectos localizados: una construcción topológica calculable

### 14.1. Proposición 8: obstrucción de escala para un escalar ordinario

En tres dimensiones, sea una energía estática

$$
E[\phi]=E_2+E_0,\qquad
E_2=\frac12\int|\nabla\phi|^2d^3x,\qquad
E_0=\int W(\phi)d^3x,
$$

con \(W\geq0\) tras restar el vacío y energías finitas. Para
\(\phi_\lambda(\mathbf x)=\phi(\lambda\mathbf x)\),

$$
E(\lambda)=\lambda^{-1}E_2+\lambda^{-3}E_0.
$$

Una configuración estacionaria no trivial exigiría
\(E'(1)=-E_2-3E_0=0\), imposible si \(E_2>0\).

**Demostración.** Cada gradiente introduce \(\lambda\), y el cambio de variables del volumen introduce \(\lambda^{-3}\). La condición estacionaria bajo esta variación admisible produce la contradicción. \(\square\)

Es el argumento de escala de Derrick en sus hipótesis elementales. No excluye objetos con dependencia temporal, carga conservada, campos gauge, términos adicionales o gravedad; sí impide declarar una partícula estable a partir de un único escalar estático canónico sin revisar esas hipótesis.

### 14.2. Energía con término de cuatro derivadas espaciales

Sea \(n^A(\mathbf x)\), \(A=1,\ldots,4\), un campo con \(n^An^A=1\) y valor constante en el infinito. El espacio compacto de configuraciones espaciales define mapas \(S^3\to S^3\).

Definimos la energía

$$
E=\int d^3x\left[
\frac{F_*^2}{2}\partial_i n^A\partial_i n^A
+\frac{\kappa_s}{4}W_{ij}^{AB}W_{ij}^{AB}\right],
$$

$$
W_{ij}^{AB}=\partial_i n^A\partial_j n^B
-\partial_j n^A\partial_i n^B,\qquad F_*>0,\quad\kappa_s>0.
\tag{14.1}
$$

\(F_*\) tiene dimensión de masa y \(\kappa_s\) es adimensional. El segundo término tiene la estructura estabilizadora de Skyrme. Bajo el escalamiento anterior, las contribuciones van como \(\lambda^{-1}\) y \(\lambda\), por lo que el argumento que favorecía colapso deja de aplicar.

### 14.3. Proposición 9: grado y energía exactos de una familia de prueba

Para \(R_s>0\), considérese

$$
n^a(\mathbf x)=\frac{2R_s x^a}{r^2+R_s^2},\quad a=1,2,3,
\qquad
n^4(\mathbf x)=\frac{r^2-R_s^2}{r^2+R_s^2}.
\tag{14.2}
$$

Con las orientaciones \(\epsilon^{123}=\epsilon_{1234}=1\), su grado es

$$
B=\frac1{12\pi^2}\int d^3x\,
\epsilon^{ijk}\epsilon_{ABCD}
n^A\partial_i n^B\partial_j n^C\partial_k n^D=1,
\tag{14.3}
$$

y su energía es

$$
\boxed{E(R_s)=6\pi^2\left(F_*^2R_s+\frac{\kappa_s}{R_s}\right).}
\tag{14.4}
$$

En esta familia,

$$
\boxed{R_{s,*}=\frac{\sqrt{\kappa_s}}{F_*},\qquad
E_{\rm trial,min}=12\pi^2F_*\sqrt{\kappa_s}.}
\tag{14.5}
$$

**Demostración.** La norma unitaria se verifica al sumar los cuatro cuadrados. Una diferenciación directa da la métrica inducida

$$
\partial_i n^A\partial_j n^A
=\frac{4R_s^2}{(r^2+R_s^2)^2}\delta_{ij}.
$$

Por tanto,

$$
\sum_{i,A}(\partial_i n^A)^2
=\frac{12R_s^2}{(r^2+R_s^2)^2},\qquad
\sum_{i,j,A,B}(W_{ij}^{AB})^2
=\frac{192R_s^4}{(r^2+R_s^2)^4}.
$$

El integrando del grado, incluyendo \(1/(12\pi^2)\) pero no \(d^3x\), es

$$
\mathcal B(r)=\frac{4R_s^3}{\pi^2(r^2+R_s^2)^3}.
$$

Use las integrales

$$
\int_0^\infty\frac{r^2\,dr}{(r^2+R_s^2)^2}=\frac{\pi}{4R_s},\quad
\int_0^\infty\frac{r^2\,dr}{(r^2+R_s^2)^3}=\frac{\pi}{16R_s^3},\quad
\int_0^\infty\frac{r^2\,dr}{(r^2+R_s^2)^4}=\frac{\pi}{32R_s^5}.
$$

Al multiplicar por \(4\pi r^2dr\) donde corresponde, se obtiene \(B=1\),
\(E_2=6\pi^2F_*^2R_s\) y \(E_4=6\pi^2\kappa_s/R_s\).
Finalmente,
\(E'=6\pi^2(F_*^2-\kappa_s/R_s^2)\) y
\(E''=12\pi^2\kappa_s/R_s^3>0\), lo que prueba (14.5). \(\square\)

Este es un resultado más concreto que la identificación verbal «partícula = vórtice»: existe una familia localizada, de energía finita, con un entero topológico y un tamaño preferido dentro de la familia.

**Límite exacto de la prueba.** La configuración de prueba no se ha demostrado solución de las ecuaciones de Euler–Lagrange completas. El mínimo respecto de \(R_s\) es estabilidad frente a esa variación, no positividad de todo el Hessiano funcional. Su energía da una cota superior al ínfimo del sector topológico, no una masa de partícula ya calculada. No se ha obtenido la masa del electrón ni una abundancia relicta.

### 14.4. Objeto puntual, cuerda y pared no son equivalentes

Un vórtice \(U(1)\) ordinario en tres dimensiones espaciales es de codimensión dos: típicamente una cuerda. La cancelación gauge puede hacer finita su energía por unidad de longitud, sin hacer finita la energía de una cuerda infinita.

Como ilustración macroscópica, supóngase una población comóvil congelada de defectos de dimensión espacial \(d\), energía proporcional a su extensión \(a^d\) y número comóvil conservado. Entonces \(\rho\propto a^{d-3}\). Comparar con continuidad da

$$
w=-d/3.
$$

| Objeto idealizado | \(d\) | \(w\) bajo estas hipótesis |
|---|---:|---:|
| Partículas lentas | 0 | 0 |
| Cuerdas congeladas | 1 | \(-1/3\) |
| Paredes congeladas | 2 | \(-2/3\) |
| Energía volumétrica constante | 3 | \(-1\) |

La tensión, las velocidades y la evolución de la red importan. Esta tabla no demuestra que una red real de paredes sea energía oscura viable; muestra que la localización y el modo de almacenar energía cambian la ecuación de estado.

### 14.5. Derivación del límite de materia fría

Para una población isotrópica de objetos de masa \(m_D\), con distribución \(\mathcal F(\mathbf p)\geq0\),

$$
\rho_D=\int d^3p\,E_{\mathbf p}\mathcal F(\mathbf p),\qquad
p_D=\frac13\int d^3p\,\frac{\mathbf p^2}{E_{\mathbf p}}\mathcal F(\mathbf p),
$$

$$
E_{\mathbf p}=\sqrt{m_D^2+\mathbf p^2}.
$$

Si \(|\mathbf p|\ll m_D\), expandir \(E_{\mathbf p}\) da

$$
\rho_D\simeq m_D n_D,\qquad
\frac{p_D}{\rho_D}\simeq\frac{\langle v^2\rangle}{3}\ll1.
\tag{14.6}
$$

Se ha derivado el límite sin presión bajo una condición cinemática. La formación por absorción puede producir objetos rápidos; por ello hay que calcular su distribución de momento, vida media, auto-interacciones y capacidad de agruparse gravitacionalmente.

### 14.6. Espín y neutrinos

La carga topológica \(B\) no es un operador de espín. Un mecanismo de cuantización tipo Finkelstein–Rubinstein requiere demostrar que el lazo de rotación de \(2\pi\) es no trivial en el espacio de configuraciones y escoger una representación adecuada de su grupo fundamental. Incluso disponer de un grupo \(\mathbb Z_2\) no identifica por sí solo ese lazo con la rotación física ni reproduce un fermión del Modelo Estándar.

Los neutrinos activos son excitaciones cuánticas propagantes con interacciones débiles y mezcla de sabores. Su baja interacción electromagnética no implica proximidad a un estado absorbente. Sus velocidades y el libre recorrido cosmológico afectan el crecimiento de estructura. [Lesgourgues y Pastor](https://arxiv.org/abs/1212.6154).

Una identificación geométrica tendría que reproducir, al menos, un sector espinorial covariante y una matriz de masas con mezcla. «Complejidad» y «capacidad de interacción» pueden ser variables heurísticas para organizar candidatos; sin operadores y acoplamientos definidos no son una explicación de las oscilaciones de neutrinos.

---

## 15. Absorción cuántica, memoria e irreversibilidad

### 15.1. Proposición 10: obstrucción unitaria en dimensión finita

Sea \(\mathcal H\) finito-dimensional, \(U(t)=e^{-iHt/\hbar}\) unitario y
\(\mathcal A\subset\mathcal H\) un subespacio que permanece dentro de sí para todo \(t\geq0\). Entonces no existe flujo unitario desde \(\mathcal A^\perp\) hacia \(\mathcal A\).

**Demostración.** \(U(t)\mathcal A\subseteq\mathcal A\), pero ambas tienen la misma dimensión, pues \(U\) es invertible. Por tanto,
\(U(t)\mathcal A=\mathcal A\). La unitaridad conserva ortogonalidad, de modo que
\(U(t)\mathcal A^\perp=\mathcal A^\perp\). En consecuencia, la probabilidad de ocupar \(\mathcal A\) no aumenta por transferencia desde su complemento. \(\square\)

Asimismo, dos estados ortogonales no pueden convertirse unitariamente en el mismo estado completo: su producto interno debe conservarse. La absorción de varios estados hacia una misma descripción exige información en un entorno, una proyección de observables o un límite no cubierto por estas hipótesis.

La proposición no excluye procesos efectivos irreversibles en sistemas abiertos ni límites de infinitos grados de libertad. Delimita qué se puede afirmar sobre un universo cerrado finito sin añadir un mecanismo.

### 15.2. Realización explícita de dos estados

En la base \(\{|I\rangle,|A\rangle\}\), sea

$$
L=\sqrt{\Gamma}\,|A\rangle\langle I|,
\qquad
\dot\varrho=L\varrho L^\dagger-\frac12\{L^\dagger L,\varrho\}.
\tag{15.1}
$$

Esta es una ecuación de tipo Lindblad con tasa constante no negativa. Conserva la traza y define un canal completamente positivo. [Lindblad](https://doi.org/10.1007/BF01608499).

Tomando elementos matriciales,

$$
\dot\varrho_{II}=-\Gamma\varrho_{II},\qquad
\dot\varrho_{AA}=\Gamma\varrho_{II},\qquad
\dot\varrho_{IA}=-\frac{\Gamma}{2}\varrho_{IA}.
$$

Como \(\varrho_{II}+\varrho_{AA}=1\), si \(f=\varrho_{AA}\),

$$
\boxed{\dot f=\Gamma(1-f).}
\tag{15.2}
$$

Esta ecuación se ha obtenido exactamente de un modelo cuántico abierto especificado. El estado \(|A\rangle\langle A|\) es estacionario y absorbente para la dinámica reducida.

### 15.3. Refuerzo sin postular una mecánica cuántica fundamental no lineal

Para \(N>1\) unidades, sea

$$
n_i=|A_i\rangle\langle A_i|,\qquad
\hat f_{\neg i}=\frac1{N-1}\sum_{j\neq i}n_j,
$$

$$
L_i=|A_i\rangle\langle I_i|
\sqrt{\Gamma_0e^{\alpha\hat f_{\neg i}}}.
\tag{15.3}
$$

En una región efectiva donde esta interacción sea una aproximación admisible, el generador global de Lindblad sigue siendo lineal en \(\varrho\). Como \(\hat f_{\neg i}\) conmuta con los operadores de la unidad \(i\),

$$
\frac{d}{dt}\langle n_i\rangle
=\left\langle(1-n_i)\Gamma_0e^{\alpha\hat f_{\neg i}}\right\rangle.
\tag{15.4}
$$

Los términos con \(L_j\), \(j\neq i\), no cambian \(n_i\), porque conmutan con él. En estados diagonales, (15.4) corresponde a nacimientos cuyas tasas dependen de otras ocupaciones. Una aproximación de campo medio produce la no linealidad macroscópica, sin hacer no lineal la evolución fundamental de la matriz de densidad conjunta.

El uso de todas las unidades del parche es una interacción de alcance efectivo finito, no una formulación relativista microscópica ya establecida. Una red causal debería especificar vecindarios y tiempos de propagación. La memoria puede surgir al incluir variables auxiliares y eliminarlas, pero aquí no se deriva un baño geométrico único que genere exactamente (6.6).

### 15.4. Entropía reducida: contraejemplo a una monotonía automática

Partiendo de \(|I\rangle\), la solución de (15.1) es diagonal con probabilidades
\(p_I=e^{-\Gamma t}\), \(p_A=1-e^{-\Gamma t}\).
La entropía de von Neumann es

$$
S_{\rm red}=-p_I\log p_I-(1-p_I)\log(1-p_I).
$$

Parte de cero, alcanza \(\log2\) cuando \(p_I=1/2\) y vuelve a cero al completarse la absorción. Por tanto, absorción no implica aumento monótono de entropía del subsistema.

La segunda ley debe aplicarse con el entorno y sus intercambios. Si cada salto libera una energía \(\Delta E\) a un baño, el balance energético debe incluir
\(\Delta E\,\Gamma p_I\). Ese baño no puede omitirse mientras se afirma conservación total.

En el modelo cosmológico, transferir energía al vacío es el postulado \(Q_V\geq0\); aún falta demostrar que una microdinámica conserve energía, produzca la entropía total adecuada y alimente ese tensor concreto.

### 15.5. Acción abierta y condiciones faltantes

Una representación efectiva esquemática de una ecuación estocástica
\(\mathcal E[f]=\mathcal N(f)\xi\) usa un campo de respuesta \(f_a\):

$$
S_{\rm resp}=\int d^4x\sqrt{-g}
\left[f_a\mathcal E[f]+\frac{i}{2}\mathcal N^2(f)f_a^2\right].
\tag{15.5}
$$

Con \(f\) adimensional y \([\mathcal E]=1\), el campo de respuesta puede normalizarse con dimensión tres, y entonces \([\mathcal N]=-1\) para un ruido blanco covariante de dimensión dos. Otras normalizaciones redistribuyen dimensiones entre campos y coeficientes.

La parte imaginaria no negativa es una condición útil, pero la expresión sola no constituye una acción cuántica de Schwinger–Keldysh completa. Hay que especificar medida, discretización del ruido multiplicativo, restricciones de unitaridad, campos auxiliares, cutoff y, si se afirma equilibrio, las relaciones termodinámicas correspondientes.

No es legítimo obtener un tensor gravitatorio completo variando solo el término de ruido esquemático mientras se omite el entorno que intercambia energía.

---

## 16. Verificación del resultado anunciado por OpenAI sobre Navier–Stokes

### 16.1. Qué se consultó y qué se encontró

El 8 de septiembre de 2026, OpenAI publicó un anuncio de solución para el problema de existencia y suavidad de Navier–Stokes, acompañado de un manuscrito y una formalización en Lean. El anuncio atribuye el resultado a un sistema interno y lo presenta como una construcción de singularidad con fuerza externa suave. [Anuncio oficial](https://openai.com/index/navier-stokes-solution/).

El teorema 1.1 del manuscrito *Finite time blowup for Navier–Stokes* declara, para toda viscosidad positiva, una fuerza suave de soporte compacto y una solución que parte del reposo, mantiene norma \(L^2\) acotada y desarrolla velocidad \(L^\infty\) no acotada al aproximarse a un tiempo finito. El texto identifica el resultado con la alternativa C y extiende la construcción a D. [Manuscrito de OpenAI, teorema 1.1](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf).

La revisión de este documento comprobó el anuncio, el enunciado principal y la descripción pública del repositorio. No reprodujo las 166 páginas de demostración ni ejecutó una auditoría independiente de los certificados Lean. [Repositorio oficial](https://github.com/openai/NavierStokesAndEuler).

La página del Clay Mathematics Institute seguía mostrando el problema como no resuelto al consultarla en esta fecha. Eso describe el estado visible de esa página; no refuta ni certifica el manuscrito recién anunciado. [Página del problema](https://www.claymath.org/millennium/navier-stokes-equation/).

### 16.2. Alcance de las alternativas oficiales

La formulación de Fefferman distingue cuatro alternativas:

| Alternativa | Dominio | Tipo de afirmación |
|---|---|---|
| A | \(\mathbb R^3\) | Regularidad global para datos admisibles y fuerza nula |
| B | Toro tridimensional | Regularidad global periódica con fuerza nula |
| C | \(\mathbb R^3\) | Existencia de datos y fuerza suave admisibles sin solución global suave de la clase requerida |
| D | Toro tridimensional | Ruptura global con datos y fuerza suave periódicos admisibles |

La formulación permite resolver el problema mediante una de las alternativas propuestas. Un resultado con fuerza externa no determina automáticamente el comportamiento de todos los datos sin fuerza. [Descripción oficial de Fefferman](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).

### 16.3. Identidad de energía que sí se deriva aquí

Sea \(\mathbf u\) una solución suave, incompresible, periódica o suficientemente decreciente, con presión normalizada por densidad:

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u
=-\nabla p+\nu\Delta\mathbf u+\mathbf f,\qquad \nabla\cdot\mathbf u=0.
$$

Multiplique escalarmente por \(\mathbf u\) e integre. El término convectivo es
\(\int\nabla\cdot(\mathbf u|\mathbf u|^2/2)\), que se anula por las condiciones de frontera. El término de presión también se convierte en una divergencia. Integrar por partes la viscosidad da

$$
\boxed{
\frac{d}{dt}\frac12\int|\mathbf u|^2\,d^3x
+\nu\int|\nabla\mathbf u|^2\,d^3x
=\int\mathbf u\cdot\mathbf f\,d^3x.
}
\tag{16.1}
$$

Controlar la energía integrada no equivale a controlar todos los valores puntuales. Para ilustrar únicamente ese hecho funcional, tome un campo suave no nulo \(\mathbf w\) de soporte compacto y

$$
\mathbf u_\lambda(\mathbf x)=\lambda\mathbf w(\lambda\mathbf x).
$$

En tres dimensiones,

$$
\|\mathbf u_\lambda\|_\infty=\lambda\|\mathbf w\|_\infty,\qquad
\|\mathbf u_\lambda\|_2^2=\lambda^{-1}\|\mathbf w\|_2^2.
$$

La primera diverge y la segunda tiende a cero. Esta familia no se presenta como solución de Navier–Stokes: demuestra que una cota \(L^2\) no implica por sí sola una cota \(L^\infty\).

### 16.4. Vorticidad y concentración

Tomar el rotacional de Navier–Stokes, usando incompresibilidad, da

$$
\partial_t\boldsymbol\omega+
(\mathbf u\cdot\nabla)\boldsymbol\omega
=(\boldsymbol\omega\cdot\nabla)\mathbf u
+\nu\Delta\boldsymbol\omega+\nabla\times\mathbf f,
\quad \boldsymbol\omega=\nabla\times\mathbf u.
\tag{16.2}
$$

El término \((\boldsymbol\omega\cdot\nabla)\mathbf u\) estira vórtices. Si
\(S_{ij}=(\partial_i u_j+\partial_j u_i)/2\), un cálculo análogo al anterior produce

$$
\frac12\frac{d}{dt}\|\boldsymbol\omega\|_2^2
=\int\omega_iS_{ij}\omega_j\,d^3x
-\nu\|\nabla\boldsymbol\omega\|_2^2
+\int\boldsymbol\omega\cdot(\nabla\times\mathbf f)\,d^3x.
$$

El primer término no tiene signo fijo. Esto explica por qué una identidad de disipación de energía no resuelve automáticamente el comportamiento de gradientes.

### 16.5. Consecuencia para la propuesta geométrica

Una singularidad de una ecuación de continuo indica que su solución sale de cierta clase de regularidad. No especifica qué grados microscópicos la reemplazan, ni convierte la región singular en un estado estable absorbente. El reemplazo podría involucrar dispersión, nueva física, cambio de fase u otro régimen.

El resultado anunciado motiva estudiar concentración y límites del continuo. No demuestra que los vórtices formen materia oscura, que la viscosidad produzca \(\hbar\), ni que se unifiquen gravedad y cuántica. Para usarlo en una microteoría geométrica habría que mostrar que sus ecuaciones y condiciones son las de ese sustrato y derivar qué ocurre después del límite de validez.

### 16.6. Tensión de Reynolds, mecanismo de Isaacson y autorrefuerzo

El interés estructural de la construcción de OpenAI para esta propuesta no está en la singularidad en sí, sino en el mecanismo que la sostiene. Conviene enunciarlo con precisión y separar lo que es una analogía exacta de lo que sería una conjetura.

**El mecanismo del manuscrito.** La singularidad no se impone con una fuerza infinita. Se construye un vórtice de fondo \((\mathbf u_B,p_B)\) cuyo residuo de momento sería singular por sí solo, y se le añade un tren de pulsos oscilatorios \(\mathbf w\), de media angular nula, cuyo flujo cuadrático promediado cancela la parte singular. Para un incremento de velocidad \(\mathbf w\) sin divergencia con incremento de presión \(\pi\), la identidad exacta del residuo es

$$
R(\mathbf u_B+\mathbf w,\,p_B+\pi)
=R(\mathbf u_B,p_B)
+\mathcal L_{\mathbf u_B}(\mathbf w,\pi)
+\nabla\!\cdot(\mathbf w\otimes\mathbf w).
\tag{16.3}
$$

El término lineal \(\mathcal L_{\mathbf u_B}\) describe la evolución de los pulsos en el fondo; el término cuadrático \(\nabla\!\cdot(\mathbf w\otimes\mathbf w)\) aporta la tensión que cancela la parte principal del residuo. La media angular de \(\mathbf w\) es cero, pero la de sus productos no lo es: es la **tensión de Reynolds** \(\langle w_i w_j\rangle\). Los pulsos crecen extrayendo energía del cizallamiento del fondo por inestabilidad centrífuga, y la viscosidad los amortigua después; una fuerza externa exponencialmente pequeña siembra cada pulso y el propio fondo suministra su crecimiento. Esa retroalimentación —semilla infinitesimal, amplificación por la estructura ya presente, saturación— es autorrefuerzo en un sentido dinámico y no meramente probabilístico.

**La correspondencia exacta.** El promedio de un producto cuadrático de oscilaciones rápidas que retroalimenta un fondo lento no es exclusivo de la hidrodinámica. En relatividad general es el mecanismo de Isaacson: para perturbaciones métricas de alta frecuencia \(h_{\mu\nu}\) sobre un fondo \(\bar g_{\mu\nu}\), el promedio de Brill–Hartle produce un tensor de energía-momento efectivo

$$
T^{\rm GW}_{\mu\nu}
=\frac{1}{32\pi G}
\big\langle\,\partial_\mu h_{\alpha\beta}\,\partial_\nu h^{\alpha\beta}\,\big\rangle,
\tag{16.4}
$$

que curva el fondo aunque cada modo tenga media nula. La estructura \(\langle\partial\phi\,\partial\phi\rangle\) de (16.4) es idéntica en forma a la tensión de Reynolds \(\langle w\,w\rangle\) de (16.3): en ambos casos la escala lenta hereda un tensor de segundo orden que las oscilaciones de primer orden no tienen individualmente. Esta correspondencia es una identidad de estructura entre dos promedios, no una identificación física entre un fluido viscoso y la métrica.

**Lo que esto añade al modelo y lo que no.** La sección 13.5 ya registró que un gas isótropo de ondas gravitacionales de alta frecuencia tiene, por (16.4) y \(k^2=0\), presión media \(\rho/3\), y que por sí solo no produce el tensor \(p=-\rho\) del vacío. La construcción de OpenAI aporta un dato complementario: el mismo tipo de promedio, cuando el fondo es un vórtice que se concentra, puede transportar momento de forma dirigida y sostener una estructura que de otro modo requeriría una fuente singular. Es decir, la tensión de segundo orden no está condenada a ser un baño isótropo; su anisotropía depende del fondo. Para la propuesta geométrica esto sugiere una vía concreta —anisotropía del tensor efectivo inducida por la estructura media— en lugar del salto injustificado «oscilaciones \(\Rightarrow\) presión negativa».

**Tres obstrucciones que la analogía no levanta.**

1. *Energía.* La singularidad de OpenAI se forma con energía del núcleo tendiendo a cero: en las escalas \(\ell_r\asymp\tau^{1/2}\), \(\ell_z\asymp\tau^{1/2-h}\), la energía cinética del núcleo es \(\asymp\tau^{1/2-3h}\to0\) con \(h<1/6\). El defecto localizado de la sección 14.3 tiene energía finita **positiva** \(E(R_s)=6\pi^2\!\left(F_*^2R_s+\kappa_s/R_s\right)\), con un tamaño preferido \(R_s=\sqrt{\kappa_s}/F_*\). Un objeto cuya energía colapsa a cero y un solitón de energía finita no nula no son el mismo objeto; identificarlos exigiría una construcción, no una metáfora.

2. *Diseño frente a emergencia.* En (16.3) la fuerza se **define** como el residuo de un campo construido a mano; la auto-organización está impuesta por elección de perfiles, no derivada de un principio variacional cerrado. La afirmación del §16.5 se mantiene: de aquí no sale \(\hbar\), ni las dos polarizaciones de Maxwell, ni una materia oscura.

3. *Conteo de grados de libertad.* La obstrucción del §13.5 sigue en pie. Einstein puro tiene dos modos de helicidad \(\pm2\); Maxwell añade dos de helicidad \(\pm1\). Un promedio de tipo (16.4) sobre modos gravitatorios reproduce un tensor efectivo, no una conexión \(U(1)\) con curvatura y dinámica propias. Por tanto la idea de «electromagnetismo como ondas gravitacionales complejas» no se obtiene por este camino: el promedio de Isaacson no incrementa el número de polarizaciones físicas, y la transformación entre un régimen ondulatorio de presión \(\rho/3\) y uno de presión \(-\rho\) requiere dinámica adicional que aquí no se ha exhibido.

**Enunciado condicional que sí se puede sostener.** Bajo las hipótesis del §1.2, si un sustrato admite excitaciones rápidas de media nula sobre una configuración media lenta, entonces —por la forma común de (16.3) y (16.4)— la configuración lenta hereda un tensor efectivo cuadrático en las excitaciones, cuya traza y anisotropía dependen del fondo. Esto es un resultado de estructura sobre promedios, del nivel «resultado condicional del modelo» en la tabla del §1.3. No es del nivel «conjetura física»: no afirma que ese tensor sea el del sector oscuro, ni que las excitaciones sean fotones. La distinción entre ambos niveles es exactamente la que este manuscrito se compromete a no borrar.

---

## 17. Verificación reproducible y experimentos sintéticos

### 17.1. Diseño del cálculo

Se integra (7.1) desde una época de referencia arbitraria \(t_i\). Las unidades son

$$
\tau=H_i(t-t_i),\quad E=H/H_i,\quad
\tilde\rho=\rho/(3M_{\rm Pl}^2H_i^2),\quad a_i=1.
$$

Las condiciones iniciales son

$$
(\tilde\rho_I,\tilde\rho_D,\tilde V,\tilde\rho_b,\tilde\rho_r)_i
=(0.9499,0,0,0.05,0.0001),\qquad f_i=M_i=0.
$$

La suma es uno y por Friedmann \(E_i=1\). Se escoge \(b=0.25\) y
\(\tau_MH_i=0.7\). Se comparan:

| Caso | \(\Gamma_0/H_i\) | \(\alpha\) | \(\beta\) |
|---|---:|---:|---:|
| Sin conversión | 0 | 0 | 0 |
| Conversión sin refuerzo | 0.3 | 0 | 0 |
| Conversión con refuerzo y memoria | 0.3 | 2 | 1 |

Estas condiciones no son una estimación de las abundancias actuales. No se usa una edad medida del universo ni se asigna un corrimiento al rojo a \(t_i\). Se comprueba la dinámica matemática desde una época elegida.

Se usa DOP853 con tolerancia relativa \(10^{-11}\), absoluta \(10^{-13}\), paso máximo \(0.025\) en \(\tau\), e interpolación densa. Se integra cada densidad y \(f\) como variables separadas para que las identidades (7.2)–(7.3) sean controles de la solución numérica, en lugar de imponerlas al construirla.

### 17.2. Evolución con memoria

| \(\tau\) | \(a\) | \(E\) | \(f\) | \(M\) | \(\tilde V\) | \(\Omega_V\) | \(q_{\rm dec}\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.500050 |
| 0.5 | 1.457946 | 0.592006 | 0.164496 | 0.045570 | 0.065614 | 0.187217 | 0.219207 |
| 1 | 1.884397 | 0.455629 | 0.370943 | 0.163019 | 0.097653 | 0.470396 | -0.205575 |
| 2 | 2.830943 | 0.380693 | 0.876645 | 0.562611 | 0.128381 | 0.885833 | -0.828744 |
| 4 | 5.926489 | 0.364310 | 0.999995 | 0.970926 | 0.131341 | 0.989594 | -0.984390 |
| 8 | 25.299738 | 0.362434 | \(\simeq1\) | 0.999904 | 0.131341 | 0.999865 | -0.999797 |
| 12 | 107.819131 | 0.362410 | \(\simeq1\) | 1.000000 | 0.131341 | 0.999998 | -0.999997 |

Los valores próximos a uno se redondean; no representan absorción completa en tiempo finito de la ecuación determinista.

En esta solución \(f\) y \(V\) aumentan, \(H\) disminuye y la expansión pasa a acelerar. A \(\tau=2\), por ejemplo, \(f\simeq0.877\) y \(\Omega_V\simeq0.886\) son cercanos por casualidad; en otras filas difieren ampliamente. No deben identificarse.

### 17.3. Comparación y límites de la inferencia

| Caso | Inicio de aceleración \(\tau_{\rm acc}\) | \(\tilde V(12)\) | \(E(12)\) |
|---|---:|---:|---:|
| Sin conversión | No ocurre en este modelo con \(V_i=0\) | 0 | 0.052631 |
| Sin refuerzo | 0.8856069613 | 0.0931006162 | 0.3051261722 |
| Con refuerzo y memoria | 0.7654081194 | 0.1313407963 | 0.3624100242 |

La memoria y el refuerzo elegidos adelantan la aceleración y producen mayor vacío final aproximado que el control de tasa constante. El control sin refuerzo también acelera: el ingrediente que permite acelerar es el producto con presión negativa y su dominancia, no la memoria por sí sola.

La comparación combina refuerzo instantáneo y memoria, pues cambian \(\alpha\) y \(\beta\). Para separar sus efectos causales se necesitaría otra corrida con \(\alpha=2,\beta=0\), además de un diseño de comparación que explicite qué tasa integrada o inicial se mantiene fija. No se atribuye todo el efecto observado exclusivamente a \(\beta\).

### 17.4. Controles realizados

| Control | Resultado del cálculo |
|---|---|
| Contracciones de la cuatro-forma | Las 16 componentes del tensor coinciden exactamente usando aritmética racional |
| Generador adjunto de absorción de dos estados | Identidad \(\mathcal L^\dagger n=1-n\) exacta para \(\Gamma=1\) |
| Solución analítica con \(\Gamma=\xi H\) | Máximo error absoluto entre las cuatro variables: \(9.44\times10^{-15}\) |
| Energías y grado del perfil topológico | Error máximo de cuadratura: \(1.42\times10^{-14}\) |
| Supervivencia comóvil en el caso con memoria | Máximo error absoluto: \(6.45\times10^{-14}\) |
| Producto localizado comóvil en el caso con memoria | Máximo error absoluto: \(4.05\times10^{-15}\) |
| Continuidad total evaluada sobre el sistema | Residuo máximo: \(4.44\times10^{-16}\) |
| Identidad cosmográfica de \(j\) | Discrepancia máxima: \(1.34\times10^{-15}\) |
| Refinamiento de tolerancias en el caso con memoria | Cambio máximo entre estados muestreados: \(1.06\times10^{-13}\) |

El benchmark analítico usa \(\xi=0.35\), \(b=0.25\),
\((\rho_I,\rho_D,V,f)_i=(0.8,0,0.2,0.07)\) en unidades arbitrarias y
\(\log a\in[0,2]\). El perfil topológico se verifica con
\(R_s=1.7,F_*=0.9,\kappa_s=0.6\), también en unidades arbitrarias.

Las cotas de error son resultados de precisión finita para esos ensayos. No son cotas intervalares certificadas ni una demostración numérica uniforme sobre todos los parámetros. Los residuos de continuidad y de \(j\) comprueban coherencia algebraica del código; no aportan evidencia independiente de una teoría física.

La corrida refinada usa tolerancia relativa \(10^{-13}\). El cruce de aceleración cambia en aproximadamente \(2.3\times10^{-16}\) en ese control, cifra comparable al redondeo de máquina, que no debe interpretarse como precisión física.

El código completo del apéndice E incluye las versiones de NumPy y SciPy utilizadas al ejecutarlo y regenera las tablas en formato JSON.

---

## 18. Programa de investigación y conclusión científica

### 18.1. Qué contrastar con observaciones

Planck 2018 ofrece un conjunto de referencia bien definido para una cosmología plana de seis parámetros y sus extensiones. DESI DR2 publicó medidas BAO y restricciones cosmológicas, incluidas comparaciones de energía oscura evolutiva al combinar conjuntos de datos. Se citan estas publicaciones identificadas, sin presentar este manuscrito como una revisión exhaustiva de todos los resultados disponibles en septiembre de 2026. Ninguna de ellas constituye evidencia específica para absorción geométrica. [Planck 2018 VI](https://arxiv.org/abs/1807.06209), [DESI DR2 II](https://arxiv.org/abs/2503.14738).

Un análisis del modelo debería usar conjuntamente expansión y perturbaciones. Para geometría plana, las distancias básicas son

$$
D_M(z)=c\int_0^z\frac{dz'}{H(z')},\qquad
D_L(z)=(1+z)D_M(z),\qquad
D_A(z)=\frac{D_M(z)}{1+z}.
$$

BAO exige además una calibración consistente de la escala sonora y del universo temprano. Supernovas requieren parámetros de calibración y covarianzas. El CMB y la estructura requieren la evolución de perturbaciones y condiciones iniciales, no solo estas integrales.

Para un vector de datos \(\mathbf d\), predicción \(\mathbf m(\theta)\) y covarianza \(C\), una contribución gaussiana sería

$$
-2\log\mathcal L=
(\mathbf d-\mathbf m)^TC^{-1}(\mathbf d-\mathbf m)+{\rm constante},
$$

cuando la aproximación gaussiana y la covarianza usada sean adecuadas. No se puede reemplazar esa evaluación por semejanza visual de curvas o por elegir parámetros que recuerden fracciones cosmológicas conocidas.

### 18.2. Preguntas que debe resolver una microteoría

| Pregunta | Cálculo requerido | Estado aquí |
|---|---|---|
| ¿Qué es el sustrato? | Variables, espacio de estados, observables y dinámica | No especificado microscópicamente |
| ¿Cómo emerge la métrica? | Mapa colectivo y límite de Einstein–Hilbert | Einstein se adopta |
| ¿Por qué existe absorción? | Eliminación de un entorno y escala de retorno | Realización cuántica abierta de ejemplo |
| ¿Por qué \(\Gamma\) aumenta? | Barrera o generador dependiente del estado derivado | Ley efectiva propuesta |
| ¿Por qué el producto tiene \(p=-\rho\)? | Tensor derivado del sector microscópico | Ejemplos de cuatro-forma y reloj |
| ¿Cómo se forman objetos fríos? | Solución, distribución de momento y tasa de producción | Perfil topológico de prueba y límite cinético |
| ¿Cuál es el reparto \(b\)? | Probabilidades y energías de cada canal | Parámetro libre |
| ¿Cómo nace el electromagnetismo? | Conexión con curvatura, dos modos y acoplamiento | Sector \(U(1)\) adicional |
| ¿Cómo aparecen fermiones? | Cuantización y representaciones físicas | Pendiente |
| ¿Qué fija \(V_\infty\)? | Escalas microscópicas y correcciones cuánticas | Depende de datos y transferencia |

El valor absoluto de la energía de vacío sigue sin explicación. Una contribución positiva de cuatro-forma o de conversión no elimina automáticamente otras contribuciones ni garantiza estabilidad radiativa de una densidad pequeña.

### 18.3. Condiciones de rechazo de una realización concreta

Una versión especificada del modelo debe abandonarse o revisarse si viola sus propias restricciones, predice densidades inadmisibles en su dominio, no admite un tensor conservado, genera una inestabilidad física incompatible con el régimen de uso o no puede describir conjuntamente los datos con sus parámetros fijados.

La desigualdad (9.4), la positividad de (9.1), la condición de integrabilidad (10.2) y la ausencia de una fase materiada prolongada en ciertas elecciones de tasa son pruebas concretas. Deben aplicarse a la realización elegida, sin cambiar de hipótesis después de observar cada discrepancia.

Tener muchos parámetros o requerir ajuste fino no es, por sí solo, una contradicción matemática ni una falsación empírica. Sí debilita el poder explicativo y exige una comparación estadística que tenga en cuenta la complejidad.

### 18.4. Secuencia de trabajo técnicamente justificada

1. Fijar una realización covariante única, incluyendo qué variables son fundamentales y cuáles son promedios.
2. Derivar de esa realización el tensor total, las transferencias y las perturbaciones; comprobar integrabilidad.
3. Estudiar el problema de valores iniciales, restricciones, velocidades características y regiones de validez.
4. Determinar una historia temprana con densidades positivas y una era de formación de estructura.
5. Ajustar expansión y crecimiento con la misma parametrización y publicar el código y las condiciones iniciales.
6. Calcular soluciones localizadas completas, sus modos de fluctuación y su producción.
7. Intentar después la derivación microscópica de campos, cuantización y espectro de partículas.

Esta secuencia evita que una colección de analogías compatibles a nivel verbal sea presentada como una única teoría dinámica antes de cerrar sus ecuaciones.

### 18.5. Conclusión

La hipótesis inicial admite un núcleo matemático preciso: un proceso de conversión con memoria puede alimentar sectores oscuros efectivos, y la relatividad general determina exactamente cuándo ese intercambio produce aceleración.

En el modelo estudiado se demuestra que la fracción convertida crece sin salir de su dominio, que el precursor y los productos satisfacen identidades de balance, que el vacío puede aumentar desde cero y que una rama física llega a un régimen de de Sitter con \(H\) acotado y decreciente. Se obtienen una solución analítica de referencia, una condición cosmográfica independiente de la forma de la memoria y una obstrucción covariante relevante para perturbaciones.

Las realizaciones de cuatro-forma, reloj restringido, absorción de Lindblad y textura topológica muestran piezas matemáticamente concretas que podrían orientar una construcción más amplia. Todavía no se han ensamblado como una microteoría única.

La afirmación científicamente sustentable de esta versión es: **existe un modelo efectivo de absorción reforzada con consecuencias cosmológicas exactas bajo hipótesis explícitas**. La identificación con el universo observado y la unificación de mecánica cuántica y relatividad general siguen siendo objetivos de investigación.

---

## Apéndice A. Dimensiones, normalizaciones y dominio

| Objeto | Dimensión de masa con \(c=\hbar=1\) | Observación |
|---|---:|---|
| \(x^\mu,t,T,\tau_M\) | -1 | \(T\) es el reloj restringido |
| \(a,f,M,b,\alpha,\beta,\xi\) | 0 | Fracciones y razones |
| \(H,\Gamma,F_*,m\) | 1 | Tasas y escalas de masa |
| \(M_{\rm Pl}\) | 1 | Masa de Planck reducida |
| \(\rho,p,V,\lambda\) de (4.1) | 4 | Densidades y multiplicador |
| \(Q,Q_V\) | 5 | Transferencia energética |
| \(\Psi,\phi,A_\mu,C_{\mu\nu\rho}\) canónicos | 1 | La acción fija la normalización |
| \(F_{\mu\nu},\mathcal H_{\mu\nu\rho\sigma},h\) de (3.1) | 2 | Intensidades de campo |
| \(Z_A,Z_\Psi,q_*,\kappa_s\) | 0 | Coeficientes de la realización escrita |
| \(\eta,\zeta\) | 3 | Viscosidades relativistas |
| \(D_f\) | -1 | Difusividad en \(c=1\) |
| \(\rho a^3\) | 4 | Densidad normalizada por expansión; no energía total sin volumen inicial |

La probabilidad de salto en una celda no es \(\Gamma\) sola, sino
\(\Gamma\,d\tau+o(d\tau)\). Una tasa de nucleación por volumen físico requiere multiplicación por un volumen apropiado para producir una intensidad por unidad.

La rama \(f_i=1\) se trata separadamente: si \(f\) cuenta las mismas unidades que el precursor, debe imponerse \(\rho_{I i}=0\). Entonces no hay nueva conversión de ese precursor. Los teoremas 1–2 se enuncian con \(f_i<1\) para que las identidades normalizadas sean aplicables.

Las expresiones hidrodinámicas locales requieren longitud de onda grande respecto de la microescala. Las expresiones cuánticas de fase requieren dominios sin nodos o una descripción por parches. Los resultados FLRW requieren homogeneidad e isotropía. Estos dominios distintos no se extienden automáticamente unos a otros.

---

## Apéndice B. Detalles de las integrales y del modelo adimensional

### B.1. Integrales radiales del perfil topológico

Para \(k>3/2\),

$$
I_k(R_s)=\int_0^\infty
\frac{r^2\,dr}{(r^2+R_s^2)^k}.
$$

Con \(u=r^2/R_s^2\),

$$
I_k(R_s)=\frac{R_s^{3-2k}}{2}
\int_0^\infty u^{1/2}(1+u)^{-k}\,du
=\frac{R_s^{3-2k}}2
\frac{\Gamma_{\rm E}(3/2)\Gamma_{\rm E}(k-3/2)}{\Gamma_{\rm E}(k)}.
$$

\(\Gamma_{\rm E}\) designa la función gamma de Euler, distinta de la tasa de absorción. Usando
\(\Gamma_{\rm E}(1/2)=\sqrt\pi\) y
\(\Gamma_{\rm E}(z+1)=z\Gamma_{\rm E}(z)\),
se recuperan los tres valores de la sección 14.

Para verificar la métrica inducida, sea \(D_r=r^2+R_s^2\):

$$
\partial_i n^a=\frac{2R_s\delta_{ia}}{D_r}
-\frac{4R_sx^a x_i}{D_r^2},\qquad
\partial_i n^4=\frac{4R_s^2x_i}{D_r^2}.
$$

Al multiplicar y sumar en \(A\), los términos proporcionales a
\(x_ix_j\) se cancelan, dejando \(4R_s^2\delta_{ij}/D_r^2\).
Si \(G_{ij}=\partial_i n^A\partial_j n^A\), entonces

$$
\sum_{ijAB}(W_{ij}^{AB})^2
=2\left[(\operatorname{tr}G)^2-\operatorname{tr}(G^2)\right].
$$

Con \(G=s^2I_3\), resulta \(12s^4\), que fija el factor de normalización usado en (14.4).

### B.2. Sistema integrado

Para la normalización de la sección 17, ponga
\(\ell=\log a\), \(g=\Gamma/H_i\) y
\(E^2=\tilde\rho_I+\tilde\rho_D+\tilde V+\tilde\rho_b+\tilde\rho_r\).
Una prima en este apéndice significa \(d/d\tau\):

$$
\begin{aligned}
\ell'&=E,\\
\tilde\rho_I'&=-3E\tilde\rho_I-g\tilde\rho_I,\\
\tilde\rho_D'&=-3E\tilde\rho_D+bg\tilde\rho_I,\\
\tilde V'&=(1-b)g\tilde\rho_I,\\
\tilde\rho_b'&=-3E\tilde\rho_b,\\
\tilde\rho_r'&=-4E\tilde\rho_r,\\
f'&=(1-f)g,\\
M'&=(f-M)/(\tau_MH_i),\\
g&=(\Gamma_0/H_i)e^{\alpha f+\beta M}.
\end{aligned}
$$

La raíz de Friedmann se recalcula a partir de las densidades. La aceleración se localiza por

$$
q_{\rm dec}
=\frac{\tilde\rho_I+\tilde\rho_D+\tilde\rho_b+2\tilde\rho_r-2\tilde V}
{2E^2}.
$$

Además,

$$
E'=-\frac32\left(\tilde\rho_I+\tilde\rho_D+\tilde\rho_b
+\frac43\tilde\rho_r\right),
$$

$$
j=1+\frac{3E'}{E^2}+\frac{E''}{E^3}
=1+\frac{2\tilde\rho_r}{E^2}+\frac{3\tilde V'}{2E^3}.
$$

Las dos formas de \(j\) son las comparadas en el código. Derivar \(E''\) a partir de las ecuaciones de densidad evita usar diferencias finitas ruidosas, pero convierte ese control en una comprobación algebraica del sistema, no en una validación independiente de la gravitación.

### B.3. Qué verifica un cálculo exacto

Las contracciones tensoriales del apéndice E usan una base ortonormal con
\(h=1\) y aritmética entera o racional. Su validez para \(h\) general sigue de homogeneidad cuadrática y para otras bases de tensorialidad, demostradas en el texto.

La identidad matricial de Lindblad se comprueba exactamente para la matriz de dos estados. El paso de muchas unidades a una ecuación cerrada de campo medio se demuestra por separado bajo hipótesis de concentración; no se valida reemplazando sin más operadores correlacionados por promedios.

En (15.3) la fracción excluye la propia unidad. Para una configuración con \(k\) unidades absorbidas y la unidad \(i\) activa, la tasa usa \(k/(N-1)\), mientras (5.1) usa \(k/N\). La diferencia es \(O(N^{-1})\) para tasas Lipschitz y no cambia el límite de campo medio; las cadenas finitas no son idénticas término a término.

---

## Apéndice C. Auditoría de la versión anterior

Esta revisión sustituye las formulaciones correspondientes del borrador 0.1. Las correcciones no son meros cambios de redacción:

| Punto auditado | Formulación de esta revisión |
|---|---|
| Fracción absorbida confundida con campo canónico o densidad | \(f\), \(\phi\) y \(V\) son objetos distintos; se deriva su relación solo cuando está especificada |
| Vacío exacto con campo canónico rodante | Se demuestra la obstrucción \(\rho_\phi+p_\phi=\dot\phi^2\) |
| Estabilidad desde una tasa positiva solo en el extremo | Se exige una cota a lo largo de la trayectoria o una hipótesis uniforme suficiente |
| Signo de cizalla con firma \((-+++)\) | Se usa \(\pi^{\mu\nu}=-2\eta\sigma^{\mu\nu}\) y se comprueba el calentamiento positivo |
| Toda hidrodinámica relativista de primer orden tratada como acausal | Se distingue el cierre tradicional de las formulaciones BDNK |
| Ruido de absorción escogido sin proceso subyacente | Se deriva el segundo momento del generador de saltos y se delimita la aproximación difusiva |
| Conexión de fase presentada como electromagnetismo ya emergente | Se distingue fase pura, curvatura gauge, dinámica de Maxwell y masa por condensación |
| Flujo topológico interpretado como carga eléctrica | Se separan flujo magnético y carga de Gauss |
| Crecimiento de perturbaciones con una fricción esquemática | Se deriva un cierre geodésico concreto y se impone integrabilidad del vacío |
| Estado absorbente considerado automáticamente entrópico | Se presenta un contraejemplo exacto de entropía reducida no monótona |
| Acumulación asociada a crecimiento ilimitado de \(H\) | Se prueban cotas y futuro de de Sitter bajo las hipótesis físicas |
| Defecto de tamaño preferido presentado como partícula estable completa | Se distingue familia de prueba, solución de campo y Hessiano funcional |
| Más parámetros o ajuste fino tratados como falsación | Se distinguen inconsistencia, incompatibilidad observacional y comparación estadística |

La prioridad de esta auditoría es que cada afirmación tenga una ecuación, una hipótesis y un dominio de validez identificables.

---

## Apéndice D. Referencias verificadas y función dentro del manuscrito

Las referencias siguientes fueron consultadas para comprobar antecedentes, enunciados o estado documental. Las demostraciones propias del texto no reproducen íntegramente estas publicaciones.

1. S. M. Carroll, *Lecture Notes on General Relativity* (1997). Convenciones, geometría y contexto de las ecuaciones gravitatorias. [arXiv:gr-qc/9712019](https://arxiv.org/abs/gr-qc/9712019).
2. D. Wands, J. De-Santiago y Y. Wang, *Inhomogeneous vacuum energy*, Classical and Quantum Gravity 29, 145017 (2012). Vacío interactuante y prescripción covariante de perturbaciones. [arXiv:1203.6776](https://arxiv.org/abs/1203.6776).
3. E. A. Lim, I. Sawicki y A. Vikman, *Dust of Dark Energy*, JCAP 2010(05), 012 (2010). Fluidos con multiplicadores y comportamiento conjunto de materia y energía oscura. [arXiv:1003.5751](https://arxiv.org/abs/1003.5751).
4. R. Bousso y J. Polchinski, *Quantization of Four-form Fluxes and Dynamical Neutralization of the Cosmological Constant*, JHEP 2000(06), 006 (2000). Antecedente del papel gravitatorio de flujos de cuatro-formas. [arXiv:hep-th/0004134](https://arxiv.org/abs/hep-th/0004134).
5. H. Hinrichsen, *Nonequilibrium Critical Phenomena and Phase Transitions into Absorbing States*, Advances in Physics 49 (2000). Contexto de procesos absorbentes; no justifica asumir criticidad en cualquier modelo. [arXiv:cond-mat/0001070](https://arxiv.org/abs/cond-mat/0001070).
6. F. S. Bemfica, M. M. Disconzi y J. Noronha, *First-Order General-Relativistic Viscous Fluid Dynamics*. Formulación de primer orden con causalidad e hiperbolicidad bajo condiciones especificadas. [arXiv:2009.11388](https://arxiv.org/abs/2009.11388).
7. A. Jain y P. Kovtun, *Schwinger–Keldysh effective field theory for stable and causal relativistic hydrodynamics*. Construcción efectiva de fluctuaciones y disipación. [arXiv:2309.00511](https://arxiv.org/abs/2309.00511).
8. G. Lindblad, *On the generators of quantum dynamical semigroups*, Communications in Mathematical Physics 48, 119–130 (1976). Generadores de dinámica cuántica completamente positiva. [Publicación original](https://doi.org/10.1007/BF01608499).
9. J. Lesgourgues y S. Pastor, *Neutrino mass from Cosmology*, Advances in High Energy Physics 2012, 608515 (2012). Propagación cosmológica y papel de los neutrinos. [arXiv:1212.6154](https://arxiv.org/abs/1212.6154).
10. Planck Collaboration, N. Aghanim et al., *Planck 2018 results. VI. Cosmological parameters*, Astronomy & Astrophysics 641, A6 (2020). Referencia observacional de cosmología y extensiones. [arXiv:1807.06209](https://arxiv.org/abs/1807.06209).
11. DESI Collaboration, M. Abdul-Karim et al., *DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints* (2025). Medidas BAO y restricciones cosmológicas. [arXiv:2503.14738](https://arxiv.org/abs/2503.14738).
12. C. L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*. Enunciado oficial del problema del Milenio y sus cuatro alternativas. [Clay Mathematics Institute](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).
13. OpenAI, *On the Navier–Stokes Millennium Prize Problem*, 8 de septiembre de 2026. Anuncio del resultado y de su alcance. [Fuente oficial](https://openai.com/index/navier-stokes-solution/).
14. OpenAI, *Finite time blowup for Navier–Stokes* (2026). Se comprobaron el teorema 1.1 y el alcance declarado; no se certificó aquí la prueba completa. [Manuscrito](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf).
15. OpenAI, repositorio *NavierStokesAndEuler* (2026). Formalizaciones Lean publicadas por sus autores; no ejecutadas en esta revisión. [Repositorio](https://github.com/openai/NavierStokesAndEuler).
16. Clay Mathematics Institute, página *Navier-Stokes Equation*, consultada el 8 de septiembre de 2026. Estado visible de la clasificación institucional en esa fecha. [Página oficial](https://www.claymath.org/millennium/navier-stokes-equation/).

---

## Apéndice E. Código completo de reproducción

El siguiente programa es autocontenido salvo NumPy y SciPy. Puede copiarse como validar_modelo.py y ejecutarse con Python 3. La salida JSON contiene controles exactos de tamaño finito, errores de los benchmarks y valores de las tres trayectorias.

La ejecución documentada usó NumPy 2.3.5 y SciPy 1.17.0. Las últimas cifras pueden variar entre plataformas. No hay descarga de datos ni ajuste estadístico.


```python
"""Verificaciones del manuscrito v0.2. Datos sinteticos, sin ajuste observacional.

Requisitos: Python 3, numpy, scipy. Ejecutar: python validar_modelo.py
Salida: JSON con errores, controles exactos y tablas. No es una prueba formal.
"""
import json
import math
from fractions import Fraction as F
from itertools import permutations, product

import numpy as np
import scipy
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq


def parity(seq):
    return (-1) ** sum(seq[i] > seq[j] for i in range(len(seq))
                       for j in range(i + 1, len(seq)))


def exact_four_form():
    metric = [-1, 1, 1, 1]
    eps = {p: parity(p) for p in permutations(range(4))}
    get = lambda p: eps.get(tuple(p), 0)
    h2 = sum(get(p)**2 * math.prod(metric[i] for i in p)
             for p in product(range(4), repeat=4))
    checks = []
    for m, n in product(range(4), repeat=2):
        contraction = sum(get((m,) + abc) * get((n,) + abc)
                          * math.prod(metric[i] for i in abc)
                          for abc in product(range(4), repeat=3))
        g = metric[m] if m == n else 0
        stress = F(contraction, 6) - F(g * h2, 48)
        checks.append(stress == -F(g, 2))
    assert h2 == -24 and all(checks)
    return {"H_squared_for_h_1": h2, "stress_components_exact": sum(checks)}


def exact_lindblad():
    # Basis: |I>, |A>. Adjoint generator acting on n=|A><A|.
    L = np.array([[0, 0], [1, 0]], dtype=object)
    n = np.array([[0, 0], [0, 1]], dtype=object)
    K = L.T @ L
    adj = L.T @ n @ L - F(1, 2) * (K @ n + n @ K)
    assert np.array_equal(adj, np.eye(2, dtype=object) - n)
    return True


def constant_rate_benchmark():
    xi, branch = 0.35, 0.25
    f0, i0, d0, v0 = 0.07, 0.8, 0.0, 0.2
    def rhs(N, y):
        i, d, v, f = y
        return [-(3 + xi)*i, -3*d + branch*xi*i,
                (1 - branch)*xi*i, xi*(1 - f)]
    sol = solve_ivp(rhs, [0, 2], [i0, d0, v0, f0],
                    method="DOP853", rtol=1e-12, atol=1e-14,
                    dense_output=True, max_step=0.03)
    assert sol.success
    N = np.linspace(0, 2, 501)
    a = np.exp(N)
    exact = np.array([
        i0*a**(-(3 + xi)),
        a**(-3)*(d0 + branch*i0*(1 - a**(-xi))),
        v0 + (1 - branch)*xi*i0/(3 + xi)*(1 - a**(-(3 + xi))),
        1 - (1 - f0)*a**(-xi),
    ])
    err = np.max(np.abs(sol.sol(N) - exact), axis=1)
    assert np.max(err) < 1e-9
    return dict(zip(["rho_I", "rho_D", "V", "f"], map(float, err)))


def soliton_integrals():
    radius, scale, coupling = 1.7, 0.9, 0.6
    R = radius
    # Independent quadrature of radial energy and degree densities.
    e2 = quad(lambda r: 24*math.pi*scale**2*R**2*r*r/(r*r + R*R)**2,
              0, np.inf, epsabs=1e-11, epsrel=1e-11)[0]
    e4 = quad(lambda r: 192*math.pi*coupling*R**4*r*r/(r*r + R*R)**4,
              0, np.inf, epsabs=1e-11, epsrel=1e-11)[0]
    degree = quad(lambda r: 16*R**3/math.pi*r*r/(r*r + R*R)**3,
                  0, np.inf, epsabs=1e-12, epsrel=1e-12)[0]
    err = [abs(e2 - 6*math.pi**2*scale**2*R),
           abs(e4 - 6*math.pi**2*coupling/R), abs(degree - 1)]
    assert max(err) < 1e-9
    return {"errors_E2_E4_degree": err}


def cosmology(alpha, beta, rate0=0.3, tol=1e-11):
    # tau=H_i(t-t_i); density unit 3 M_Pl^2 H_i^2; a_i=1.
    # y=(ln a, rho_I, rho_D, V, rho_b, rho_r, f, M).
    branch, memory_time = 0.25, 0.7
    y0 = [0., 0.9499, 0., 0., 0.05, 0.0001, 0., 0.]
    def rhs(t, y):
        ell, i, d, v, b, r, f, memory = y
        E = math.sqrt(i + d + v + b + r)
        gamma = rate0*math.exp(alpha*f + beta*memory)
        Q = gamma*i
        return np.array([E, -3*E*i-Q, -3*E*d+branch*Q,
                         (1-branch)*Q, -3*E*b, -4*E*r,
                         (1-f)*gamma, (f-memory)/memory_time])
    sol = solve_ivp(rhs, [0, 12], y0, method="DOP853",
                    rtol=tol, atol=tol*1e-2, max_step=0.025,
                    dense_output=True)
    assert sol.success
    grid = np.linspace(0, 12, 2401)
    ys = sol.sol(grid)
    ell, i, d, v, b, r, f, memory = ys
    E = np.sqrt(i + d + v + b + r)
    q = (i+d+b+2*r-2*v)/(2*E**2)
    invariant = i*np.exp(3*ell) - y0[1]*(1-f)/(1-y0[6])
    invariant_d = d*np.exp(3*ell) - branch*y0[1]*(f-y0[6])/(1-y0[6])
    max_residual = 0.
    max_jerk_error = 0.
    for tt, yy in zip(grid[::10], ys.T[::10]):
        der = rhs(tt, yy)
        _, ii, dd, vv, bb, rr, ff, mm = yy
        ee = math.sqrt(ii+dd+vv+bb+rr)
        residual = sum(der[1:6]) + 3*ee*(ii+dd+bb+4*rr/3)
        max_residual = max(max_residual, abs(residual))
        edot = -1.5*(ii+dd+bb+4*rr/3)
        eddot = -1.5*(der[1]+der[2]+der[4]+4*der[5]/3)
        jerk = 1+3*edot/ee**2+eddot/ee**3
        rhs_jerk = 1+2*rr/ee**2+1.5*der[3]/ee**3
        max_jerk_error = max(max_jerk_error, abs(jerk-rhs_jerk))
    def q_at(t):
        _, ii, dd, vv, bb, rr, _, _ = sol.sol(t)
        return (ii+dd+bb+2*rr-2*vv)/(2*(ii+dd+vv+bb+rr))
    hits = np.flatnonzero(q < 0)
    transition = None
    if len(hits):
        k = hits[0]
        transition = brentq(q_at, grid[k-1], grid[k], xtol=1e-12)
    rows = []
    for t in [0, 0.5, 1, 2, 4, 8, 12]:
        ell1, i1, d1, v1, b1, r1, f1, m1 = sol.sol(t)
        e1 = math.sqrt(i1+d1+v1+b1+r1)
        rows.append(dict(tau=t, a=float(math.exp(ell1)), E=e1,
                         f=float(f1), M=float(m1), V=float(v1),
                         Omega_V=float(v1/e1**2), q=float(q_at(t))))
    assert np.min(ys[1:6]) > -1e-10
    assert np.min(np.diff(f)) > -1e-10
    assert np.max(np.diff(E)) < 1e-10
    assert np.min(f) > -1e-10 and np.max(f) < 1+1e-10
    assert max_residual < 1e-10 and max_jerk_error < 1e-9
    assert np.max(np.abs(invariant)) < 1e-8
    assert np.max(np.abs(invariant_d)) < 1e-8
    return {"transition_tau": transition, "rows": rows,
            "max_abs_survival_error": float(np.max(np.abs(invariant))),
            "max_abs_defect_error": float(np.max(np.abs(invariant_d))),
            "max_continuity_residual": max_residual,
            "max_jerk_identity_error": max_jerk_error}, sol


def main():
    out = {"versions": {"numpy": np.__version__, "scipy": scipy.__version__},
           "four_form": exact_four_form(), "lindblad_exact": exact_lindblad(),
           "analytic_benchmark": constant_rate_benchmark(),
           "soliton": soliton_integrals()}
    cases = [("sin_conversion",0.,0.,0.), ("sin_refuerzo",0.,0.,0.3),
             ("con_memoria",2.,1.,0.3)]
    for name, alpha, beta, gamma in cases:
        report, sol = cosmology(alpha,beta,gamma)
        out[name] = report
        if name == "con_memoria":
            refined, sol2 = cosmology(alpha,beta,gamma,tol=1e-13)
            grid = np.linspace(0,12,2001)
            err = float(np.max(np.abs(sol.sol(grid)-sol2.sol(grid))))
            assert err < 1e-8
            out["convergence_max_abs_state_error"] = err
            out["convergence_transition_error"] = abs(
                report["transition_tau"] - refined["transition_tau"])
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
```
