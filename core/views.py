from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, Modulo, Pregunta, Progreso
from .forms import PerfilForm
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if form.is_valid() and perfil_form.is_valid():
            user = form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            login(request, user)
            return redirect('perfil')
    else:
        form = UserCreationForm()
        perfil_form = PerfilForm()
    return render(request, 'core/register.html', {'form': form, 'perfil_form': perfil_form})

@login_required
def perfil(request):
    return render(request, 'core/perfil.html', {'perfil': request.user.perfil})

@login_required
def diagnostico(request):
    modulos = Modulo.objects.all()
    preguntas_por_modulo = {modulo: Pregunta.objects.filter(modulo=modulo) for modulo in modulos}
    if request.method == 'POST':
        brechas = []
        for modulo in modulos:
            preguntas = Pregunta.objects.filter(modulo=modulo)
            puntaje = 0
            total_preguntas = len(preguntas)
            for pregunta in preguntas:
                respuesta = request.POST.get(f'pregunta_{pregunta.id}')
                if respuesta == pregunta.respuesta_correcta:
                    puntaje += 1
            porcentaje = (puntaje / total_preguntas) * 100 if total_preguntas > 0 else 0
            if porcentaje < 50:  # Umbral del 50% para detectar brechas
                brechas.append(modulo)
            progreso, _ = Progreso.objects.get_or_create(user=request.user, modulo=modulo)
            progreso.puntaje = puntaje
            progreso.save()
        request.session['brechas'] = [m.id for m in brechas]
        return redirect('progreso')
    return render(request, 'core/diagnostico.html', {'preguntas_por_modulo': preguntas_por_modulo})

@login_required
def modulo(request, modulo_id):
    modulo = Modulo.objects.get(id=modulo_id)
    contenido = {
        'Uso seguro de internet': 'Aprende a proteger tus datos en línea, usar contraseñas seguras y detectar phishing.',
        'Manejo básico de herramientas ofimáticas': 'Domina herramientas como Word, Excel y PowerPoint para el trabajo diario.',
        'Comunicación digital': 'Mejora tus habilidades en correo electrónico, videollamadas y plataformas colaborativas.'
    }.get(modulo.nombre, 'Contenido en desarrollo...')
    if request.method == 'POST':
        progreso = Progreso.objects.get(user=request.user, modulo=modulo)
        progreso.completado = True
        progreso.save()
        return redirect('progreso')
    return render(request, 'core/modulo.html', {'modulo': modulo, 'contenido': contenido})

@login_required
def tutor(request):
    respuestas_predefinidas = {
        '¿Qué es seguridad digital?': 'Es el conjunto de prácticas y herramientas para proteger información en línea, como contraseñas seguras y evitar phishing.',
        '¿Cómo usar Excel?': 'Empieza con fórmulas básicas como =SUMA(A1:A10) para sumar celdas.',
        '¿Cómo redactar un correo profesional?': 'Usa un saludo formal, estructura clara (introducción, cuerpo, cierre) y revisa la ortografía.',
    }
    respuesta = None
    if request.method == 'POST':
        pregunta = request.POST.get('pregunta')
        respuesta = respuestas_predefinidas.get(pregunta, 'Lo siento, no tengo una respuesta para esa pregunta. Intenta con otra.')
    return render(request, 'core/tutor.html', {'respuesta': respuesta, 'preguntas': respuestas_predefinidas.keys()})

@login_required
def progreso(request):
    progresos = Progreso.objects.filter(user=request.user)
    brechas = Modulo.objects.filter(id__in=request.session.get('brechas', []))
    completados = progresos.filter(completado=True).count()
    total = Modulo.objects.count()
    return render(request, 'core/progreso.html', {
        'progresos': progresos,
        'brechas': brechas,
        'completados': completados,
        'total': total
    })

@login_required
def generar_certificado(request):
    if Progreso.objects.filter(user=request.user, completado=False).exists():
        return redirect('progreso')  # No listo para certificado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{request.user.username}.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 16)
    p.drawString(100, 800, f"Certificado de Competencias Digitales")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Otorgado a: {request.user.perfil.nombre}")
    p.drawString(100, 760, f"Por completar todos los módulos de capacitación.")
    p.drawString(100, 740, f"Fecha: {request.user.date_joined.strftime('%d/%m/%Y')}")
    p.showPage()
    p.save()
    return response