# 📖 Diccionario de Variables - Análisis DiDi Food

**Versión:** 2.0 (Actualizado)  
**Periodo:** 5 Dic 2025 - 25 Ene 2026 (24 días)

---

## 🎯 Variables Primarias (Dataset Original)

| Variable | Tipo | Definición |
| :--- | :--- | :--- |
| `fecha` | DATE | Fecha de operación (YYYY-MM-DD) |
| `ingreso_base` | DECIMAL | Pago base calculado por DiDi antes de bonos (COP) |
| `complemento_bono` | DECIMAL | Bonificaciones adicionales pagadas por DiDi (COP) |
| `pedidos_fisicos` | INT | Total de entregas reales realizadas en el día |
| `unidades_progreso`| INT | **Pedidos Cohete:** Entregas ≥7km (Cuentan doble) |
| `gastos_operativos`| DECIMAL | Gastos de combustible, comida y otros (COP) |

---

## 🚀 ¿Qué son los "Pedidos Cohete"?

Un **"pedido cohete"** es una entrega con distancia ≥ 7km. En el sistema de DiDi, estos pedidos son estratégicos porque cuentan doble para alcanzar las metas de bonos semanales.

* **Fórmula de Eficiencia:** `(Pedidos Cohete / Pedidos Físicos) * 100`
* **Ejemplo:** Si haces 15 pedidos y los 15 son cohetes, tienes **100% de eficiencia**.

---

## 📊 Variables Calculadas (Derivadas)

| Variable | Fórmula | Interpretación |
| :--- | :--- | :--- |
| `utilidad_real` | `ingreso_total - gastos` | Ganancia neta real del día |
| `eficiencia_cohete`| `(cohetes / físicos) * 100` | % de pedidos largos (Meta: >80%) |
| `ingreso_x_pedido` | `ingreso_total / físicos` | Valor promedio de cada entrega |

---

## 📈 Clasificación de Desempeño

### Nivel de Eficiencia
* **Excelente (≥ 90%):** Estrategia de cohetes ejecutada a la perfección.
* **Alto (70% - 89%):** Mayoría de pedidos fueron cohetes.
* **Medio/Bajo (< 70%):** Predominancia de pedidos cortos (menos rentables).

---

## 📝 Limitaciones Técnicas
* No se cuenta con registro de tipo de vehículo (Moto/Bici).
* No se registra la latencia geográfica (kilómetros recorridos sin pedido).
* Los gastos son reportados de forma agregada.
