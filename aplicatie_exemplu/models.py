from django.db import models

class Categorie(models.Model):
    class Meta:
        verbose_name_plural = "Categorii"
        ordering = ['nume_categorie'] # bifeaza ordonarea implicita
        indexes = [
            models.Index(fields=['nume_categorie'], name='cat_nume_idx') # bifeaza index
        ]

    TIP_CHOICES = [
        ('ingrijire', 'Ingrijire ten'),
        ('machiaj', 'Machiaj'),
    ]

    nume_categorie = models.CharField(
        max_length=100, 
        unique=True, # bifeaza camp unic
        error_messages={'unique': 'exista deja.', 'blank': 'nu poate fi gol.'}, # bifeaza mesaje eroare
        help_text='nume categorie' # bifeaza help_text
    )
    descriere = models.TextField(null=True, blank=True, help_text='detalii categorie') # bifeaza camp null si help_text
    tip_categorie = models.CharField(max_length=50, choices=TIP_CHOICES, default='ingrijire') # bifeaza choices si default

    def __str__(self):
        return self.nume_categorie


class Brand(models.Model):
    class Meta:
        verbose_name_plural = "Branduri"
        ordering = ['nume_brand'] # bifeaza ordonarea implicita
        indexes = [
            models.Index(fields=['nume_brand'], name='brand_nume_idx')
        ]

    nume_brand = models.CharField(
        max_length=100, 
        unique=True, 
        default="Generic",
        error_messages={'unique': 'brand existent.'} # bifeaza mesaj eroare
    )
    categorie_cumparator = models.CharField(max_length=50, null=True, blank=True) # bifeaza null
    descriere = models.TextField(null=True, blank=True) # bifeaza null
    sigla = models.ImageField(upload_to='branduri/', null=True, blank=True) # bifeaza ImageField si null
    website = models.URLField(null=True, blank=True, help_text='site web oficial') # bifeaza URLField, null si help_text

    def __str__(self):
        return self.nume_brand


class SpecificatieProdus(models.Model):
    class Meta:
        verbose_name_plural = "Specificatii Produse"

    factor_protectie = models.IntegerField(
        null=True, 
        blank=True,
        error_messages={'invalid': 'spf invalid.'} # bifeaza mesaj eroare
    ) # bifeaza null
    nuanta = models.CharField(max_length=50, null=True, blank=True, help_text='nuanta produs') # bifeaza null si help_text

    def __str__(self):
        return f"SPF: {self.factor_protectie}"


class Produs(models.Model):
    class Meta:
        verbose_name_plural = "Produse"
        indexes = [
            models.Index(fields=['pret'], name='prod_pret_idx'), # bifeaza index
            models.Index(fields=['stoc_disponibil'], name='prod_stoc_idx', condition=models.Q(stoc_disponibil__gt=0)), # bifeaza index & Q
        ]
        constraints = [
            # bifeaza cele 5 constrangeri folosind models.Q
            models.CheckConstraint(condition=models.Q(pret__gte=0), name='pret_pozitiv'),
            models.CheckConstraint(condition=models.Q(stoc_disponibil__gte=0), name='stoc_pozitiv'),
            models.CheckConstraint(condition=models.Q(pret__lt=100000), name='pret_limita'),
            models.CheckConstraint(condition=models.Q(stoc_disponibil__lte=50000), name='stoc_limita'),
            models.CheckConstraint(condition=models.Q(pret__gt=-1), name='pret_valid'),
        ]

    IMPACHETARE = [
        ('tub', 'Tub'),
        ('borcan', 'Borcan'),
    ]

    nume_produs = models.CharField(
        max_length=200, 
        unique=True,
        error_messages={'unique': 'produs existent.', 'blank': 'obligatoriu.'} # bifeaza mesaj eroare
    )
    pret = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=10.00, # bifeaza default
        error_messages={'invalid': 'pret invalid.'} # bifeaza mesaj eroare
    )
    tip_impachetare = models.CharField(max_length=50, choices=IMPACHETARE, default='tub') # bifeaza choices si default
    gramaj = models.CharField(max_length=50, null=True, blank=True, default="50ml", help_text='gramaj produs') # bifeaza null, default (permite gol in admin), help_text
    stoc_disponibil = models.IntegerField(default=0) # bifeaza default
    ingrediente = models.TextField(null=True, blank=True) # bifeaza null
    descriere = models.TextField(null=True, blank=True) # bifeaza null
    este_activ = models.BooleanField(default=True)
    este_noutate = models.BooleanField(default=False)
    este_bestseller = models.BooleanField(default=False)
    
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True) # bifeaza SlugField si null
    data_adaugare = models.DateTimeField(auto_now_add=True, null=True) # bifeaza auto_now_add si null

    # legaturi
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="produse") # bifeaza null
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name="produse") # bifeaza null
    specificatie = models.OneToOneField(SpecificatieProdus, on_delete=models.CASCADE, null=True, blank=True) # bifeaza null

    def __str__(self):
        return self.nume_produs


class Contract(models.Model):
    class Meta:
        verbose_name_plural = "Contracte"

    begin_date = models.DateField(help_text='data inceput') # bifeaza help_text
    end_date = models.DateField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="contracte")

    def __str__(self):
        return f"Contract #{self.id}"