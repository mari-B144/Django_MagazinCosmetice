import datetime
from collections import Counter
from django.shortcuts import render
from django.http import HttpResponse

lista_accesari = []

def formatare(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    zile=["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"]
    luni=["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie","Iulie","August", "Septembrie", "Octombrie", "Noiembrie","Decembrie"]

    current_day = zile[datetime.datetime.now().weekday()]
    current_month= luni[datetime.datetime.now().month-1]
    return f"{current_day}, {datetime.datetime.now().day} {current_month} {datetime.datetime.now().year}"
    
# Create your views here.
def index(request):
    
    acc = Accesare(request)
    lista_accesari.append(acc)
    return render(request, 'html/index.html')
    #return HttpResponse(f"""<html><body><h1>Magazin de cosmetice</h1><p>Acesta este un magazin online de unde se pot achizitiona produse cosmetice si de ingrijire personala. Exista o selectie vasta de produse organizate pe categorii sau in functie de brand.</p></body></html>""")

def info(request):
   
    acc = Accesare(request)
    tip_param=request.GET.get("data", "")
    rezultat_data=acc.data(tip_param)
    
    
    html = f"""<html>
                            <title>Informații despre server</title>
                                <body>
                                    <h1>Informații despre server</h1>
                                    <section>
                                        <h2>Data și ora</h2>
                                        <p>{rezultat_data}</p>
                                    </section>
                                </body>
                            </html>"""
    return HttpResponse(html)

def istoric(request):
    acc = Accesare(request)
    lista_accesari.append(acc)
    return HttpResponse("<html><body><h1>Pagina de Istoric</h1><p>Aici va fi istoricul magazinului de cosmetice.</p></body></html>")


def despre(request):
    acc = Accesare(request)
    lista_accesari.append(acc)
    return HttpResponse("<html><body><h1>Despre Noi</h1><p>Magazinul nostru ofera cele mai bune produse cosmetice.</p></body></html>")

class Accesare:
    
    contor = 1

    def __init__(self, request):
        self.id = Accesare.contor
        Accesare.contor += 1
        self.ip_client = request.META.get('REMOTE_ADDR')
        self.parametri = dict(request.GET)
        self._url = request.build_absolute_uri()  
        self._pagina = request.path             
        self.data_obiect = datetime.datetime.now()

    def lista_parametri(self):
        return [(k, v) for k, v in self.parametri.items()]

    def url(self):
        return self._url

    def pagina(self):
        return self._pagina

    def data(self, format=None):
        data_ro = formatare(self.data_obiect)
        ora_curenta = self.data_obiect.strftime("%H:%M:%S")
        
        if format == "zi":
            return f"Data curentă: {data_ro}"
        elif format == "timp":
            return f"Ora curentă: {ora_curenta}"
        else: 
            return f"Data și ora curentă: {data_ro}, ora {ora_curenta}" 

    def __str__(self):
        params_str = ", ".join([f"{k}={v}" for k, v in self.lista_parametri()]) if self.parametri else "fără parametri"
        return f"Accesare ID: {self.id} | IP: {self.ip_client} | Pagină: {self.pagina()} | Data: {self.data()} | Parametri: {params_str}"
        
def log_view(request):
    acc = Accesare(request)
    lista_accesari.append(acc)

    html_out = "<html><head><title>Jurnal Accesări</title></head><body>"
    html_out += "<h1>Jurnal Accesări (Log)</h1>"

    #parametri
    nr_param = len(request.GET)
    nume_param = list(request.GET.keys())
    html_out += f"<section><h2>Parametri</h2><p>Număr parametri: <b>{nr_param}</b></p>"
    html_out += f"<p>Nume parametri: {', '.join(nume_param) if nume_param else 'niciunul'}</p></section>"

    #parametrul accesari=nr
    if request.GET.get("accesari") == "nr":
        html_out += f"<section><h2>Număr total accesări</h2><p>Sesiunea curentă are <b>{len(lista_accesari)}</b> accesări.</p></section>"

    #parametrul accesari=detalii
    if request.GET.get("accesari") == "detalii":
        html_out += "<section><h2>Detalii Accesări</h2><ul>"
        for a in lista_accesari:
            html_out += f"<li>Data și ora: {a.data()} (Pagină: {a.pagina()})</li>"
        html_out += "</ul></section>"

    #filtrare dupa iduri si dubluri
    iduri_raw = request.GET.getlist("iduri")
    dubluri_param = request.GET.get("dubluri", "false").lower() == "true"
    
    if iduri_raw:
        lista_ceruta = []
        for segment in iduri_raw:
            for val in segment.split(","):
                if val.strip().isdigit():
                    lista_ceruta.append(int(val.strip()))
        
        accesari_filtrate = []
        vazute = set()
        for i in lista_ceruta:
            for a in lista_accesari:
                if a.id == i:
                    if dubluri_param:
                        accesari_filtrate.append(a)
                    else:
                        if i not in vazute:
                            accesari_filtrate.append(a)
                            vazute.add(i)
                    break
        
        html_out += "<section><h2>Accesări după ID-uri</h2><ul>"
        for a in accesari_filtrate:
            html_out += f"<li>{a}</li>"
        html_out += "</ul></section>"

    #ultimele=n
    ultimele_val = request.GET.get("ultimele")
    mesaj_eroare = ""
    accesari_de_afisat = lista_accesari
    
    if ultimele_val is not None:
        try:
            n = int(ultimele_val)
            if n < 0:
                raise ValueError
            k = len(lista_accesari)
            if n > k:
                mesaj_eroare = f"Exista doar {k} accesari fata de n accesari cerute".replace("n", str(n)).replace("k", str(k))
                accesari_de_afisat = lista_accesari
            else:
                accesari_de_afisat = lista_accesari[-n:]
        except ValueError:
            mesaj_eroare = "Eroare: Parametrul 'ultimele' trebuie să fie un număr întreg valid!"

    if ultimele_val is not None or not request.GET:
        html_out += "<section><h2>Lista Accesări</h2>"
        if mesaj_eroare:
            html_out += f"<p style='color:red;'><b>{mesaj_eroare}</b></p>"
        html_out += "<ul>"
        for a in accesari_de_afisat:
            html_out += f"<li>{a}</li>"
        html_out += "</ul></section>"

    #parametru tabel (tabel=tot sau tabel=id,url)
    tabel_val = request.GET.get("tabel")
    if tabel_val is not None:
        if tabel_val == "tot":
            coloane = ["id", "ip_client", "url", "pagina", "data"]
        else:
            coloane = [c.strip() for c in tabel_val.split(",")]
        
        html_out += "<section><h2>Tabel Accesări</h2><table border='1' cellpadding='5'><tr>"
        for col in coloane:
            html_out += f"<th>{col.upper()}</th>"
        html_out += "</tr>"

        for a in lista_accesari:
            html_out += "<tr>"
            for col in coloane:
                val = getattr(a, col)() if callable(getattr(a, col, None)) else getattr(a, col, "")
                html_out += f"<td>{val}</td>"
            html_out += "</tr>"
        html_out += "</table></section>"

    #statistici
    if lista_accesari:
        pagini_numar = Counter([a.pagina() for a in lista_accesari])
        cel_mai_mult = pagini_numar.most_common(1)[0]
        cel_mai_putin = pagini_numar.most_common()[-1]
        
        html_out += "<section><h2>Statistici Pagini</h2>"
        html_out += f"<p><b>Cea mai accesată:</b> {cel_mai_mult[0]} ({cel_mai_mult[1]} ori)</p>"
        html_out += f"<p><b>Cea mai puțin accesată:</b> {cel_mai_putin[0]} ({cel_mai_putin[1]} ori)</p>"
        html_out += "</section>"

    html_out += "</body></html>"
    return HttpResponse(html_out)


# ruta dinamica cu re_path pentru /accesare<id>
def detalii_accesare(request, id):
    acc = Accesare(request)
    lista_accesari.append(acc)
    
    id_numeric = int(id)
    gasit = next((a for a in lista_accesari if a.id == id_numeric), None)
    
    if not gasit:
        return HttpResponse(f"<html><body><h1>Accesarea #{id_numeric} nu a fost găsită.</h1></body></html>", status=404)
        
    return HttpResponse(f"<html><body><h1>Detalii Accesare #{gasit.id}</h1><p>{gasit}</p></body></html>")


    
def exemplu_template(request):
    return render(request,"template.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )
    
def exemplu_template2(request):
    return render(request,"template2.html")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Produs
from django.shortcuts import render

def afisare_produse(request):
    nrPagina=request.GET.get("pagina",1)
    # veti trata situatia in care nu e dat un numar intreg
    produse=Produs.objects.all()
    paginator = Paginator(produse, 5)
    mesajEroare=None
    try:
        obPagina = paginator.page(nrPagina)
    except EmptyPage:
        obPagina=None
        mesajEroare = "Nu mai sunt produse"
    return render(request, 'aplicatie_exemplu/produse.html',
                    {
                        'pagina': obPagina,
                        'eroare': mesajEroare
                    }
    )

    
