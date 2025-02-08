from django.shortcuts import render, redirect
from Report_app.forms import reportForm
from django.contrib.auth.decorators import login_required
from Form_app.models import Country, EconomicIndicator, Indicator_List
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.io import to_image
import base64
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse, FileResponse
from PyPDF2 import PdfMerger, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame

# Create your views here.

def generate_PDF(request): 

    if request.method == "POST":
        form = reportForm(request.POST)
        if form.is_valid():
            indicator = form.cleaned_data['indicateur']
            countries = form.cleaned_data['pays']
            year_min = form.cleaned_data['annee_min']
            year_max = form.cleaned_data['annee_max']

            if year_min > year_max:
                context = {'message': 'Formulaire mal renseigné !!', "form": form,}
                return render(request, 'Report_app/html_to_pdf_file.html', context)

            try:
                filtered_data = EconomicIndicator.objects.filter(
                    Year__gte=year_min,
                    Year__lte=year_max,
                    Country__in=countries,
                )
                n_data = pd.DataFrame(list(filtered_data.values()))
                n_data['Country'] = [element.Country.Countryname for element in filtered_data]
                indicator_obj = Indicator_List.objects.get(Name=indicator)
                indicator_name = indicator_obj.Name_EconomicIndicator
                available_columns = ['Country', 'Year'] + [indicator_name]
                data = n_data[[col for col in available_columns if col in n_data.columns]]
        
                graphs=[]; images_path=[]
                graph_counter = 1
                graph_folder = os.path.join(settings.MEDIA_ROOT, 'graphs')
                os.makedirs(graph_folder, exist_ok=True) 

                for country in data['Country'].unique():

                    data_filtered = data[data['Country'] == country]
                    
                    if not data_filtered.empty:
                        fig, ax = plt.subplots(figsize=(12, 5))
                        ax.plot(data_filtered['Year'], data_filtered[indicator_name])
                        ax.set_title(f'{indicator_name} de {country} par Année', fontsize=16, fontname='Times-Roman', pad=20)
                        ax.set_xlabel('Année', fontsize=12, fontname='Times-Roman', labelpad=15)
                        ax.set_ylabel(f'{indicator_name}', fontsize=12, fontname='Times-Roman', labelpad=15)
                        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
                        
                        # Convertir le graphique en image (PNG) en mémoire
                        img_stream = io.BytesIO()
                        fig.savefig(img_stream, format='png')
                        img_stream.seek(0)
                        img_data = img_stream.getvalue()
                        
                        # Encodage de l'image en base64 pour l'affichage dans le template
                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                        graphs.append(f"data:image/png;base64,{img_base64}")

                        # Enregistrer le graphique sur le disque avec un nom unique
                        graph_filename = f"graph{graph_counter}.png"
                        graph_path = os.path.join(graph_folder, graph_filename)
                        fig.savefig(graph_path, format='png')
                        images_path.append(os.path.join(settings.MEDIA_ROOT, 'graphs', graph_filename))
                        graph_counter += 1
                        plt.close(fig)
                        
                        # Incrémenter le compteur pour le nom du prochain graphique
                        graph_counter += 1
                    else:
                        # Ajouter un graphique vide si aucune donnée n'est disponible
                        graphs.append(None)

                show_graph = True
                request.session['images_path'] = images_path
                request.session['indicator_name'] = indicator_name
                request.session['indicator_description'] = indicator_obj.Description

                context = {"form": form, "graphs": graphs, "indicator": indicator_obj, 
                            "show_graph":show_graph, }

                return render(request, 'Report_app/html_to_pdf_file.html', context)
            
            except EconomicIndicator.DoesNotExist:
                context = {'message': 'Aucune donnée trouvée !!', "form": form,}
                return render(request, 'Report_app/html_to_pdf_file.html', context)

        else:  
            context = {'message': 'Formulaire mal renseigné !!', "form": form,}
            return render(request, 'Report_app/html_to_pdf_file.html', context)

    form = reportForm()

    return render(request, 'Report_app/html_to_pdf_file.html', {"form": form,})


from Users_app.decorators import connectez_vous

@connectez_vous
def download_PDF(request):

    images_path = request.session.get('images_path', [])
    indicator_name = request.session.get('indicator_name', 'Indicateur')
    indicator_description = request.session.get('indicator_description', '')

    logo_path = "media/graphs/logo.jpeg"
    x_marge = 20; y_marge = 55; space = 55; space_logo = 15; correction = 50; 
    logo_dim = 40; page_width, page_height = A4

    if not images_path:
        return HttpResponse("Aucun graphique disponible pour générer le rapport.", status=400)

    # Création du fichier PDF d'introduction
    report_filename = f"Rapport_{indicator_name}.pdf"
    intro_path = os.path.join(settings.MEDIA_ROOT, report_filename)
    c = canvas.Canvas(intro_path, pagesize=A4)

    def insert_logo(c, logo_path, logo_dim, y_marge, space_logo, page_height):
        x_position = y_marge  
        y_position = page_height - y_marge  
        logo_width = logo_dim
        logo_height = logo_dim
        c.drawImage(logo_path, x_position, y_position, width=logo_width, height=logo_height)

        c.setFont("Helvetica", 10)
        title_text = "Rapport généré par STYMO-AW"
        title_width = c.stringWidth(title_text, "Helvetica", 10)
        title_x = x_position + logo_width + space_logo 
        title_y = y_position + (logo_height - 10)/2
        c.drawString(title_x, title_y, title_text)

    def insert_image1(c, images_path, x_marge, y_marge, page_width, page_height, space, correction, i):
        image_path = images_path[i]
        x_position = x_marge
        y_position = (page_height + space)/2 
        image_width = page_width - 2*x_marge  
        image_height = (page_height - 2*y_marge - space)/2 - correction
        c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height)

    def insert_image2(c, images_path, x_marge, y_marge, page_width, page_height, space, correction, i):
        image_path = images_path[i]
        x_position = x_marge
        y_position = y_marge + space/2
        image_width = page_width -2*x_marge  
        image_height = (page_height - 2*y_marge - space)/2 - correction
        c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height)
        c.showPage() # Passe à la page suivante

    insert_logo(c, logo_path, logo_dim, y_marge, space_logo, page_height)

    # Titre : Centrer le texte avec les marges de 2 cm
    c.setFont("Helvetica-Bold", 24)
    title_text = "Rapport sur les indicateurs économiques"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 24)
    title_x = (page_width - title_width - 2*y_marge) / 2 + y_marge
    title_y = page_height - y_marge - 35
    c.drawString(title_x, title_y, title_text)

    c.setFont("Helvetica-Bold", 24)
    title_text = "en Afrique Centrale"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 24)
    title_x = (page_width - title_width - 2*y_marge) / 2 + y_marge
    title_y = title_y - 40 
    c.drawString(title_x, title_y, title_text)

    # Sous-titre avec les marges
    subtitle_text = f"Rapport de l'indicateur : {indicator_name}"
    max_width = page_width - 2 * y_marge  
    font_size = 20
    subtitle_width = c.stringWidth(subtitle_text, "Times-Bold", font_size)
    while subtitle_width > max_width and font_size > 8:
        font_size -= 1  
        subtitle_width = c.stringWidth(subtitle_text, "Times-Bold", font_size)
    subtitle_x = (page_width - subtitle_width) / 2
    c.setFont("Times-Bold", font_size)
    subtitle_y = title_y - 60
    c.drawString(subtitle_x, subtitle_y, subtitle_text)

    # Description de l'indicateur avec marges
    description_frame = Frame(y_marge, 430, page_width - 2 * y_marge, 200, showBoundary=0)
    styles = getSampleStyleSheet()
    description_style = ParagraphStyle(
        "DescriptionStyle",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=14,
        alignment=4,
        leading=20,
    )
    description_paragraph = Paragraph(indicator_description, style=description_style)
    description_frame.addFromList([description_paragraph], c)

    insert_image2(c, images_path, x_marge, y_marge, page_width, page_height, space, correction, i=0) 
    i=1

    while (i < len(images_path)-1):

        # Logo
        insert_logo(c, logo_path, logo_dim, y_marge, space_logo, page_height)
        
        # Ajouter l'image 1 :
        insert_image1(c, images_path, x_marge, y_marge, page_width, page_height, space, correction, i)
        i = i+1
        
        # Ajouter l'image 1 :
        insert_image2(c, images_path, x_marge, y_marge, page_width, page_height, space, correction, i)
        i = i+1

    # Sauvegarder le PDF
    c.save()

    # Fournir le fichier comme réponse pour le téléchargement
    try:
        response = FileResponse(open(intro_path, 'rb'), as_attachment=True, filename=report_filename)
        return response
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération du fichier : {e}", status=500)