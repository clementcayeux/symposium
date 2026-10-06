import os
from datetime import date
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'symposium_site.settings')
django.setup()

from core.models import Invite

# Les 30 personnalités majeures de Symposium (titre = nom seul)
TOP_30_INVITES = [
    {
        "nom": "Jean-Marc Jancovici",
        "fonction": "Président du Shift Project & Associé Carbone 4",
        "categorie": "sciences",
        "ordre": 1,
        "date_venue": date(2023, 11, 29),
        "youtube_url": "https://www.youtube.com/watch?v=PYDNV0Ro1x0",
    },
    {
        "nom": "Dominique de Villepin",
        "fonction": "Ancien Premier ministre & Ministre des Affaires étrangères",
        "categorie": "politique",
        "ordre": 2,
        "date_venue": date(2024, 9, 16),
        "youtube_url": "https://www.youtube.com/watch?v=UCAZxRdwXkc",
    },
    {
        "nom": "Carlos Tavares",
        "fonction": "Directeur général de Stellantis (Diplômé Centrale)",
        "categorie": "economie",
        "ordre": 3,
        "date_venue": date(2023, 9, 19),
        "youtube_url": "https://www.youtube.com/watch?v=Tdj08ojp2OI",
    },
    {
        "nom": "Bernard Fontana",
        "fonction": "Président-directeur général d'EDF",
        "categorie": "economie",
        "ordre": 4,
        "date_venue": date(2026, 9, 23),
        "youtube_url": "https://www.youtube.com/watch?v=Ppmu73F8eb8",
    },
    {
        "nom": "Jacques Attali",
        "fonction": "Économiste, écrivain & Conseiller d'État",
        "categorie": "economie",
        "ordre": 5,
        "date_venue": date(2025, 4, 10),
        "youtube_url": "https://www.youtube.com/watch?v=8KxSIAFLE9U",
    },
    {
        "nom": "Éric Dupond-Moretti",
        "fonction": "Garde des Sceaux, ministre de la Justice & Avocat",
        "categorie": "politique",
        "ordre": 6,
        "date_venue": date(2018, 12, 14),
        "youtube_url": "https://www.youtube.com/watch?v=joRP61cb_Uo",
    },
    {
        "nom": "Édith Cresson",
        "fonction": "Première femme Première ministre de France",
        "categorie": "politique",
        "ordre": 7,
        "date_venue": date(2024, 10, 22),
        "youtube_url": "https://www.youtube.com/watch?v=8Kfy_3S1egQ",
    },
    {
        "nom": "Valérie Pécresse",
        "fonction": "Présidente de la Région Île-de-France",
        "categorie": "politique",
        "ordre": 8,
        "date_venue": date(2025, 10, 8),
        "youtube_url": "https://www.youtube.com/watch?v=iPvnxnpMZ1o",
    },
    {
        "nom": "Cédric Villani",
        "fonction": "Mathématicien (Médaille Fields) & Ancien député",
        "categorie": "sciences",
        "ordre": 9,
        "date_venue": date(2020, 12, 6),
        "youtube_url": "https://www.youtube.com/watch?v=Keabh7PuViE",
    },
    {
        "nom": "Patrice Caine",
        "fonction": "Président-directeur général de Thales",
        "categorie": "economie",
        "ordre": 10,
        "date_venue": date(2024, 10, 14),
        "youtube_url": "https://www.youtube.com/watch?v=SpdyLIcPjqE",
    },
    {
        "nom": "Martin Sion",
        "fonction": "Président exécutif d'ArianeGroup",
        "categorie": "sciences",
        "ordre": 11,
        "date_venue": date(2025, 4, 29),
        "youtube_url": "https://www.youtube.com/watch?v=4JRUmaFpjgM",
    },
    {
        "nom": "Geoffroy Roux de Bézieux",
        "fonction": "Ancien Président du MEDEF",
        "categorie": "economie",
        "ordre": 12,
        "date_venue": date(2024, 12, 2),
        "youtube_url": "https://www.youtube.com/watch?v=FfjV4ccK3Bo",
    },
    {
        "nom": "Amiral Nicolas Vaujour",
        "fonction": "Chef d'état-major de la Marine nationale",
        "categorie": "politique",
        "ordre": 13,
        "date_venue": date(2024, 11, 15),
        "youtube_url": "https://www.youtube.com/watch?v=FfjV4ccK3Bo",
    },
    {
        "nom": "André Comte-Sponville",
        "fonction": "Philosophe & Écrivain",
        "categorie": "culture",
        "ordre": 14,
        "date_venue": date(2024, 4, 9),
        "youtube_url": "https://www.youtube.com/watch?v=2mkWMLssZPM",
    },
    {
        "nom": "Sylvie Retailleau",
        "fonction": "Ministre de l'Enseignement supérieur et de la Recherche",
        "categorie": "politique",
        "ordre": 15,
        "date_venue": date(2023, 2, 2),
        "youtube_url": "https://www.youtube.com/watch?v=w5rh3Kh7w5Y",
    },
    {
        "nom": "Pascal Boniface",
        "fonction": "Directeur de l'IRIS & Géopolitologue",
        "categorie": "politique",
        "ordre": 16,
        "date_venue": date(2026, 5, 14),
        "youtube_url": "https://www.youtube.com/watch?v=rb2S1bkVKlM",
    },
    {
        "nom": "Gérard Araud",
        "fonction": "Ambassadeur de France aux États-Unis et à l'ONU",
        "categorie": "politique",
        "ordre": 17,
        "date_venue": date(2023, 3, 16),
        "youtube_url": "https://www.youtube.com/watch?v=-ZvEpR2Ulgc",
    },
    {
        "nom": "Manuel Bompard",
        "fonction": "Député & Coordinateur national de La France Insoumise",
        "categorie": "politique",
        "ordre": 18,
        "date_venue": date(2026, 6, 20),
        "youtube_url": "https://www.youtube.com/watch?v=iPvnxnpMZ1o",
    },
    {
        "nom": "Jean-Michel Fauvergue",
        "fonction": "Ancien chef du RAID & Député",
        "categorie": "culture",
        "ordre": 19,
        "date_venue": date(2025, 6, 12),
        "youtube_url": "https://www.youtube.com/watch?v=rb2S1bkVKlM",
    },
    {
        "nom": "François Villeroy de Galhau",
        "fonction": "Gouverneur de la Banque de France",
        "categorie": "economie",
        "ordre": 20,
        "date_venue": date(2023, 5, 24),
        "youtube_url": "https://www.youtube.com/watch?v=Ppmu73F8eb8",
    },
    {
        "nom": "Patrick Pouyanné",
        "fonction": "Président-directeur général de TotalEnergies",
        "categorie": "economie",
        "ordre": 21,
        "date_venue": date(2023, 10, 18),
        "youtube_url": "https://www.youtube.com/watch?v=Tdj08ojp2OI",
    },
    {
        "nom": "Laurent Fabius",
        "fonction": "Président du Conseil constitutionnel & Ancien Premier ministre",
        "categorie": "politique",
        "ordre": 22,
        "date_venue": date(2022, 11, 8),
        "youtube_url": "https://www.youtube.com/watch?v=UCAZxRdwXkc",
    },
    {
        "nom": "Florence Parly",
        "fonction": "Ancienne Ministre des Armées",
        "categorie": "politique",
        "ordre": 23,
        "date_venue": date(2023, 1, 26),
        "youtube_url": "https://www.youtube.com/watch?v=SpdyLIcPjqE",
    },
    {
        "nom": "Jean-Baptiste Djebbari",
        "fonction": "Ancien Ministre délégué chargé des Transports",
        "categorie": "politique",
        "ordre": 24,
        "date_venue": date(2022, 3, 15),
        "youtube_url": "https://www.youtube.com/watch?v=iPvnxnpMZ1o",
    },
    {
        "nom": "Henri Proglio",
        "fonction": "Ancien Président-directeur général d'EDF et de Veolia",
        "categorie": "economie",
        "ordre": 25,
        "date_venue": date(2024, 2, 7),
        "youtube_url": "https://www.youtube.com/watch?v=Ppmu73F8eb8",
    },
    {
        "nom": "Gaspard Koenig",
        "fonction": "Philosophe, essayiste & Fondateur de GenerationLibre",
        "categorie": "culture",
        "ordre": 26,
        "date_venue": date(2024, 5, 22),
        "youtube_url": "https://www.youtube.com/watch?v=2mkWMLssZPM",
    },
    {
        "nom": "Jean-Dominique Senard",
        "fonction": "Président du conseil d'administration de Renault",
        "categorie": "economie",
        "ordre": 27,
        "date_venue": date(2023, 12, 11),
        "youtube_url": "https://www.youtube.com/watch?v=Tdj08ojp2OI",
    },
    {
        "nom": "Clara Gaymard",
        "fonction": "Cofondatrice de Raise & Ancienne PDG de GE France",
        "categorie": "economie",
        "ordre": 28,
        "date_venue": date(2023, 4, 4),
        "youtube_url": "https://www.youtube.com/watch?v=FfjV4ccK3Bo",
    },
    {
        "nom": "Philippe Aghion",
        "fonction": "Économiste & Professeur au Collège de France",
        "categorie": "sciences",
        "ordre": 29,
        "date_venue": date(2024, 3, 27),
        "youtube_url": "https://www.youtube.com/watch?v=8KxSIAFLE9U",
    },
    {
        "nom": "Bertrand Badré",
        "fonction": "Ancien Directeur général de la Banque mondiale",
        "categorie": "economie",
        "ordre": 30,
        "date_venue": date(2024, 6, 5),
        "youtube_url": "https://www.youtube.com/watch?v=Ppmu73F8eb8",
    },
]

def main():
    print("Purge complète de la table Invite...")
    Invite.objects.all().delete()

    print("Insertion des 30 plus grands invités...")
    for data in TOP_30_INVITES:
        Invite.objects.create(
            nom=data["nom"],
            fonction=data["fonction"],
            categorie=data["categorie"],
            ordre=data["ordre"],
            date_venue=data["date_venue"],
            youtube_url=data["youtube_url"],
            description="",
        )
        print(f"[{data['ordre']:02d}] {data['nom']}")

    print(f"\nTerminé : {len(TOP_30_INVITES)} invités de premier plan enregistrés.")

if __name__ == "__main__":
    main()