from demandes.forms import DemandeVirementForm
from demandes.models import DemandeCaution, DemandeVirement
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from num2words import num2words

from weasyprint import HTML




from .forms import DemandeCautionForm
from django.shortcuts import render, get_object_or_404, redirect



@login_required
def demande_cautions_list(request):
    search = request.GET.get('search')
    demande_cautions = DemandeCaution.objects.all().order_by("-id")
    if search:
        demande_cautions = demande_cautions.filter(numero_marche__icontains=search)
    paginator = Paginator(demande_cautions, 7)
    page_number = request.GET.get('page')
    demande_cautions = paginator.get_page(page_number)

    return render(request, 'demande_caution/list.html', {'demande_cautions': demande_cautions, 'search': search})
@login_required
@permission_required("demandes.add_demandecaution")
def create_demande_caution(request):
    form=DemandeCautionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Demande de caution successfully created")
            return redirect("demandes-caution-list")

    return render(request,"demande_caution/create.html",{"form":form})
@login_required
@permission_required("demandes.change_demandecaution")
def edit_demande_caution(request, demande_caution_id):
    demande_caution = get_object_or_404(DemandeCaution, id=demande_caution_id)
    form = DemandeCautionForm(request.POST or None, instance=demande_caution)
    if form.is_valid():
            form.save()
            messages.success(request,"Demande de caution successfully updated")
            return redirect('demandes-caution-list')


    return render(request, 'demande_caution/create.html', {'form': form})
@login_required
@permission_required("demandes.delete_demandecaution")
def delete_demande_caution(request, demande_caution_id):
    demande_caution = get_object_or_404(DemandeCaution, id=demande_caution_id)
    if request.method == 'POST':
        demande_caution.delete()
        messages.success(request, "Demande de caution successfully deleted")
    return redirect('demandes-caution-list')
@login_required
def demande_caution_pdf(request,demande_caution_id):
    demande_caution = get_object_or_404(DemandeCaution, id=demande_caution_id)
    if demande_caution.type_caution == "Retenue de garantie":
        html_string = render_to_string('demande_caution/pdf(retenue).html', {
            'demande_caution': demande_caution,
        }, request)
    elif demande_caution.type_caution == "Définitive":
        html_string = render_to_string('demande_caution/pdf(definitive).html', {
            'demande_caution': demande_caution,
        }, request)
    else:
        html_string = render_to_string('demande_caution/pdf(provisoir).html', {
            'demande_caution': demande_caution,
        }, request)



    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    pdf = html.write_pdf()


    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=demande_caution_{demande_caution.type_caution}N°{demande_caution.numero_marche}.pdf'
    return response


@login_required
def demande_virement_list(request):
    search = request.GET.get('search')
    demandes_virement = DemandeVirement.objects.all().order_by("-id")
    if search:
        demandes_virement = demandes_virement.filter(titulaire__icontains=search)
    paginator = Paginator(demandes_virement, 10)
    page_number = request.GET.get('page')
    demandes_virement = paginator.get_page(page_number)

    return render(request, 'demande_virement/list.html', {'demandes_virement': demandes_virement, 'search': search})

@login_required
@permission_required("demandes.add_demandevirement")
def create_demande_virement(request):
    form=DemandeVirementForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Demande de virement successfully created")
            return redirect("demande-virement-list")

    return render(request,"demande_virement/create.html",{"form":form})

@login_required
@permission_required("demandes.change_demandevirement")
def edit_demande_virement(request, demande_virement_id):
    demande_virement = get_object_or_404(DemandeVirement, id=demande_virement_id)
    form = DemandeVirementForm(request.POST or None, instance=demande_virement)
    if form.is_valid():
        form.save()
        messages.success(request,"Demande de virement successfully updated")
        return redirect('demande-virement-list')


    return render(request, 'demande_virement/create.html', {'form': form})


@login_required
@permission_required("demandes.delete_demandevirement")
def delete_demande_virement(request, demande_virement_id):
    demande_caution = get_object_or_404(DemandeVirement, id=demande_virement_id)
    if request.method == 'POST':
        demande_caution.delete()
        messages.success(request, "Demande de virement successfully deleted")
    return redirect('demande-virement-list')

@login_required
def demande_virement_pdf(request,demande_virement_id):
    demande_virement = get_object_or_404(DemandeVirement, id=demande_virement_id)

    html_string = render_to_string('demande_virement/pdf.html', {
            'demande_virement': demande_virement,
        }, request)



    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    pdf = html.write_pdf()


    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=demande_virement_banquaire:{demande_virement.titulaire}.pdf'
    return response