# Gestor de Eventos Locales
## Trabajo de Fin de Grado

**CENTRO INTEGRADO MARÍA ANA SANZ**  
**PAMPLONA**  
**2º GRADO SUPERIOR**  
**DESARROLLO DE APLICACIONES MULTIPLATAFORMA**

**Autor:** Martin Peñalva Artázcoz  
**Tutor/a Académico:** XXXXXXXX  
**Tutor/a TFG:** XXXXXXXX  
**Pamplona, 2024**

**Repositorio del Proyecto:** [https://github.com/martinPenalva/prueba-PP.git](https://github.com/martinPenalva/prueba-PP.git)

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Objetivos](#1-objetivos)
3. [Recursos Software y Hardware](#2-recursos-software-y-hardware)
   - [2.1. Software](#21-software)
   - [2.2. Hardware](#22-hardware)
4. [Enumeración y Desarrollo de las Fases](#3-enumeración-y-desarrollo-de-las-fases)
   - [3.1. Fase 1: Análisis y Diseño](#31-fase-1-análisis-y-diseño)
   - [3.2. Fase 2: Desarrollo Frontend y Backend](#32-fase-2-desarrollo-frontend-y-backend)
   - [3.3. Fase 3: Implementación de Concurrencia y Optimización](#33-fase-3-implementación-de-concurrencia-y-optimización)
   - [3.4. Fase 4: Pruebas, Documentación y Lanzamiento](#34-fase-4-pruebas-documentación-y-lanzamiento)
5. [Conclusiones](#conclusiones)
6. [Bibliografías y Referencias](#bibliografías-y-referencias)

---

## Introducción

![Icono de la Aplicación](PROYECTO_FINAL_IMAGENES/ICONO_APLICACION.png)
*Figura: Icono de la aplicación Gestor de Eventos Locales*

En la actualidad, la gestión de eventos locales se ha convertido en una necesidad fundamental para organizaciones, ayuntamientos y entidades que buscan coordinar actividades, talleres, conferencias y eventos de diversa índole dentro de sus comunidades. Este escenario plantea desafíos significativos para los gestores, quienes se enfrentan a la dificultad de centralizar la información de participantes, gestionar inscripciones, controlar aforos y mantener un registro organizado de todos los eventos programados.

La complejidad aumenta cuando múltiples usuarios necesitan trabajar simultáneamente sobre los mismos datos, lo que puede generar conflictos, pérdida de información o inconsistencias en los registros. Además, la necesidad de generar informes y reportes para la distribución y archivo de información requiere herramientas que faciliten la exportación de datos en formatos estándar como CSV y PDF.

En el contexto actual, muchas organizaciones gestionan eventos mediante hojas de cálculo o sistemas básicos que no ofrecen las funcionalidades necesarias para una gestión eficiente. Esto se traduce en procesos manuales tediosos, mayor probabilidad de errores y dificultades para coordinar equipos de trabajo.

El mercado de software de gestión de eventos ha experimentado un crecimiento significativo en los últimos años. Según estudios recientes, las organizaciones que utilizan sistemas especializados de gestión de eventos reportan una mejora del 40% en la eficiencia de sus procesos. Sin embargo, muchas soluciones disponibles son costosas, requieren infraestructura compleja o no se adaptan a las necesidades específicas de eventos locales.

En este contexto, el **Gestor de Eventos Locales** emerge como una solución integral que no solo centraliza la información de eventos y participantes, sino que también mejora la experiencia del usuario al ofrecer una plataforma unificada para gestionar todos los aspectos relacionados con la organización de eventos. La aplicación ofrecerá funcionalidades como gestión completa de eventos (crear, editar, eliminar), administración de participantes, sistema de inscripciones con control de aforo, búsqueda y filtrado avanzado, y la posibilidad de exportar datos a CSV y PDF para su distribución y archivo.

Para llevar a cabo este proyecto, se ha empleado tecnología moderna y ampliamente utilizada, con un enfoque en el lenguaje de programación **Python** para el desarrollo de la aplicación de escritorio. Además, se ha integrado una base de datos **MySQL** para el almacenamiento persistente de datos, con un sistema avanzado de gestión de concurrencia que permite múltiples usuarios trabajando simultáneamente sin conflictos. Para la interfaz gráfica se ha utilizado **Tkinter**, la biblioteca estándar de Python para desarrollo de interfaces gráficas de usuario.

En el desarrollo de la aplicación, se han empleado librerías modernas y ampliamente utilizadas por la comunidad de desarrolladores Python, como `mysql-connector-python` para la conexión a la base de datos, `bcrypt` para el hash seguro de contraseñas, `ReportLab` para la generación de PDFs, y `python-dotenv` para la gestión de configuración mediante variables de entorno, con el fin de garantizar un rendimiento óptimo, seguridad y una experiencia de usuario satisfactoria.

Una de las características más destacadas de esta aplicación es su capacidad para soportar múltiples usuarios simultáneos mediante un sistema avanzado de gestión de concurrencia que incluye control de versiones optimista, bloqueos transaccionales, sistema de locks por recurso, procesamiento paralelo y reintentos automáticos con backoff exponencial.

---

## 1. OBJETIVOS

Debido a lo comentado anteriormente, he decidido emprender el desarrollo de una aplicación de escritorio para sistemas Windows (compatible con otros sistemas operativos) desarrollada en Python. Esta aplicación tiene como objetivo brindar a los gestores de eventos una herramienta integral para la gestión centralizada de eventos locales, participantes e inscripciones. Entre las características destacadas se incluyen:

- Gestión completa de eventos (crear, editar, eliminar, buscar)
- Administración de participantes con validación de datos
- Sistema de inscripciones con control de aforo automático
- Búsqueda y filtrado avanzado
- Exportación de datos a CSV y PDF
- Sistema de autenticación y autorización basado en roles (administrador y usuario)

Además, se incorporará la funcionalidad de soporte para múltiples usuarios simultáneos, permitiendo que varios gestores trabajen al mismo tiempo sobre los mismos datos sin generar conflictos ni pérdida de información, mediante un sistema avanzado de gestión de concurrencia que incluye control de versiones optimista, bloqueos transaccionales y procesamiento paralelo.

El propósito fundamental de este Trabajo de Fin de Grado es profundizar en el desarrollo de aplicaciones de escritorio y explorar el uso de tecnologías modernas en Python. Asimismo, se pretende poner en práctica diversos conceptos adquiridos durante el curso de mi formación en grado superior de informática. A través de este proyecto, se espera adquirir experiencia en el uso de herramientas como MySQL para bases de datos relacionales, Tkinter para interfaces gráficas, y sistemas avanzados de gestión de concurrencia.

Adicionalmente, este proyecto me permitirá desarrollar habilidades en arquitectura de software, específicamente en el patrón Modelo-Vista-Controlador (MVC), gestión de bases de datos relacionales, programación orientada a objetos, y resolución de problemas complejos de concurrencia en sistemas multi-usuario.

---

## 2. RECURSOS SOFTWARE Y HARDWARE

### 2.1. Software

#### 2.1.1. Python

Python ha sido fundamental para el desarrollo de este proyecto. Desde las etapas iniciales, hemos empleado este lenguaje de programación, empezando con la configuración del proyecto, hasta su implementación y pruebas. Su sintaxis clara, su amplia biblioteca estándar y su ecosistema de librerías han sido esenciales para agilizar el proceso de desarrollo.

**Características principales:**
- **Lenguaje de Programación:** Python 3.8+ se ha utilizado como lenguaje principal para el desarrollo de toda la aplicación, aprovechando sus características de programación orientada a objetos, tipado dinámico y sintaxis clara y legible.

<img src="PROYECTO_FINAL_IMAGENES/logotipo_python.png" alt="Logotipo de Python" width="200"/>
*Figura: Logotipo oficial de Python*

- **Edición de Código:** Se ha utilizado Visual Studio Code como editor principal, proporcionando funciones avanzadas como resaltado de sintaxis, completado automático, depuración integrada y gestión de extensiones.

![Editor de Código Python en Visual Studio Code](PROYECTO_FINAL_IMAGENES/ejemplo_editor_Ejemplo del Editor de Código Python en Visual Studio Code.png)
*Figura: Ejemplo del editor Visual Studio Code mostrando código Python con resaltado de sintaxis*

- **Estructura del Proyecto:** Python nos ha permitido organizar el código en módulos y paquetes siguiendo el patrón MVC (Modelo-Vista-Controlador), facilitando la mantenibilidad y escalabilidad del proyecto.

#### 2.1.2. Tkinter

Tkinter se ha utilizado como framework para el desarrollo de la interfaz gráfica de usuario (GUI) de la aplicación. Esta decisión se basa en las ventajas que nos ofrece Tkinter en términos de simplicidad, integración nativa con Python y disponibilidad multiplataforma.

**Características principales:**
- **Interfaz Gráfica Nativa:** Tkinter es la biblioteca estándar de Python para desarrollo de interfaces gráficas, lo que nos ha permitido crear ventanas, formularios, tablas y componentes interactivos sin necesidad de dependencias externas adicionales.

<img src="PROYECTO_FINAL_IMAGENES/logotipo_thinker.png" alt="Logotipo Tkinter" width="200"/>
*Figura: Logotipo de Tkinter*

- **Diseño de Ventanas:** Tkinter proporciona un conjunto completo de widgets (botones, etiquetas, campos de texto, tablas, etc.) que hemos utilizado para diseñar una interfaz intuitiva y funcional.
- **Personalización y Estilos:** Aunque Tkinter tiene un aspecto visual básico, hemos logrado personalizar la interfaz mediante el uso de colores, fuentes y layouts personalizados para crear una experiencia de usuario moderna y atractiva.

#### 2.1.3. MySQL

MySQL ha sido utilizado como sistema de gestión de bases de datos relacionales (RDBMS) para almacenar toda la información de la aplicación, incluyendo usuarios, eventos, participantes e inscripciones.

<img src="PROYECTO_FINAL_IMAGENES/logotipo_MYSQL.png" alt="Logotipo de MySQL" width="200"/>
*Figura: Logotipo oficial de MySQL*

**Características principales:**
- **Base de Datos Relacional:** MySQL nos ha permitido diseñar un esquema de base de datos normalizado con tablas relacionadas mediante claves foráneas, garantizando la integridad referencial y la consistencia de los datos.
- **Esquema de Base de Datos:** Hemos diseñado un esquema que incluye las tablas: `users` (usuarios), `events` (eventos), `participants` (participantes), `event_registrations` (inscripciones) y `audit_logs` (logs de auditoría), con sus respectivas relaciones y restricciones.

![Tabla Users](PROYECTO_FINAL_IMAGENES/tabla_users.png)
*Figura: Estructura de la tabla users*

![Tabla Events](PROYECTO_FINAL_IMAGENES/tabla_eventos.png)
*Figura: Estructura de la tabla events con campo version para control de concurrencia*

![Tabla Participants](PROYECTO_FINAL_IMAGENES/tabla_participantes.png)
*Figura: Estructura de la tabla participants*

![Tabla Event Registrations](PROYECTO_FINAL_IMAGENES/tabla_event_registrations.png)
*Figura: Estructura de la tabla event_registrations*

![Tabla Audit Logs](PROYECTO_FINAL_IMAGENES/tabla_auditlogs.png)
*Figura: Estructura de la tabla audit_logs*

- **Pool de Conexiones:** MySQL soporta pools de conexiones que hemos implementado para permitir múltiples usuarios simultáneos, optimizando el rendimiento y la gestión de recursos.
- **Transacciones y Aislamiento:** MySQL nos ha permitido utilizar transacciones con diferentes niveles de aislamiento (REPEATABLE READ) para garantizar la consistencia de datos en operaciones concurrentes.

#### 2.1.4. MySQL Connector Python

MySQL Connector Python ha sido la librería utilizada para establecer la comunicación entre la aplicación Python y la base de datos MySQL.

**Características principales:**
- **Conexión a Base de Datos:** MySQL Connector Python nos ha permitido establecer conexiones seguras a la base de datos MySQL, manejando autenticación, encriptación y gestión de errores de manera eficiente.
- **Pool de Conexiones:** La librería incluye soporte para pools de conexiones (MySQLConnectionPool) que hemos utilizado para gestionar múltiples conexiones simultáneas, mejorando el rendimiento de la aplicación con múltiples usuarios.

![Configuración de Base de Datos](PROYECTO_FINAL_IMAGENES/DB_CONFIG.png)
*Figura: Configuración de conexión a MySQL*

![Patrón Singleton](PROYECTO_FINAL_IMAGENES/Captura del patrón Singleton con `__new__` y `_lock`.png)
*Figura: Implementación del patrón Singleton para el pool de conexiones*

![Creación del Pool](PROYECTO_FINAL_IMAGENES/create_conection_pool.png)
*Figura: Método que crea el pool de conexiones MySQL*

![Método get_connection](PROYECTO_FINAL_IMAGENES/get_conection.png)
*Figura: Método get_connection() que permite a cada usuario tener su propia conexión*

- **Ejecución de Consultas:** MySQL Connector Python proporciona métodos para ejecutar consultas SQL (SELECT, INSERT, UPDATE, DELETE) de manera segura mediante prepared statements, previniendo inyecciones SQL.
- **Gestión de Transacciones:** La librería nos ha permitido gestionar transacciones completas, incluyendo commit y rollback, esencial para mantener la integridad de los datos en operaciones complejas.

#### 2.1.5. bcrypt

bcrypt ha sido utilizado para el hash seguro de contraseñas de usuarios, garantizando que las contraseñas nunca se almacenen en texto plano en la base de datos.

<img src="PROYECTO_FINAL_IMAGENES/logo_bcrypt.png" alt="Logotipo de bcrypt" width="200"/>
*Figura: Logotipo de bcrypt*

**Características principales:**
- **Hash Seguro de Contraseñas:** bcrypt implementa el algoritmo bcrypt, un algoritmo de hash criptográfico diseñado específicamente para contraseñas, que incluye salting automático y es resistente a ataques de fuerza bruta.

![Implementación de Autenticación con bcrypt](PROYECTO_FINAL_IMAGENES/Implementación de Autenticación con bcrypt.png)
*Figura: Implementación de hash de contraseñas con bcrypt*

- **Verificación de Contraseñas:** bcrypt nos ha permitido verificar contraseñas de manera segura comparando el hash almacenado con el hash de la contraseña introducida, sin necesidad de almacenar la contraseña en texto plano.
- **Seguridad:** El uso de bcrypt garantiza que incluso si la base de datos es comprometida, las contraseñas no pueden ser recuperadas fácilmente, ya que el algoritmo es unidireccional y computacionalmente costoso de revertir.

#### 2.1.6. ReportLab

ReportLab ha sido utilizado para la generación de documentos PDF a partir de los datos de la aplicación, permitiendo exportar eventos, participantes e inscripciones en formato PDF.

<img src="PROYECTO_FINAL_IMAGENES/logotipo_reportlab.png" alt="Logotipo de ReportLab" width="200"/>
*Figura: Logotipo de ReportLab*

**Características principales:**
- **Generación de PDFs:** ReportLab nos ha permitido crear documentos PDF profesionales con tablas, texto formateado, encabezados y pies de página, proporcionando una solución completa para la exportación de datos.
- **Exportación de Datos:** Hemos implementado funcionalidades para exportar listados de eventos, participantes e inscripciones a PDF, con formato tabular y diseño profesional.
- **Personalización:** ReportLab nos ha permitido personalizar completamente el diseño de los PDFs, incluyendo fuentes, colores, márgenes y estructura, adaptándolos a las necesidades del proyecto.

![Configuración de Exportación](PROYECTO_FINAL_IMAGENES/EXPORT_CONFIG.png)
*Figura: Configuración de exportación a PDF y CSV*

#### 2.1.7. python-dotenv

python-dotenv ha sido utilizado para la gestión de configuración mediante variables de entorno, permitiendo separar la configuración del código fuente y facilitar el despliegue en diferentes entornos.

**Características principales:**
- **Gestión de Configuración:** python-dotenv nos ha permitido almacenar configuraciones sensibles como credenciales de base de datos, puertos y otros parámetros en un archivo `.env` separado del código fuente.

![Ejemplo de python-dotenv](PROYECTO_FINAL_IMAGENES/dotenv_python.png)
*Figura: Ejemplo de uso de python-dotenv para cargar variables de entorno*

- **Seguridad:** El uso de variables de entorno mediante python-dotenv garantiza que las credenciales no se expongan en el código fuente, mejorando la seguridad de la aplicación.
- **Flexibilidad:** python-dotenv nos ha permitido tener diferentes configuraciones para desarrollo, pruebas y producción sin modificar el código fuente.

![Configuración de la Aplicación](PROYECTO_FINAL_IMAGENES/APP_CONFIG.png)
*Figura: Configuración general de la aplicación*

#### 2.1.8. GitHub y Git

GitHub se ha utilizado como plataforma de control de versiones para almacenar y gestionar el código fuente del proyecto. Git, como sistema de control de versiones, nos ha permitido realizar un seguimiento de los cambios en el código y revertir a versiones anteriores en caso necesario.

<img src="PROYECTO_FINAL_IMAGENES/logo_Github.png" alt="Logotipo de GitHub" width="200"/>
*Figura: Logotipo de GitHub*

**Repositorio del Proyecto:** [https://github.com/martinPenalva/prueba-PP.git](https://github.com/martinPenalva/prueba-PP.git)

**Características principales:**
- **Control de Versiones:** Utilizamos Git para mantener un historial completo de cambios en el código fuente, lo que nos permite mantener un registro de todas las modificaciones realizadas y colaborar de manera eficiente.

![Commits en GitHub](PROYECTO_FINAL_IMAGENES/commits_github.png)
*Figura: Historial de commits del proyecto en GitHub*

- **Colaboración y Gestión de Proyectos:** GitHub proporciona herramientas para la gestión de proyectos, seguimiento de problemas y documentación, lo que ha facilitado el proceso de desarrollo del proyecto.

### 2.2. Hardware

#### 2.2.1. Ordenador de sobremesa

El ordenador de sobremesa ha sido el principal entorno de desarrollo utilizado para el proyecto. Su potencia de procesamiento y memoria RAM han permitido ejecutar Python, MySQL Server, Visual Studio Code y otras herramientas de desarrollo de manera eficiente.

#### 2.2.2. Sistema de doble monitor

El sistema de doble monitor ha mejorado la productividad del desarrollo al proporcionar más espacio de pantalla para trabajar simultáneamente en código, documentación, base de datos y herramientas de desarrollo.

#### 2.2.3. Ordenador portátil

El ordenador portátil ha sido utilizado como una herramienta complementaria para el desarrollo en entornos fuera del ámbito habitual.

---

## 3. ENUMERACIÓN Y DESARROLLO DE LAS FASES

### 3.0.1. Diagrama de Gantt

Para proporcionar una visión más clara y detallada de las fases del proyecto, se incluye un cronograma visual o diagrama de Gantt que representa las fases y actividades principales a lo largo del tiempo.

**Actividades realizadas en cada fase:**

- **Análisis y Diseño:** Se identificaron los requisitos funcionales y no funcionales de la aplicación. Se realizó análisis de necesidades para recoger ideas. Se diseñó la arquitectura de la aplicación siguiendo el patrón MVC, incluyendo el diseño de la base de datos y las interfaces de usuario.

- **Desarrollo Frontend:** Se implementaron las pantallas principales de la aplicación, como la pantalla de login, ventana principal, gestión de eventos, gestión de participantes, inscripciones y reportes.

- **Desarrollo Backend:** Se configuró MySQL para manejar el almacenamiento de datos. Se implementaron los controladores necesarios para la lógica de negocio y la comunicación entre el frontend y la base de datos.

- **Implementación de Concurrencia:** Se desarrolló un sistema avanzado de gestión de concurrencia para soportar múltiples usuarios simultáneos, incluyendo control de versiones optimista, bloqueos transaccionales y procesamiento paralelo.

- **Pruebas y Depuración:** Se realizaron pruebas para componentes individuales de la aplicación, así como pruebas para asegurar el correcto funcionamiento de la aplicación general y el sistema de concurrencia. Se corrigieron los errores encontrados.

- **Documentación y Lanzamiento:** Se preparó la documentación técnica completa del proyecto y se realizaron las pruebas finales para garantizar la estabilidad y fiabilidad de la aplicación.

### 3.1. Fase 1: Análisis y Diseño

**Fecha de Inicio:** [Fecha]  
**Fecha de Finalización:** [Fecha]

**Actividades:**
- ⮚ Análisis de Requisitos del Proyecto: Se llevó a cabo una revisión exhaustiva de los requisitos del proyecto, identificando las necesidades y expectativas de los usuarios finales.
- ⮚ Investigación de Tecnologías y Herramientas: Se realizó una investigación detallada de las tecnologías y herramientas disponibles para el desarrollo de aplicaciones de escritorio en Python.
- ⮚ Diseño de la Arquitectura: Se diseñó la arquitectura de la aplicación siguiendo el patrón Modelo-Vista-Controlador (MVC), definiendo las capas de presentación, lógica de negocio y acceso a datos.
- ⮚ Diseño de la Base de Datos: Se diseñó el esquema de la base de datos, definiendo las tablas, relaciones, índices y restricciones necesarias.

**Desarrollo:**

Durante esta fase, se asignaron los primeros días para realizar un análisis detallado de los requisitos del proyecto. Se definieron los objetivos y alcance del proyecto. Posteriormente, se dedicaron sesiones de trabajo a recopilar y documentar los requisitos específicos del proyecto, lo que incluyó investigación de herramientas a usar.

Una vez definidas las tecnologías, se procedió al diseño de la arquitectura de la aplicación siguiendo el patrón MVC, definiendo claramente las responsabilidades de cada capa. Simultáneamente, se diseñó el esquema de la base de datos, identificando las entidades principales (usuarios, eventos, participantes, inscripciones) y sus relaciones.

![Diagrama de Arquitectura](PROYECTO_FINAL_IMAGENES/diagrama.png)
*Figura: Diagrama de arquitectura del sistema mostrando las capas MVC y las relaciones entre componentes*

### 3.2. Fase 2: Desarrollo Frontend y Backend

**Fecha de Inicio:** [Fecha]  
**Fecha de Finalización:** [Fecha]

**Actividades:**
- ⮚ Desarrollo de Interfaces de Usuario: Se diseñaron y desarrollaron las interfaces de usuario para la aplicación de escritorio utilizando Python y Tkinter.
- ⮚ Implementación de Funcionalidades del Backend: Se desarrollaron las funcionalidades del backend utilizando Python y MySQL.
- ⮚ Integración de Base de Datos: Se integró la base de datos MySQL con la aplicación, implementando el sistema de conexión mediante pool de conexiones.
- ⮚ Implementación de Autenticación: Se implementó el sistema de autenticación de usuarios con hash seguro de contraseñas utilizando bcrypt.

**Desarrollo:**

Las semanas de desarrollo se han centrado en el desarrollo del frontend de la aplicación de escritorio, asignando tareas específicas para el diseño de interfaces de usuario y la implementación de funcionalidades básicas.

Simultáneamente, se ha trabajado en el backend de la aplicación, configurando la infraestructura necesaria en MySQL y desarrollando las funciones de autenticación de usuarios y gestión de datos.

#### Etapa 1: Diseño de la Ventana de Login

Durante esta fase inicial, me centré en diseñar la ventana de login, la cual es la primera interfaz que ve el usuario al abrir la aplicación. Se estableció su estructura para validar credenciales y gestionar el acceso a la aplicación.

![Ventana de Login](PROYECTO_FINAL_IMAGENES/login.png)
*Figura: Ventana de login de la aplicación en ejecución*

![Método handle_login](PROYECTO_FINAL_IMAGENES/handle_login_1.png)
*Figura: Método handle_login() que valida las credenciales del usuario*

![Método start](PROYECTO_FINAL_IMAGENES/metodo_start.png)
*Figura: Método start() que inicia la aplicación mostrando la ventana de login*

![Método on_login_success](PROYECTO_FINAL_IMAGENES/on_login_success___1.png)
*Figura: Método on_login_success() que gestiona el acceso tras el login exitoso*

![Código de AuthController](PROYECTO_FINAL_IMAGENES/Código de AuthController.png)
*Figura: Implementación completa del AuthController con métodos de autenticación*

![Ventana de Registro](PROYECTO_FINAL_IMAGENES/registrarse.png)
*Figura: Ventana de registro de nuevos usuarios*

#### Etapa 2: Diseño de la Ventana Principal

Después de definir la ventana de login, se procedió al diseño de la ventana principal. Esta pantalla es crucial ya que es el centro de control de toda la aplicación. Se dedicó especial atención a la disposición de los elementos de la interfaz de usuario, incluyendo un menú lateral para la navegación entre diferentes secciones.

![Vista de Inicio](PROYECTO_FINAL_IMAGENES/pantalla_unaveziniciado.png)
*Figura: Vista de inicio de la aplicación mostrando el resumen general y estadísticas*

![Método create_sidebar](PROYECTO_FINAL_IMAGENES/create_sidebar.png)
*Figura: Método create_sidebar() que crea el menú lateral de navegación*

![Método show_home](PROYECTO_FINAL_IMAGENES/show_home.png)
*Figura: Método show_home() que muestra la vista de inicio con estadísticas*

![Método setup_icon](PROYECTO_FINAL_IMAGENES/setup_icon.png)
*Figura: Método setup_icon() que configura el icono de la aplicación*

#### Etapa 3: Desarrollo de Modelos de Datos

Se desarrollaron los modelos de datos que representan las entidades del dominio de negocio.

![Constructor de User](PROYECTO_FINAL_IMAGENES/Captura del constructor de la clase User mostrando todos los atributos.png)
*Figura: Constructor de la clase User con todos sus atributos*

![Métodos to_dict y from_dict](PROYECTO_FINAL_IMAGENES/Captura de los métodos to_dict() y from_dict()..png)
*Figura: Métodos to_dict() y from_dict() para serialización de datos*

![Constructor de Event con version](PROYECTO_FINAL_IMAGENES/Captura del constructor mostrando el campo version.png)
*Figura: Constructor de Event mostrando el campo version para control de concurrencia*

![Modelo Participant](PROYECTO_FINAL_IMAGENES/participant.png)
*Figura: Modelo completo de Participant*

![Propiedad full_name](PROYECTO_FINAL_IMAGENES/Captura de la propiedad full_name.png)
*Figura: Propiedad full_name que retorna el nombre completo del participante*

#### Etapa 4: Vista de Gestión de Eventos

Se desarrolló la vista completa de gestión de eventos, permitiendo crear, editar, eliminar y buscar eventos de manera intuitiva.

![Vista de Eventos](PROYECTO_FINAL_IMAGENES/eventos_view.png)
*Figura: Vista de gestión de eventos mostrando la tabla de eventos y opciones de acción*

![Método create_widgets de EventView](PROYECTO_FINAL_IMAGENES/create_widgets.png)
*Figura: Método create_widgets() de EventView que crea los componentes de la interfaz*

#### Etapa 5: Vista de Gestión de Participantes

Se implementó la vista de gestión de participantes, que permite administrar toda la información de los participantes del sistema.

![Vista de Participantes](PROYECTO_FINAL_IMAGENES/participantes_view.png)
*Figura: Vista de gestión de participantes mostrando la tabla con todos los participantes*

![Método create_widgets de ParticipantView](PROYECTO_FINAL_IMAGENES/create_widgets_participantes.png)
*Figura: Método create_widgets() de ParticipantView que crea los componentes de la interfaz*

#### Etapa 6: Vista de Inscripciones

Se desarrolló la vista de inscripciones, que permite gestionar las inscripciones de participantes a eventos, con control de aforo y validaciones.

![Vista de Inscripciones](PROYECTO_FINAL_IMAGENES/incripciones_view.png)
*Figura: Vista de gestión de inscripciones mostrando las inscripciones activas*

![Método create_widgets de RegistrationView](PROYECTO_FINAL_IMAGENES/create_widgets() de RegistrationView.png)
*Figura: Método create_widgets() de RegistrationView que crea los componentes de la interfaz*

![Proceso de Inscripción](PROYECTO_FINAL_IMAGENES/incribirse.png)
*Figura: Formulario de inscripción de un participante a un evento*

![Inscripción Exitosa](PROYECTO_FINAL_IMAGENES/inscribirse_correctamente.png)
*Figura: Confirmación de inscripción exitosa a un evento*

![Mensaje de Registro Correcto](PROYECTO_FINAL_IMAGENES/mensaje_registro_correcto.png)
*Figura: Mensaje de confirmación tras registrar un participante correctamente*

#### Etapa 7: Vista de Reportes y Exportación

Se implementó la funcionalidad de exportación de datos a CSV y PDF, permitiendo generar reportes de eventos, participantes e inscripciones.

![Ventana de Reportes y Exportación](PROYECTO_FINAL_IMAGENES/ventana_reportes_exportar.png)
*Figura: Vista de reportes mostrando las opciones de exportación a CSV y PDF*

![Código de Exportación a CSV](PROYECTO_FINAL_IMAGENES/Código de Exportación a CSV.png)
*Figura: Implementación del método export_events() de CSVExporter*

![Código de Exportación a PDF](PROYECTO_FINAL_IMAGENES/Código de Exportación a PDF.png)
*Figura: Implementación del método export_events() de PDFExporter*

### 3.3. Fase 3: Implementación de Concurrencia y Optimización

**Fecha de Inicio:** [Fecha]  
**Fecha de Finalización:** [Fecha]

**Actividades:**
- ⮚ Implementación de Control de Versiones Optimista: Se implementó un sistema de control de versiones optimista para prevenir conflictos cuando múltiples usuarios intentan modificar el mismo evento simultáneamente.
- ⮚ Implementación de Bloqueos Transaccionales: Se implementó el uso de SELECT FOR UPDATE en las operaciones de inscripción para prevenir condiciones de carrera.
- ⮚ Desarrollo del Sistema de Locks de Recursos: Se desarrolló un sistema de locks por recurso (ResourceLockManager) que permite bloquear recursos específicos de forma independiente.
- ⮚ Implementación de Procesamiento Paralelo: Se implementó un sistema de procesamiento paralelo de suscripciones utilizando worker threads y colas thread-safe.
- ⮚ Implementación de Reintentos con Backoff Exponencial: Se implementó un sistema de reintentos automáticos con backoff exponencial para operaciones críticas.

**Desarrollo:**

Esta fase se centró en la implementación de un sistema avanzado de gestión de concurrencia que permite a múltiples usuarios trabajar simultáneamente sobre los mismos datos sin generar conflictos ni pérdida de información.

![Configuración de Concurrencia](PROYECTO_FINAL_IMAGENES/CONCURRENCY_CONFIG.png)
*Figura: Configuración del sistema de concurrencia con timeouts, reintentos y tamaño del pool*

#### Etapa 1: Control de Versiones Optimista

Se implementó un sistema de control de versiones optimista en la tabla de eventos, añadiendo un campo `version` que se incrementa en cada actualización. Cuando un usuario intenta actualizar un evento, se verifica que la versión no haya cambiado desde que se leyó, rechazando la actualización si otro usuario la ha modificado.

![Control de Versiones Optimista](PROYECTO_FINAL_IMAGENES/Control de Versiones Optimista.png)
*Figura: Código que implementa el control de versiones optimista en las actualizaciones*

![Código de Control de Concurrencia en EventController](PROYECTO_FINAL_IMAGENES/Código de Control de Concurrencia en EventController.png)
*Figura: Método _update_internal() completo con control de concurrencia*

#### Etapa 2: Sistema de Locks de Recursos

Se desarrolló un sistema de locks por recurso que permite bloquear recursos específicos (eventos, participantes) de forma independiente. Esto mejora la granularidad del control de concurrencia, permitiendo que diferentes usuarios trabajen en diferentes recursos simultáneamente sin interferencias.

![Código de ResourceLockManager](PROYECTO_FINAL_IMAGENES/Código de ResourceLockManager.png)
*Figura: Implementación completa de la clase ResourceLockManager*

#### Etapa 3: Bloqueos Transaccionales en Inscripciones

Se implementó el uso de SELECT FOR UPDATE en las operaciones de inscripción para prevenir condiciones de carrera cuando múltiples usuarios intentan inscribirse en un evento con capacidad limitada. Se configuró el nivel de aislamiento REPEATABLE READ para garantizar la consistencia de datos.

![SELECT FOR UPDATE en Inscripciones](PROYECTO_FINAL_IMAGENES/SELECT FOR UPDATE en Inscripciones.png)
*Figura: SELECT FOR UPDATE que previene condiciones de carrera en inscripciones*

![Código de Registro con Protección de Concurrencia](PROYECTO_FINAL_IMAGENES/Código de Registro con Protección de Concurrencia.png)
*Figura: Método _register_participant_internal() completo con todas las protecciones de concurrencia*

#### Etapa 4: Procesamiento Paralelo

Se implementó un sistema de procesamiento paralelo de suscripciones utilizando worker threads y colas thread-safe. Esto permite procesar múltiples inscripciones simultáneamente de forma segura, mejorando el rendimiento en operaciones masivas.

### 3.4. Fase 4: Pruebas, Documentación y Lanzamiento

**Fecha de Inicio:** [Fecha]  
**Fecha de Finalización:** [Fecha]

**Actividades:**
- ➢ Pruebas de Múltiples Usuarios Simultáneos: Se llevaron a cabo pruebas exhaustivas con múltiples instancias de la aplicación ejecutándose simultáneamente.
- ➢ Pruebas de Funcionalidad: Se realizaron pruebas exhaustivas de todas las funcionalidades de la aplicación.
- ➢ Documentación Técnica: Se creó documentación técnica completa del proyecto.
- ➢ Evaluación del Rendimiento: Se realizó una evaluación exhaustiva del rendimiento y la estabilidad de la aplicación.
- ➢ Preparación para Lanzamiento: Se preparó la aplicación para su uso en producción.

**Desarrollo:**

Durante esta fase final, se realizaron pruebas exhaustivas de todas las funcionalidades de la aplicación, con especial atención al sistema de concurrencia. Se probó la aplicación con múltiples usuarios simultáneos para verificar que no se producen conflictos ni pérdida de datos.

Además, se creó documentación técnica completa del proyecto, incluyendo la arquitectura, estructura del código, módulos principales, sistema de gestión de concurrencia y guías de instalación y uso.

---

## CONCLUSIONES

Concluyendo este trabajo, me siento extremadamente satisfecho con los resultados alcanzados en el desarrollo de la aplicación. Durante este proceso, he logrado cumplir con la gran mayoría de los requisitos establecidos inicialmente, demostrando así mi capacidad para planificar y ejecutar proyectos en plazo de manera efectiva.

A lo largo de este proyecto, he enfrentado desafíos significativos que me han permitido adquirir un conocimiento más profundo sobre el desarrollo de aplicaciones de escritorio y la gestión de concurrencia en sistemas multi-usuario. El desarrollo del sistema avanzado de gestión de concurrencia ha sido uno de los aspectos más complejos y enriquecedores del proyecto, permitiéndome profundizar en conceptos como control de versiones optimista, bloqueos transaccionales, procesamiento paralelo y gestión de recursos compartidos.

Mirando hacia el futuro, identifico varias áreas de mejora y nuevas funcionalidades que podrían agregarse a la aplicación para enriquecer la experiencia del usuario. Una de estas áreas es la implementación de notificaciones en tiempo real para informar a los usuarios sobre cambios en eventos o inscripciones. Además, considero importante implementar un sistema de roles más granular, permitiendo diferentes niveles de permisos según el tipo de usuario.

En cuanto a la interfaz de usuario, aunque Tkinter ha sido adecuado para este proyecto, considero que en futuras versiones podría explorarse el uso de frameworks más modernos como PyQt o Kivy para ofrecer una experiencia de usuario más rica y moderna.

En el transcurso de este proyecto, he adquirido una valiosa experiencia técnica y he desarrollado habilidades de resolución de problemas que sin duda me servirán tanto en mi carrera profesional como personal. A través de la planificación, el diseño y la implementación de esta aplicación, he fortalecido mi comprensión de los principios fundamentales del desarrollo de software, arquitectura de aplicaciones, gestión de bases de datos relacionales y resolución de problemas complejos de concurrencia.

Alguna de las lecciones aprendidas durante el desarrollo de este proyecto, son la importancia de una planificación detallada y un diseño robusto para evitar problemas durante las fases de desarrollo y pruebas, y la necesidad de una buena flexibilidad y adaptabilidad para manejar los imprevistos y ajustar el proyecto según el feedback recibido.

El desarrollo del sistema de gestión de concurrencia me ha permitido comprender en profundidad los desafíos que surgen cuando múltiples usuarios interactúan simultáneamente con los mismos datos, y las diferentes técnicas disponibles para resolver estos problemas de manera eficiente y segura.

En resumen, el desarrollo de esta aplicación ha sido una experiencia enriquecedora que me ha permitido aplicar y ampliar mis conocimientos en desarrollo de software. Aunque queda trabajo por hacer para alcanzar todas las metas propuestas, estoy seguro de que las habilidades y el conocimiento adquiridos durante este proyecto me servirán como base sólida para futuros desafíos en el campo de la informática.

---

## BIBLIOGRAFÍAS Y REFERENCIAS

### Bibliografía

- Python Software Foundation. (s.f.). Python.org. Obtenido de https://www.python.org/
- Python Software Foundation. (s.f.). Python Documentation. Obtenido de https://docs.python.org/3/
- Tkinter Documentation. (s.f.). Tkinter. Obtenido de https://docs.python.org/3/library/tkinter.html
- MySQL. (s.f.). MySQL Documentation. Obtenido de https://dev.mysql.com/doc/
- Oracle Corporation. (s.f.). MySQL Connector/Python. Obtenido de https://dev.mysql.com/doc/connector-python/en/
- bcrypt Developers. (s.f.). bcrypt. Obtenido de https://pypi.org/project/bcrypt/
- ReportLab. (s.f.). ReportLab Documentation. Obtenido de https://www.reportlab.com/docs/
- python-dotenv. (s.f.). python-dotenv. Obtenido de https://pypi.org/project/python-dotenv/
- GitHub. (s.f.). GitHub. Obtenido de https://github.com/
- Git. (s.f.). Git Documentation. Obtenido de https://git-scm.com/doc
- Stack Overflow. (s.f.). Stack Overflow. Obtenido de https://stackoverflow.com/
- Real Python. (s.f.). Real Python. Obtenido de https://realpython.com/
- GeeksforGeeks. (s.f.). GeeksforGeeks. Obtenido de https://www.geeksforgeeks.org/
- W3Schools. (s.f.). W3Schools Python Tutorial. Obtenido de https://www.w3schools.com/python/
- Visual Studio Code. (s.f.). Visual Studio Code. Obtenido de https://code.visualstudio.com/

---

**Módulo Proyecto Desarrollo de aplicaciones Multiplataforma**

**Gestor de Eventos Locales - Trabajo de Fin de Grado**

**Autor:** Martin Peñalva Artázcoz  
**Pamplona, 2024**

