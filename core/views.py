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
            for p in preguntas:
                respuesta = request.POST.get(f'pregunta_{p.id}')
                if respuesta == p.respuesta_correcta:
                    puntaje += 1
            if puntaje < len(preguntas) / 2:
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
    contenido = f"Contenido para {modulo.nombre}: Aprende sobre esto..."
    if request.method == 'POST':
        progreso, _ = Progreso.objects.get_or_create(user=request.user, modulo=modulo)
        progreso.completado = True
        progreso.save()
        return redirect('progreso')
    return render(request, 'core/modulo.html', {'modulo': modulo, 'contenido': contenido})

@login_required
def tutor(request):
    respuestas_predefinidas = {
        '¿Qué es seguridad digital?': 'Es el conjunto de prácticas para proteger información en línea.',
        '¿Cómo usar Excel?': 'Empieza con fórmulas básicas como =SUMA().',
    }
    preguntas = list(respuestas_predefinidas.keys())
    if request.method == 'POST':
        pregunta = request.POST.get('pregunta')
        respuesta = respuestas_predefinidas.get(pregunta, 'Lo siento, no tengo respuesta para eso.')
        return render(request, 'core/tutor.html', {'preguntas': preguntas, 'respuesta': respuesta})
    return render(request, 'core/tutor.html', {'preguntas': preguntas})

@login_required
def progreso(request):
    progresos = Progreso.objects.filter(user=request.user)
    
    # Obtener brechas de la sesión
    brechas_ids = request.session.get('brechas', [])
    brechas = Modulo.objects.filter(id__in=brechas_ids)

    # Contar módulos completados y total de módulos
    completados = progresos.filter(completado=True).count()
    total = Modulo.objects.count()

    # CORRECCIÓN: Calcular el porcentaje en la vista
    if total > 0:
        # Se calcula el porcentaje y se redondea a un entero.
        porcentaje_real = round((completados / total) * 100)
    else:
        porcentaje_real = 0

    context = {
        'progresos': progresos, 
        'brechas': brechas, 
        'completados': completados, 
        'total': total,
        'porcentaje_real': porcentaje_real  # Enviamos el valor calculado
    }

    return render(request, 'core/progreso.html', context)

@login_required
def generar_certificado(request):
    if Progreso.objects.filter(user=request.user, completado=False).exists():
        return redirect('progreso')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Certificado para {request.user.username}")
    p.drawString(100, 780, "Ha completado todas las competencias digitales.")
    p.save()
    return response