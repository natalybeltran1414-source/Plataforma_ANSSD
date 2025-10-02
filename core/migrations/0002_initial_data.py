from django.db import migrations

def crear_datos_iniciales(apps, schema_editor):
    Modulo = apps.get_model('core', 'Modulo')
    Pregunta = apps.get_model('core', 'Pregunta')

    # Crear módulos
    modulos = [
        ('Uso seguro de internet', 'Aprende a proteger tus datos en línea.'),
        ('Manejo básico de herramientas ofimáticas', 'Domina Word, Excel y PowerPoint.'),
        ('Comunicación digital', 'Mejora tus habilidades en correo y videollamadas.')
    ]
    modulo_objs = []
    for nombre, descripcion in modulos:
        modulo = Modulo.objects.create(nombre=nombre, descripcion=descripcion)
        modulo_objs.append(modulo)

    # Preguntas para Uso seguro de internet
    Pregunta.objects.create(
        modulo=modulo_objs[0],
        texto='¿Cuál es la mejor práctica para crear una contraseña segura?',
        opcion_a='Usar tu nombre',
        opcion_b='Combinar letras, números y símbolos',
        opcion_c='Usar una sola palabra',
        opcion_d='Usar la misma contraseña para todo',
        respuesta_correcta='B'
    )
    Pregunta.objects.create(
        modulo=modulo_objs[0],
        texto='¿Qué es el phishing?',
        opcion_a='Un tipo de software antivirus',
        opcion_b='Un ataque para robar información personal',
        opcion_c='Una técnica de programación',
        opcion_d='Un protocolo de seguridad',
        respuesta_correcta='B'
    )
    Pregunta.objects.create(
        modulo=modulo_objs[0],
        texto='¿Qué debes hacer si recibes un correo sospechoso?',
        opcion_a='Hacer clic en los enlaces para verificar',
        opcion_b='Ignorarlo o reportarlo',
        opcion_c='Responder con tus datos personales',
        opcion_d='Descargar los adjuntos',
        respuesta_correcta='B'
    )

    # Preguntas para Manejo básico de herramientas ofimáticas
    Pregunta.objects.create(
        modulo=modulo_objs[1],
        texto='¿Qué fórmula en Excel suma un rango de celdas?',
        opcion_a='=SUMA(A1:A10)',
        opcion_b='=PROMEDIO(A1:A10)',
        opcion_c='=CONTAR(A1:A10)',
        opcion_d='=MAX(A1:A10)',
        respuesta_correcta='A'
    )
    Pregunta.objects.create(
        modulo=modulo_objs[1],
        texto='¿Cómo insertar una tabla en Word?',
        opcion_a='Usar la pestaña "Insertar" y seleccionar "Tabla"',
        opcion_b='Escribir "tabla" y presionar Enter',
        opcion_c='Usar la barra de herramientas rápida',
        opcion_d='Copiar y pegar desde Excel',
        respuesta_correcta='A'
    )

    # Preguntas para Comunicación digital
    Pregunta.objects.create(
        modulo=modulo_objs[2],
        texto='¿Qué es una buena práctica al enviar un correo profesional?',
        opcion_a='Usar emojis en el asunto',
        opcion_b='Redactar un asunto claro y conciso',
        opcion_c='Escribir todo en mayúsculas',
        opcion_d='No incluir saludo',
        respuesta_correcta='B'
    )
    Pregunta.objects.create(
        modulo=modulo_objs[2],
        texto='¿Cuál es una herramienta común para videollamadas?',
        opcion_a='Microsoft Word',
        opcion_b='Zoom',
        opcion_c='Notepad',
        opcion_d='Paint',
        respuesta_correcta='B'
    )

class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RunPython(crear_datos_iniciales)]