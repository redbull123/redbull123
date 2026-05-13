# 📡 Telecom Network Analytics Pipeline

> Pipeline de análisis end-to-end para eventos de señalización en redes móviles (SGSN-MME)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/status-in%20development-orange.svg)]()

## 📋 Descripción

Este proyecto implementa un pipeline completo de ingeniería de datos para analizar eventos de señalización en redes de telecomunicaciones móviles. Procesa y analiza eventos como attach, handover, paging y otros procedimientos de señalización SGSN-MME.

**Caso de uso:** Monitoreo y análisis de rendimiento de red móvil en tiempo casi-real, permitiendo detectar anomalías, calcular KPIs de red y optimizar la experiencia del usuario.

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────┐
│  Data Generator     │  Simulador de eventos de señalización
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   ETL Pipeline      │  Extracción, transformación y carga
│   (Apache Airflow)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   PostgreSQL DB     │  Almacenamiento persistente
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Analytics/Viz      │  Power BI / Streamlit
└─────────────────────┘
```

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Orchestration:** Apache Airflow 2.7+
- **Base de Datos:** PostgreSQL 14+
- **Visualización:** Power BI / Streamlit
- **Containerización:** Docker & Docker Compose *(próximamente)*
- **Cloud:** AWS (RDS, ECS, S3) *(próximamente)*

## 📊 Métricas y KPIs Analizados

### KPIs Principales
- **Attach Success Rate (ASR):** % de attach procedures exitosos
- **Handover Success Rate (HOSR):** % de handovers sin fallo
- **Paging Success Rate:** Tiempo de respuesta promedio de paging
- **Service Request Success Rate:** % de service requests exitosos

### Análisis Dimensionales
- Distribución temporal (horaria, diaria, semanal)
- Performance por celda/eNodeB
- Análisis de causas de fallo
- Detección de anomalías
- Comparativa horas pico vs normales

## 🚀 Quick Start

### Prerequisitos

```bash
Python 3.10 o superior
PostgreSQL 14+ (opcional para desarrollo inicial)
Git
```

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/redbull123/telecom-network-analytics.git
cd telecom-network-analytics
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Crear estructura de directorios:**
```bash
mkdir -p data/raw data/processed data/staging
```

### Uso del Generador de Datos

> Nota: el script actual se encuentra en `data_generator/generator_2.py`.

#### Generar dataset una sola vez

```bash
# Generar 10,000 eventos en JSON
python data_generator/generator_2.py --mode batch --events 10000 --format json

# Generar 50,000 eventos en CSV
python data_generator/generator_2.py --mode batch --events 50000 --format csv
```

#### Ejecutar en modo continuo (simulación de stream)

```bash
# Generar 1,000 eventos cada 60 segundos
python data_generator/generator_2.py --mode continuous --events 1000 --interval 60

# Detener con Ctrl+C
```

#### Opciones adicionales

```bash
# Con seed para reproducibilidad
python data_generator/generator_2.py --mode batch --events 10000 --seed 42

# Especificar directorio de salida
python data_generator/generator_2.py --mode batch --events 10000 --directory data/custom_output
```

#### Corrección conocida

- Se corrigió un bug donde el campo `plmn_id` no se incluía en la construcción de `Event` en `generator_2.py`, provocando `Event.__init__() missing 1 required positional argument: 'plmn_id'`. Ahora se genera con `plmn_id` tomado del valor de IMSI.

### Estructura de Datos Sintéticos

Los eventos generados incluyen los siguientes campos:

- `event_id`: Identificador único del evento
- `timestamp`: Marca de tiempo en formato ISO
- `event_type`: Tipo de evento (attach, handover, paging, service_request)
- `result`: Resultado (success, failure)
- `cause_code`: Código de causa del resultado
- `imsi`: Identificador internacional de suscriptor móvil
- `cell_id`: ID de la celda (ECGI)
- `enodeb_id`: ID del eNodeB
- `mme_id`: ID del MME
- `tracking_area`: Área de rastreo (TAI)
- `duration_ms`: Duración en milisegundos
- `rat_type`: Tipo de tecnología de acceso radio (LTE)
- `apn`: Nombre del punto de acceso de red
- `plmn_id`: Identificador de red pública móvil


### Ejemplos de Uso

```python
# Usar el generador en código Python
from data_generator.generator import TelecomEventGenerator

# Crear generador
generator = TelecomEventGenerator(seed=42)

# Generar eventos
events = generator.generate_batch(num_events=1000)

# Guardar a archivo
from pathlib import Path
generator.save_to_json(events, Path("data/raw/my_events.json"))
```

## 📂 Estructura del Proyecto

```
telecom-network-analytics/
├── .gitignore                  # Archivos ignorados por Git
├── README.md                   # Este archivo
├── requirements.txt            # Dependencias de Python
├── config/                     # Configuraciones
│   └── config.yaml            # (próximamente)
├── data/                       # Datos (gitignored)
│   ├── raw/                   # Datos crudos generados
│   ├── processed/             # Datos procesados
│   └── staging/               # Datos intermedios
├── data_generator/            # Generador de datos sintéticos
│   ├── __init__.py
│   └── generator.py           # Script principal del generador
├── sql/                       # Scripts SQL
│   └── schema.sql             # (próximamente)
├── etl/                       # Scripts ETL
│   └── (próximamente)
├── airflow/                   # DAGs de Airflow
│   └── dags/
│       └── (próximamente)
├── dashboards/                # Visualizaciones
│   ├── powerbi/               # Archivos Power BI
│   └── streamlit/             # App Streamlit (próximamente)
├── tests/                     # Tests unitarios
│   └── (próximamente)
└── docs/                      # Documentación adicional
    └── architecture.md        # (próximamente)
```

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto basándose en el archivo `.env.example`:

```bash
# Copiar el ejemplo
cp .env.example .env

# Editar .env con tus credenciales
```

#### Parámetros Principales
- `DB_URL`: URL de conexión a PostgreSQL.
- `RAW_DATA_DIR`: Directorio donde se guardan los eventos generados.
- `STAGING_DATA_DIR`: Directorio temporal para el proceso ETL.
- `PROCESSED_DATA_DIR`: Directorio para archivos ya procesados.


## 📝 Datos Sintéticos

Los eventos generados incluyen los siguientes campos:

```json
{
        "event_id": "event_1",
        "timestamp": "2026-03-22T17:46:16.635485",
        "event_type": "attach",
        "result": "success",
        "cause_code": "0_attach success",
        "imsi": "234133562293375",
        "cell_id": 2341019851,
        "enodeb_id": 1986,
        "mme_id": 2,
        "tracking_area": 234101,
        "duration_ms": 152,
        "rat_type": "LTE",
        "apn": "fwa.mcc10.mnc234.gprs",
        "plmn_id": "23413"
}
```

### Tipos de Eventos Soportados

- **attach** (35%): Initial attach, handover attach, periodic TAU
- **handover** (25%): X2 handover, S1 handover
- **paging** (20%): MT call, MT SMS
- **service_request** (15%): Data, voice, SMS

## 🤝 Contribuciones

Este es un proyecto de portafolio personal. Si tienes sugerencias o encuentras bugs, feel free to:

1. Fork el proyecto
2. Crear una rama con tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Raul Santana**
- Packet Core Specialist | EPC & 5G NSA | Network Automation & Data Engineering | Ericsson Stack
- LinkedIn: [ingraulsantana](https://linkedin.com/in/ingraulsantana)
- GitHub: [@redbull123](https://github.com/redbull123)
- Email: rjsantana95@gmail.com

## 🙏 Agradecimientos

- Dataset sintético inspirado en 3GPP TS 23.401 (GPRS enhancements for E-UTRAN access)
- Arquitectura basada en mejores prácticas de Data Engineering

---

⚠️ **Nota:** Este proyecto utiliza datos sintéticos simulados. No contiene información real o confidencial de ninguna red de telecomunicaciones.
