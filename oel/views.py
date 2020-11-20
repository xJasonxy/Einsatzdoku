import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from doku.models import Einstellungen, Einsatz, Meldung, Ort
from oel.models import Einsatzstellen, Einheiten


@login_required()
def oel(request, einsatz_id):
    if request.method == "GET":
        return oel_response(request, einsatz_id)
    elif request.method == "POST":
        autor = request.user if request.user.is_authenticated else None
        try:
            einsatz = get_object_or_404(Einsatz, pk=einsatz_id)
            if 'Name' not in request.POST or request.POST['Name'] == "":
                if 'Einsatzstelle' not in request.POST:
                    raise Exception("Es muss ein Name eingegeben werden!")
            name = request.POST.get('Name', "")
            if 'neueEinsatzstelle' in request.POST:
                neue_einsatzstelle(request, einsatz_id)
            elif 'Einsatzstelle' in request.POST:
                e = Einsatzstellen.objects.filter(pk=request.POST['Einsatzstelle'])[0]
                if 'DONE' in request.POST:
                    e.Abgeschlossen = datetime.datetime.now()
                    e_ort = e.OrtFrei if e.OrtFrei else e.Ort.Langname
                    inhalt = "Einsatzstelle \"" + e.Name + ", " + e_ort + "\" abgearbeitet von \"" + e.Einheit.Name + "\""
                    m = Meldung(Inhalt=inhalt, Wichtig=False, Einsatz=einsatz, Autor=autor, Zug=None)
                    m.save()
                elif 'Anmerkungen' in request.POST:
                    e.Anmerkungen = request.POST['Anmerkungen']
            else:
                if Einheiten.objects.filter(Name=name).filter(Einsatz=einsatz).count() == 0:
                    e = Einheiten(Name=name, Einsatz=einsatz)
                else:
                    e = Einheiten.objects.filter(Name=name).filter(Einsatz=einsatz)[0]
            e.save()
        except Exception as err:
            error = str(err)
        return oel_response(request, einsatz_id, error)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def oel_response(request, einsatz_id, error=None):
    einstellungen = Einstellungen.objects.get_or_create(pk=1)[0]
    try:
        einsatz = Einsatz.objects.filter(Nummer=einsatz_id)[0]
    except:
        einsatz = None
    aktive_Einsaetze = Einsatz.objects.filter(Ende=None).filter(Training=einsatz.Training).order_by('-Nummer')
    autor = request.user if request.user.is_authenticated else None
    einsatzstellen = Einsatzstellen.objects.filter(Einsatz=einsatz_id)
    einheiten = Einheiten.objects.filter(Einsatz=einsatz_id)
    alle_Orte = Ort.objects.order_by('Kurzname')
    context = {
        'training': einsatz.Training,
        'einstellungen': einstellungen,
        'autor': autor,
        'einsatz': einsatz,
        'aktive_Einsaetze': aktive_Einsaetze,
        'einsatzstellen': einsatzstellen,
        'einheiten': einheiten,
        'alle_Orte': alle_Orte,
        'error': error,
    }
    return render(request, 'oel/oel.html', context)


@require_POST()
@login_required()
def neue_einheit(request, einsatz_id):
    return oel(request, einsatz_id)


@require_POST()
@login_required()
def neue_einsatzstelle(request, einsatz_id):
    ort_frei = None
    autor = request.user if request.user.is_authenticated else None
    einsatz = get_object_or_404(Einsatz, pk=einsatz_id)
    name = request.POST.get('Name', "")
    if name == "":
        raise Exception("Es muss ein Name eingegeben werden!")
    if 'Ort' not in request.POST:
        raise Exception("Es muss ein Ort ausgewählt werden!")
    ort = get_object_or_404(Ort, Kurzname=request.POST['Ort'])
    if ort.Kurzname == "ZZZ":
        ort_frei = request.POST.get('Freitext', "")
        if not ort_frei:
            raise Exception("Das Freitext Feld muss ausgefüllt sein!")
    anmerkungen = request.POST.get('Anmerkungen', "")
    e = Einsatzstellen(Ort=ort, OrtFrei=ort_frei, Einsatz=einsatz, Name=name, Anmerkungen=anmerkungen)
    e.save()
    e_ort = ort_frei if ort_frei else ort.Langname
    inhalt = "Neue Einsatzstelle: \"" + name + ", " + e_ort + "\""
    m = Meldung(Inhalt=inhalt, Wichtig=False, Einsatz=einsatz, Autor=autor, Zug=None)
    m.save()
    return HttpResponseRedirect(reverse('oel:oel', args=[einsatz_id]))


@require_POST()
@login_required()
def einheit_zuweisen(request, einsatz_id, einsatzstelle):
    autor = request.user if request.user.is_authenticated else None
    einheit = get_object_or_404(Einheiten, Name=request.POST['einheit'])
    einsatz = get_object_or_404(Einsatz, pk=einsatz_id)
    e = get_object_or_404(Einsatzstellen, pk=einsatzstelle)
    e.Einheit = einheit
    e.Zugewiesen = datetime.datetime.now()
    e_ort = e.OrtFrei if e.OrtFrei else e.Ort.Langname
    inhalt = "Einsatzstelle \"" + e.Name + ", " + e_ort + "\" übernommen von \"" + e.Einheit.Name + "\""
    m = Meldung(Inhalt=inhalt, Wichtig=False, Einsatz=einsatz, Autor=autor, Zug=None)
    m.save()
    return HttpResponseRedirect(reverse('oel:oel', args=[einsatz_id]))


@require_POST()
@login_required()
def einsatzstelle_erledigt(request, einsatz_id):
    return oel_response(request, einsatz_id, error)


@require_POST()
@login_required()
def neue_information(request, einsatz_id):
    return oel_response(request, einsatz_id, error)
