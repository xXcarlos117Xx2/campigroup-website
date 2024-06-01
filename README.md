# Campigroup website

Este proyecto es una web para Campigroup. La idea principal es que, de manera pública puedas ver los estados de los servidores de juegos abiertos. Tambien puedes ver la información necesaria para acceder al servidor, sea la IP, mods etc.

## Como iniciar el proyecto
1. Abrir un codespace (recomendado) o un local con sus requisitos (`requirements.txt` en la raiz del proyecto)
2. Instalar dependencias con `npm install`
3. Instalar dependencias con `pipenv install`
4. Configurar el `.env` tal y como indica `.env.example`
5. Iniciar primero el Backend `pipenv run start`
6. Iniciar el Frontend `npm run start`

## Características

- Mobile first
- Implementado con TailwindCSS
- Información de cada juego independientemente
- Cajón de comentarios para usuarios registrados
- Modal para login y register
- Dos temas: claro y oscuro

## Tecnologías utilizadas

- Flask
- React
- TailwindCSS
- flask_jwt_extended
- flask_mail

## Estructura de Directorios

```
src
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── commands.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
└── front
    ├── img
    ├── js 
    │   ├── component 
    │   ├── pages 
    │   └── store 
    │       ├── index.js 
    │       └── layout.js 
    └── styles 
        ├── home.css  
        └── index.css  
├─ app.py  
├─ wsgi.py  
├─ .env.example
└─ .env
```
## Contribución

Las contribuciones son bienvenidas. Para cualquier cambio importante, por favor abra un problema primero para discutir lo que le gustaría cambiar.

This template was built as part of the 4Geeks Academy [Coding Bootcamp](https://4geeksacademy.com/us/coding-bootcamp) by [Alejandro Sanchez](https://twitter.com/alesanchezr) and many other contributors. Find out more about our [Full Stack Developer Course](https://4geeksacademy.com/us/coding-bootcamps/part-time-full-stack-developer), and [Data Science Bootcamp](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning).

You can find other templates and resources like this at the [school github page](https://github.com/4geeksacademy/).

## Licencia
Este repositorio cuenta con una [licencia MIT](LICENSE)
