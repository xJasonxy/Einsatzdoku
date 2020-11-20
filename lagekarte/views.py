import os

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404

from doku.models import Lagekarte, Einstellungen, Einsatz


def lagekarte(request, einsatz_id):
    einsatz = get_object_or_404(Einsatz, pk=einsatz_id)
    if request.method == "POST":
        if request.POST['image'] and request.POST['canvas_data']:
            karte = Lagekarte(Bild=request.POST['image'], Data=request.POST['canvas_data'], Einsatz=einsatz)
            karte.save()
            return HttpResponse("Success")
            # return HttpResponseRedirect(reverse('doku:lagekarte', args=[einsatz_id]))
        else:
            return HttpResponseServerError
    else:
        einstellungen = Einstellungen.objects.get_or_create(pk=1)[0]
        aktive_Einsaetze = Einsatz.objects.filter(Ende=None).filter(Training=einsatz.Training).order_by('-Nummer')
        lagekarten = Lagekarte.objects.filter(Einsatz=einsatz_id).order_by('-Erstellt')
        autor = request.user if request.user.is_authenticated else None
        icons = get_icons()
        context = {
            'training': einsatz.Training,
            'einstellungen': einstellungen,
            'autor': autor,
            'einsatz': einsatz,
            'lagekarten': lagekarten,
            'aktive_Einsaetze': aktive_Einsaetze,
            'icons': icons,
        }
        return render(request, 'lagekarte/lagekarte.html', context)

def get_icons():
    icons = []
    for icon in os.listdir("doku/static/doku/icons"):
        try:
            order = int(icon.split("_")[0])
            name = icon.split("_", 1)[1].split(".")[0]
        except:
            order = 999
            try:
                name = icon.split(".")[0]
            except:
                name = icon
        icons.append({
            'path': icon,
            'name': name,
            'order': order
        })
    icons.sort(key=lambda i: (i['order'], i['name']))
    return icons
