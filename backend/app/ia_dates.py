import openai
import json
from app.chunks import generate_chunks
from app.event_validator import is_event_valid
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_events(text):
    def get_events_from_chunk(text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a software that only returns output",
                },
                {
                    "role": "system",
                    "content": """Parse the following text and return all the names of events with its dates in a JSON format {name: <name>, date:<date:ISO8601>}. Events without a date or that do not correspond to an evaluation, shall be discarded""",
                },
                {
                    "role": "user",
                    "content": """La condici´ on de aprobaci´ on es NF≥3,95.
Las fechas de las interrogaciones y el examen son las siguientes:
I1 : viernes 8 de septiembre a las 17:30 hrs
I2 : viernes 3 de noviembre a las 17:30 hrs
Examen : jueves 7 de diciembre a las 08:20 hrs
Las fechas de publicaci´ on del enunciado y entrega de las tareas aparecen en la siguiente tabla:""",
                },
                {
                    "role": "assistant",
                    "content": """[{"name": "I1", "date": "2023-09-08T20:30:00.000Z"}, {"name": "I2", "date": "2023-11-03T20:30:00.000Z"}, {"name": "Examen", "date": "2023-12-07T11:20:00.000Z"}]""",
                },
                {
                    "role": "user",
                    "content": """Evaluaciones.
Prueba 1: Jueves 25 de Mayo, 14:00 - 15:20. 25%
Examen : Martes 4 de Julio, 08:30 - 10:30. 25%
Realizaremos dos pruebas durante el semestre""",
                },
                {
                    "role": "assistant",
                    "content": """[{"name": "Prueba 1", "date": "2023-05-25T18:00:00.000Z"}, {"name": "Examen", "date": "2023-07-04T12:30:00.000Z"}]""",
                },
                {
                    "role": "user",
                    "content": """El objetivo del curso es introducir al alumno a las t´ecnica b´asicas y algunas t´ecnicas avanzadas tanto para
el dise˜no como para el an´alisis de la complejidad computacional de un algoritmo""",
                },
                {
                    "role": "assistant",
                    "content": """[""]""",
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )
        try:
            json_text = response["choices"][0]["message"]["content"]
            print(json_text)
            data = json.loads(json_text)
            return data
        except:
            print(response)
            raise Exception("The IA module could not decode the events")

    chunks = generate_chunks(text)

    events = []
    for chunk in chunks:
        events.extend(get_events_from_chunk(chunk))

    valid_events = [event for event in events if is_event_valid(event)]
    return valid_events

# Funcion que retorna el nombre del ramo
def get_course_name(text):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a software that only returns output",
                 },
                 {
                     "role": "system",
                     "content": "Parse the following syllabus and return the name of the course"
                },
                {
                    "role": "user",
                    "content": """Pontificia Universidad Católica de Chile
Escuela de Administración
EAA325B OPCIONES Y FUTUROS
PROGRAMA CURSO1
Segundo Semestre 2023 Profesor: David Buchuk (dbuchuk@uc.cl)
(Oficina #411 – Escuela de Administración)
Cátedras: L-W:3 (Sala C504)
Ayudantías: L:2 (Sala AE003) Ayudantes: Gonzalo Lanis (gonzalo.lanis@uc.cl)
Oscar Herrera (olherrera@uc.cl)
1. Objetivos del Curso
Al finalizar este curso el alumno debiera conocer las características y potenciales usos de los
principales derivados financieros (futuros, forwards, opciones y swaps) y herramientas de administración
de riesgos financieros. El énfasis estará en la valoración de estos instrumentos y en el
análisis de estrategias para la administración de riesgos desde el punto de vista de una corporación
o una institución financiera.
2. Clases, Ayudantías y Atención de Alumnos
Clases son en formato presencial los días lunes y miércoles en el módulo 3 (11:00 a 12:10) en
la sala C504.
Las ayudantías son los días lunes en el módulo 2 (9:40 a 10:50) en la sala AE003.
Atención de alumnos es los días miércoles de 14:00 a 17:00 a través de zoom o presencial
agendando con antelación.
Preguntas que sean de interés de todo el curso deben ser hechas en el foro del curso en Canvas.
El profesor se reserva el derecho de postear en el foro este tipo de preguntas hechas por correo
electrónico.
3. Pre"""
                },
                {
                    "role": "assistant",
                    "content": """["Opciones y futuros"]"""
                },
                {
                    "role": "user",
                    "content": """Pontificia Universidad Cat´olica de Chile
Facultad de Econom´ıa y Administraci´on
Instituto de Econom´ıa
Macroeconometria Aplicada
EAE3102
Primer Semestre 2023
Informaci´on del Curso
Profesores: Javier Tur´en (jturen@uc.cl)
Ayudantes: Francisca Kegevic (fkegevic@uc.cl) y ...
Clases: Lunes y Mi´ercoles (CS201), m´odulo 2 (10:00 a 11:20).
Ayudant´ıas: Lunes (AE102), m´odulo 5 (15:30 a 16:50).
Atenci´on de alumnos: Fijar d´ıa y hora por email.
Descripci´on del Curso
Este curso cubrir´a conceptos y t´ecnicas de econometr´ıa avanzada de series de tiempo, intentando
seguir siempre un enfoque aplicado. En la primera parte del curso, se revisar´a en profundidad
t´ecnicas econom´etricas avanzadas de modelos de series de tiempo univariadas, predicci´on, ciclos
econ´omicos y filtros. La segunda parte, se enfocar´a en modelos multivariados y en modelos frecuentemente
utilizados por la literatura como por ejemplo Local Projection Models o VARs. El
objetivo del curso es que el alumno se familiarice con macroeconometr´ıa avanzada, siguiendo un
enfoque m´as pr´actico. La materia se complementar´a con an´alisis y discusi´on de papers, intentando
replicar algunos resultados cuando sea posible. Se asumir´a que el alumno ya posee conocimientos
b´asicos de Stata.
Contenidos
1."""
                },
                {
                    "role": "assistant",
                    "content": """["Macroeconometria aplicada"]"""
                },
                {
                    "role": "user",
                    "content": """# Plataforma de apoyo : Canvas, https://github.com/darroyue/IIC2283
# Objetivo
# El objetivo del curso es introducir al alumno a las t´ ecnica b´ asicas y algunas t´ ecnicas avanzadas tanto para
# el dise˜ no como para el an´ alisis de la complejidad computacional de un algoritmo. Se dar´ a especial ´ enfasis a
# la comprensi´ on del modelo computacional sobre el cual se dise˜ na y analiza un algoritmo. Adem´ as, para cada
# una de las t´ ecnicas mostradas se estudiar´ a algunos algoritmos que permiten entender su potencial, poniendo
# ´ enfasis en la variedad e importancia de las ´ areas donde estos algoritmos son utilizados.
# Evaluaci´ on
# La evaluaci´ on del curso estar´ a basada en dos interrogaciones, un examen y tres tareas. Las interrogaciones
# y el examen estar´ an orientadas a medir los conceptos fundamentales ense˜ nados en el curso. En las tareas,
# los alumnos programaran en Python algoritmos para resolver distintos tipos de problemas, donde ser´ an
# utilizadas las t´ ecnicas aprendidas en el curso.
# Suponiendo que las notas en las interrogaciones son I1eI2, la nota del examen es E, y las notas en las tareas
# 1
# sonT1,T2yT3, la nota final del curso se calcula de la siguiente forma:
# NF =1
# 2·T1+T2+T3
# 3
# +1
# 2·I1+I2+E
# 3
# .
# La condici´ on de aprobaci´ on es NF≥3,95.
# Las fechas de las interrogaciones y el examen son las siguientes:
# I1 : viernes 8 de septiembre a las 17"""
                },
                {
                    "role": "assistant",
                    "content": "[]"
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
    )
    try:
        json_text = response["choices"][0]["message"]["content"]
        data = json.loads(json_text)
        return data
    except:
        print(response)
        raise Exception("The IA module could not decode the course name")


if __name__ == "__main__":
    from pprint import pprint

    query = """PONTIFICIA UNIVERSIDAD CATOLICA DE CHILE
# ESCUELA DE INGENIERIA
# DEPARTAMENTO DE CIENCIA DE LA COMPUTACION
# Dise˜ no y An´ alisis de Algoritmos - IIC2283
# Programa de Curso
# 2dosemestre - 2023
# Horario c´ atedra : lunes y mi´ ercoles m´ odulo 5, sala B13
# Horario ayudant´ ıa : viernes m´ odulo 5, sala B13
# Profesor : Diego Arroyuelo ( diego.arroyuelo@uc.cl )
# Ayudantes : Ernesto Ayala ( ernesto.ayala@uc.cl ), Mauricio Cari
# (mauricio.cari@uc.cl ), Felipe Guzm´ an ( faguzman2@uc.cl ), Ricar-
# do Rodriguez ( rrrodriguez@uc.cl ), Amaranta Salas ( afsalas@uc.cl ),
# Tom´ as Vergara ( tomvergara@uc.cl ).
# Plataforma de apoyo : Canvas, https://github.com/darroyue/IIC2283
# Objetivo
# El objetivo del curso es introducir al alumno a las t´ ecnica b´ asicas y algunas t´ ecnicas avanzadas tanto para
# el dise˜ no como para el an´ alisis de la complejidad computacional de un algoritmo. Se dar´ a especial ´ enfasis a
# la comprensi´ on del modelo computacional sobre el cual se dise˜ na y analiza un algoritmo. Adem´ as, para cada
# una de las t´ ecnicas mostradas se estudiar´ a algunos algoritmos que permiten entender su potencial, poniendo
# ´ enfasis en la variedad e importancia de las ´ areas donde estos algoritmos son utilizados.
# Evaluaci´ on
# La evaluaci´ on del curso estar´ a basada en dos interrogaciones, un examen y tres tareas. Las interrogaciones
# y el examen estar´ an orientadas a medir los conceptos fundamentales ense˜ nados en el curso. En las tareas,
# los alumnos programaran en Python algoritmos para resolver distintos tipos de problemas, donde ser´ an
# utilizadas las t´ ecnicas aprendidas en el curso.
# Suponiendo que las notas en las interrogaciones son I1eI2, la nota del examen es E, y las notas en las tareas
# 1
# sonT1,T2yT3, la nota final del curso se calcula de la siguiente forma:
# NF =1
# 2·T1+T2+T3
# 3
# +1
# 2·I1+I2+E
# 3
# .
# La condici´ on de aprobaci´ on es NF≥3,95.
# Las fechas de las interrogaciones y el examen son las siguientes:
# I1 : viernes 8 de septiembre a las 17:30 hrs
# I2 : viernes 3 de noviembre a las 17:30 hrs
# Examen : jueves 7 de diciembre a las 08:20 hrs
# Las fechas de publicaci´ on del enunciado y entrega de las tareas aparecen en la siguiente tabla:
# Publicaci´ on enunciado Entrega
# Tarea 1 Mi´ ercoles 13 de septiembre Martes 26 de septiembre
# Tarea 2 Mi´ ercoles 11 de octubre Viernes 27 de octubre
# Tarea 3 Lunes 6 de noviembre Lunes 20 de noviembre
# La entrega ser´ a en la fecha estipulada hasta las 23:59 horas. La publicaci´ on del enunciado ser´ a durante la
# ma˜ nana de la fecha estipulada.
# Adicionalmente, cada estudiante puede acceder a realizar entregas atrasadas para las tareas obteniendo un
# descuento sobre su nota como penalizaci´ on. El descuento diasociado a la i-´ esima tarea es
# di=
# 
# 0 si entrega sin atraso,
# 0,5 si entrega con menos de 24 horas de atraso,
# 1,5 si entrega con m´ as de 24 pero menos de 48 horas de atraso,
# 3,0 si entrega con m´ as de 48 pero menos de 72 horas de atraso,
# 7,0 en otro caso.
# As´ ı, siendo T′
# ila nota correspondiente seg´ un la r´ ubrica de la i-´ esima tarea, la nota Tide la i-´ esima tarea se
# calcula como
# Ti= m´ ax {T′
# i−di,1,0}
# Dicho eso, cada estudiante cuenta con la opci´ on de utilizar un cup´ on de extensi´ on de plazo para la entrega
# de una tarea. Este cup´ on se puede utilizar s´ olo una vez durante el semestre y permitir´ a extender el plazo de
# entrega de una tarea sin necesidad de una justificaci´ on. La extensi´ on permite al estudiante entregar hasta
# 72 horas despu´ es de la entrega original, anulando el descuento por atraso.
# Vale mencionar que la recepci´ on de entregas atrasadas es un beneficio excepcional para el estudiante, por lo
# que las horas de atraso ser´ an contabilizadas incluso si es que los d´ ıas posteriores a la entrega original son
# feriados (por ejemplo si la entrega es un jueves, como m´ aximo se puede entregar atrasado hasta el siguiente
# domingo). Fuera del uso del cup´ on de extensi´ on, no se har´ an excepciones sobre estos plazos.
# 2
# Contenido
# 1. Introducci´ on
# 2. An´ alisis de la eficiencia de un algoritmo
# a) Notaciones asint´ oticas
# b) Ecuaciones de recurrencia: cambio de variables, inducci´ on constructiva, teorema maestro
# c) An´ alisis de la complejidad de un algoritmo en el peor caso
# 3. An´ alisis de la eficiencia de un algoritmo m´ as all´ a del peor caso: an´ alisis de caso promedio
# 4. T´ ecnicas para demostrar cotas inferiores: mejor estrategia del adversario, ´ arboles de decisi´ on y reduc-
# ciones
# 5. T´ ecnicas fundamentales de dise˜ no de algoritmos
# a) Dividir para conquistar
# b) Programaci´ on din´ amica
# c) Algoritmos codiciosos
# 6. Transformaciones de dominio
# a) Representaci´ on, evaluaci´ on e interpolaci´ on de polinomios y la transformada r´ apida de Fourier
# 7. Algoritmos aleatorizados
# a) Algoritmos de Monte Carlo: igualdad de polinomios
# b) Algoritmos de Las Vegas: c´ alculo de la mediana de una lista
# c) Hashing universal
# 8. Algoritmos en teor´ ıa de n´ umeros
# a) Aritm´ etica modular
# b) Algoritmos b´ asicos: exponenciaci´ on r´ apida, c´ alculo del m´ aximo com´ un divisor, el algoritmo de
# Euclides extendido y el c´ alculo del inverso modular
# c) Un algoritmo de Monte Carlo para la verificaci´ on de primalidad
# Bibliograf´ ıa
# 1. Transparencias de clases.
# 2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest y Clifford Stein. Introduction to Algorithms ,
# 3aedici´ on. MIT Press, 2009.
# 3. Gilles Brassard y Paul Bratley. Algorithmics: Theory and Practice , 1aedici´ on. Prentice Hall, 1988.
# 4. Rajeev Motwani y Prabhakar Raghavan. Randomized Algorithms , 1aedici´ on, 1995.
# 5. Jon Kleinberg y ´Eva Tardos. Algorithm Design , 1aedici´ on. Pearson, 2005.
# 6. Michael Mitzenmacher y Eli Upfal. Probability and Computing: Randomized Algorithms and Probabi-
# listic Analysis . Cambridge University Press, 2005."""

    dates = get_events(query)
    pprint(dates)
