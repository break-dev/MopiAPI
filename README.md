# Backend de MOPI

## Desarrollo Local (sin Docker)

Si necesitas trabajar con el proyecto sin usar Docker, es **vital** gestionar las dependencias directamente con `pip` y un entorno virtual.

---

## Pre-requisitos

Antes de comenzar, debes tener instalado:

- **Python 3.10+**
- **FFmpeg** (obligatorio para el procesamiento multimedia)

### Instalación de FFmpeg

- **Windows:** usar binarios oficiales o `choco install ffmpeg`
- **macOS (Homebrew):**
  ```bash
  brew install ffmpeg
  ```
- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt install ffmpeg
  ```

### Archivos Requeridos

Crea estos archivos en la carpeta `app/`:

1. **`.env`** - Variables de entorno
2. **`cookies.txt`** - Para procesar videos de YouTube
3. **`bitacora.log`** - Archivo de logs

> **IMPORTANTE:** El archivo `.env` NO debe versionarse.

---

## Desarrollo en Windows

Abre una terminal (**PowerShell** o **CMD**) en el directorio raíz del proyecto.

### Gestión de Dependencias

| Tarea                     | Comando                               | Descripción                        |
| ------------------------- | ------------------------------------- | ---------------------------------- |
| **Crear Entorno**         | `python -m venv .venv`                | Crea el entorno virtual `.venv`    |
| **Activar Entorno**       | `.\.venv\Scripts\activate`            | Activa el entorno virtual          |
| **Actualizar pip**        | `python -m pip install --upgrade pip` | Actualiza el gestor de paquetes    |
| **Instalar Dependencias** | `pip install -r requirements.txt`     | Instala las librerías del proyecto |
| **Desactivar Entorno**    | `deactivate`                          | Sale del entorno virtual           |

### Mantenimiento

- **Actualizar pip:**

  ```bash
  python -m pip install --upgrade pip
  ```

- **Actualizar `requirements.txt`:**
  ```bash
  pip freeze > requirements.txt
  ```

### Limpieza de caché Python

```powershell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

---

## Desarrollo en macOS / Linux

Abre **Terminal** en el directorio raíz del proyecto.

### Gestión de Dependencias

| Tarea                     | Comando                                | Descripción                        |
| ------------------------- | -------------------------------------- | ---------------------------------- |
| **Crear Entorno**         | `python3 -m venv .venv`                | Crea el entorno virtual `.venv`    |
| **Activar Entorno**       | `source .venv/bin/activate`            | Activa el entorno virtual          |
| **Actualizar pip**        | `python3 -m pip install --upgrade pip` | Actualiza el gestor de paquetes    |
| **Instalar Dependencias** | `pip install -r requirements.txt`      | Instala las librerías del proyecto |
| **Desactivar Entorno**    | `deactivate`                           | Sale del entorno virtual           |

### Mantenimiento

- **Actualizar pip:**

  ```bash
  python3 -m pip install --upgrade pip
  ```

- **Actualizar `requirements.txt`:**
  ```bash
  pip freeze > requirements.txt
  ```

### Limpieza de caché Python

```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## Ejecución del Backend

Con el entorno virtual activado:

```bash
fastapi dev app/main.py
```

El backend quedará disponible en:

- **API:** [http://localhost:8000](http://localhost:8000)
- **Documentación:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Configuración y Uso con Docker

El servicio se levanta usando el archivo `docker-compose.yml` del proyecto.

### Inicio del Servicio

```bash
docker compose up -d
```

> La bandera `-d` ejecuta los contenedores en segundo plano.

Verifica que esté activo:

```bash
docker ps
```

Deberías ver el contenedor `cnt-apimopi`.

### Comandos Útiles de Docker

| Comando                                                     | Descripción                                 |
| ----------------------------------------------------------- | ------------------------------------------- |
| `docker compose up -d`                                      | Inicia los servicios en segundo plano       |
| `docker compose down`                                       | Detiene y elimina contenedores y redes      |
| `docker compose restart`                                    | Reinicia los servicios                      |
| `docker run -d --name cnt-apimopi -p 8080:80 iso-apimopi`   | Crea y arranca el contenedor                |
| `docker stop cnt-apimopi`                                   | Detiene el contenedor                       |
| `docker start cnt-apimopi`                                  | Inicia el contenedor detenido               |
| `docker logs -f cnt-apimopi`                                | Logs en tiempo real                         |
| `docker rm cnt-apimopi`                                     | Elimina el contenedor (debe estar detenido) |
| `docker build -t iso-apimopi .`                             | Construye la imagen del backend             |
| `docker rmi iso-apimopi`                                    | Elimina la imagen local                     |
| `docker ps -a`                                              | Lista todos los contenedores                |

---

## 📝 Cookies para YouTube

Para procesar videos de YouTube:

1. Crea el archivo **`cookies.txt`** dentro de `app/`
2. Obtén las cookies desde tu navegador

Referencia oficial:  
[https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
