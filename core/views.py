from django.contrib import messages
from django.shortcuts import redirect, render
from io import BytesIO
from django.shortcuts import render, HttpResponse, Http404
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from .fusioncharts import FusionCharts
from xhtml2pdf import pisa
# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout_then_login

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

@login_required
def ImprimePdf(request, id):
    texts = FeeRequest.objects.get(id=id)
    
    context = {
        'texts': texts,
    }

    return render_to_pdf('core/pdf_template.html', context)


@login_required
def rapport_mensuel(request):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = { 
        "caption": "Montant par Code activité",
            "subCaption": "",
            "xAxisName": "Code activité",
            "yAxisName": "Montant (en XOF)",
            "numberPrefix": "",
            "theme": "umber"
        }
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list
    for key in FeeRequest.objects.filter(level2=True).order_by('activity'):
        data={}
        data['label'] = key.activity
        data['value'] = key.get_total_price
        dataSource['data'].append(data)
    # Create an object for the Column 2D chart using the FusionCharts class constructor 
    template_name='core/charts.html'
    column2D = FusionCharts("column2D", "ex1" , "900", "350", "chart-1", "json", dataSource)
    return render(request , template_name, {'output': column2D.render()} )



def login(request):
    template_name='login.html'
    return render(request , template_name )

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        template_name='core/index.html'
        login(request, user)
        return render(request,template_name)
    else:
        print('login none ')
        return 0

def logout_view(request):
    logout(request)
    template_name='registration/login.html'
    return render(request, template_name)



def logoutTlogin(request):
    return logout_then_login(request, login_url='/login')


def intro(request):
    template_name = 'core/home.html'
    return render(request, template_name)

@login_required
def demande_affiche(request):
    query_results=FeeRequest.objects.all()
    template_name='core/table_copy.html'
    
    context={"query_results":query_results}
    return render(request , template_name ,context)


@login_required
def admin_demande_affiche(request):
    query_results=FeeRequest.objects.filter(refused=False, level1=False)
    template_name='core/table_admin.html'
    
    context={"query_results":query_results}
    return render(request , template_name ,context)


@login_required
def admin2_demande_affiche(request):
    query_results=FeeRequest.objects.filter(refused=False, level1=True, level2=False)
    template_name='core/table_admin2.html'
    
    context={"query_results":query_results}
    return render(request , template_name ,context)


@login_required
def demande_traffiche(request):
    query_results=FeeRequest.objects.all().filter(validated=True)
    template_name='core/table.html'
    context={"query_results":query_results}
    return render(request , template_name ,context)



@login_required
def traitementDemande(request, id):

    query = FeeRequest.objects.get(id=id)
    form = FeeValidateForm2(initial={'validated': query.validated, 'driver': query.driver, 'activity': query.activity, 'agency': query.agency, 'date': query.date, 'a_rembourser': query.a_rembourser, 'code_vehicule': query.code_vehicule, 'code_remorque': query.code_remorque, 'imat_vehicule': query.imat_vehicule, 'imat_remorque': query.imat_remorque, })
    if request.method == "POST":
        form = FeeValidateForm2(request.POST, instance=query)
        if form.is_valid():
            try:
                form.instance.level1 = True
                form.save()
                model = form.instance
                messages.info(request, "Demande traitée avec succès !")
                return redirect('/admin-demandes')
            except Exception as e:
                messages.info(request, "Veuillez fournir les infos réquises!")
    context = {'form': form, 'query': query}
    return render(request, 'core/traitement-demande.html', context)


@login_required
def traitementDemande2(request, id):

    query = FeeRequest.objects.get(id=id)
    form = FeeValidateForm(initial={'validated': query.validated})
    if request.method == "POST":
        form = FeeValidateForm(request.POST, instance=query)
        if form.is_valid():
            try:
                form.instance.level2 = True
                form.instance.en_attente = False
                form.save()
                model = form.instance
                messages.info(request, "Demande traitée avec succès !")
                return redirect('/admin-demandes')
            except Exception as e:
                messages.info(request, "Veuillez fournir les infos réquises!")
    context = {'form': form, 'query': query}
    return render(request, 'core/traitement-demande2.html', context)



@login_required
def welcome_admin(request):
    template_name='core/index.html'
    nb_dmd=FeeRequest.objects.all().filter(en_attente=True).count()
    
    nb_dmdt=FeeRequest.objects.all().filter(level1=True, level2=True).count()
    nb_dmds=FeeRequest.objects.all().filter(refused=True).count()
    context = {'nb_dmd': nb_dmd, 'nb_dmdt': nb_dmdt, 'nb_dmds': nb_dmds}
    return render(request , template_name, context )


class FeeRequestCreateView(LoginRequiredMixin, CreateView):

    login_url = '/login'

    model = FeeRequestForm
    form_class = FeeRequestForm
    template_name = 'core/fee_request_create.html'

    def post(self, request, *args, **kwargs):
        reasons_data = {
            'PESAGE': request.POST.get('PESAGE'),
            'PEAGE': request.POST.get('PEAGE'),
            'SBK': request.POST.get('SBK'),
            'FRAIS TAXI': request.POST.get('FRAIS TAXI'),
        }

        form = self.form_class(request.POST)
        form_reason = ReasonDataChecker(reasons_data)

        if form.is_valid() and form_reason.is_valid():
            print('can be saved')
            fee_request = form.save(commit=False)
            fee_request.user = request.user
            fee_request.save()
            form_reason.save(fee_request)
            messages.success(request, "Demande soumise avec succès !")
            return redirect('/home')
        else:
            pass
            print('can not be saved')
            messages.warning(request, "Veuillez vérifier toutes les infos !")
        context = {'form': form, 'has_reason_error': not form_reason.is_valid()}
        return render(request, self.template_name, context)


class ReasonDataChecker:
    _data = None
    _cleaned_data = None

    def __init__(self, data):
        if not isinstance(data, dict):
            self._data = None
        else:
            self._data = data

    def is_valid(self):
        if self._data is None:
            return False
        # sanitize str to int if not can not convert to int force return of False
        for key, val in self._data.items():
            try:
                self._data[key] = int(val)
            except (TypeError, ValueError):
                self._data[key] = None

        is_valid = any(self._data.values())
        self._cleaned_data = self._data if is_valid else None
        return is_valid

    def save(self, fee_request):

        if self._cleaned_data is not None:
            for key, val in self._cleaned_data.items():
                if val is not None:
                    fee_reason = FeeReason(request=fee_request, label=key, quantity=val)
                    fee_reason.save(force_update=True)
                    # le prix est automatiquement defini à la creation grâce à la surcharge de la methode save dans le modele
