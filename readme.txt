===================================
MOTOR
===================================


Motor es un sistema de reservas hoteleras pensado para operar a 
través de internet orientado a hoteles y cadenas hoteleras.

A diferencia de otros sistemas parecidos MOTOR es:

	* De código abierto.
	* Desarrollado en Python, lo que implica una gran versatilidad
	  legibilidad del código y capacidad de adaptación
	* Pensado para que cada empresa esté en una base de datos
 	  independiente.

Instalación en desarrollo
=========================

Crear un entorno virtual, previamente es necesario tener isntalado virtualenv y virtualenvwrapper


	mkvirtualenv motor --no-site-packages

	workon motor

	pip install -r devel_requirements.txt
