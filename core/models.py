from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import F, Sum, ExpressionWrapper
from django.http import request





class Chauffeur(models.Model):

    nom_prenom = models.CharField(max_length=150, verbose_name='Nom et prénoms')
    code_matricule = models.CharField(max_length=10, verbose_name='Code matricule')
    est_actif = models.BooleanField(default=True, verbose_name='Est Actif')

    class Meta:
        verbose_name = "chauffeur"
        verbose_name_plural = "chauffeurs"

    def __str__(self):
        return f"{self.nom_prenom} - {self.code_matricule}"




ACTIVITY_CHOICES = [
    ('DGE', 'Dir. Générale(DGE)'),
    ('DCF', 'Dir. Financière(DCF)'),
    ('DRH', 'Dir. RH(DRH)'),
    ('DEX', 'Dir. Exploitation(DEX)'),
    ('DET', 'Dir. Technique(DET)'),
    ('DCM', 'Dir. Commerciale(DCM)'),
    ('SMG', 'Moyens Generaux(SMG)'),
    ('FHY', 'fret Hydrocarbure(FHY)'),
    ('FSB', 'fret boisson(FSB)'),
    ('FHP', 'fret huile de palm(FHP)'),
    ('FTC', 'fret conteneurs(FTC)'),
    ('FCS', 'fret canne à sucre(FCS)'),
    ('FDI', 'fret divers(FDI)'),
    ('LEV', 'levage(LEV)'),
    ('LOC', 'location de surfaces(LOC)'),
    ('SDI', 'services divers(SDI)'),
    ('RAV', 'revenus à ventiler(RAV)'),
    ('PAF', 'Prestation Accessoir(PAF)'),
    ('COL', 'fret Colis lourds(COL)'),

]

AGENCY_CHOICES = [
    ('0000', 'Siège'),
    ('0001', 'Abidjan (agence principale)'),
    ('0002', 'Bouaflé'),
    ('0003', 'San-Pedro'),
    ('0007', 'Bouaké'),
    ('0008', 'Yamoussoukro'),
    ('0009', 'Ferké'),
    ('0010', 'Minautores'),

]


axeAnalyseChoix = [
    ('200', 'Batiment et charge locative'),
    ('210', 'Voyage & deplacement'),
    ('220', 'Fourniture & consommable de bureau'),
    ('230', 'Charge personnel'),
    ('240', 'Quote-part depreciation immo'),
    ('250', 'Personnel & services exterieur'),
    ('260', 'Relation exterieur'),
    ('270', 'Impôt & taxes'),
    ('280', 'Autres charges directions et service'),
    ('900', "Recette d'exploitation"),
    ('910', 'Frais/Opération (frais voyages)'),
    ('920', 'Papier administratif-CR'),
    ('930', "Main d'oevre dédiée"),
    ('940', 'Quote-part amortissement CR et autres'),
    ('950', 'Entretien & reparation CR'),
    ('960', 'Frais generaux'),


]

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    direction = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    code_matricule = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class FeeRequest(models.Model):
    driver = models.ForeignKey(Chauffeur, on_delete=models.CASCADE, verbose_name="Chauffeur")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="demandeur", on_delete=models.CASCADE)
    activity = models.CharField(choices=ACTIVITY_CHOICES, max_length=3, default='DGE', verbose_name="activité")
    agency = models.CharField(choices=AGENCY_CHOICES, max_length=4, default='0001', verbose_name="agence", blank=True)
    date = models.DateTimeField()
    timestamp = models.DateField(auto_now_add=True)
    observation_admin = models.TextField(blank=True, verbose_name="Observation")
    a_rembourser = models.BooleanField(default=False, verbose_name='A rembourser')
    axe_analyse = models.CharField(choices=axeAnalyseChoix, max_length=255, verbose_name="Axe analyse", blank=True)
    validated = models.BooleanField(default=False, verbose_name="Validée")
    refused = models.BooleanField(default=False, verbose_name="Refusée")
    en_attente = models.BooleanField(default=True, verbose_name="En attente")
    code_vehicule = models.CharField(max_length=50, verbose_name='Code véhicule', blank=True)
    code_remorque = models.CharField(
        max_length=50, verbose_name='Code remorque', blank=True)
    level1 = models.BooleanField(default=False)
    level2 = models.BooleanField(default=False)
    imat_vehicule = models.CharField(
        max_length=50, verbose_name='Imat. véhicule', blank=True)
    imat_remorque = models.CharField(
        max_length=50, verbose_name='Imat. Remorque', blank=True)

    commentaire = models.TextField(blank=True)

    class Meta:
        verbose_name = "Demande"
        verbose_name_plural = "Demandes"

    @property
    def get_total_price(self):
        total_price = FeeReason.objects.filter(request_id=self.id).aggregate(
            total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=models.FloatField()))
        )['total']

        return f'{total_price}'


    @property
    def get_reasons(self):
        return FeeReason.objects.filter(request_id=self.id)



    def __str__(self):
        return f'{self.driver} -> {self.activity} -> {self.timestamp}'


FEE_LABEL_CHOICES = [
    ('PESAGE', 'PESAGE'),
    ('PEAGE', 'PEAGE'),
    ('SBK', 'SEJOUR BOUAKE'),
    ('FRAIS TAXI', 'TAXI'),

]


# juste pour retrouver le prix en fonction du libelle
FEE_LABEL_CHOICES_PRICE = {
    'PESAGE': 5000,
    'PEAGE': 10000,
    'SBK': 25000,
    'FRAIS TAXI': 5000,
}


class FeeReason(models.Model):

    label = models.CharField(max_length=80, choices=FEE_LABEL_CHOICES, verbose_name="Libelle")
    quantity = models.PositiveIntegerField(default=1, verbose_name="quantité")
    price = models.FloatField(default=0, verbose_name="Montant")
    request = models.ForeignKey(FeeRequest, on_delete=models.CASCADE, verbose_name="Demande")


    class Meta:
        verbose_name = "Motif"
        verbose_name_plural = "Motifs"

    def __str__(self):
        return f'{self.label} x{self.quantity}  | {self.get_total_price} FCFA'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.price = FEE_LABEL_CHOICES_PRICE[self.label]
        super(FeeReason, self).save(force_insert, using, update_fields)

    @property
    def get_total_price(self):
        return self.price * self.quantity


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)