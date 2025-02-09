$(document).ready(function() {
    $('.select2').select2({
        language: {
            noResults: function() {
                return "Aucun résultat trouvé";
            }
        }
    });
    
    $('#countries').on('select2:select', function (e) {
        if ($(this).val().length > 4) {
            $(this).val($(this).val().slice(0, 4)).trigger('change');
        }
    });

    const GET_COUNTRY_DATA_URL = "{% url 'Visualisation_app:get_country_data' %}";
    function updateVisualization() {
        const indicator = $('#indicator').val();
        const countries = $('#countries').val();
        const selectedStats = $('input[name="statistics"]:checked').map(function() {
            return this.value;
        }).get();
        
        if (!indicator || !countries || countries.length === 0 || selectedStats.length === 0) {
            $('#welcome-message').show();
            $('#plotly-chart').hide();
            $('#indicator-description').hide();
            $('#stats-container').empty();
            return;
        }
        
        const startYear = $('#start-year').val();
        const endYear = $('#end-year').val();
        
        $.get(GET_COUNTRY_DATA_URL, {
            indicator: indicator,
            countries: countries,
            start_year: startYear,
            end_year: endYear,
            statistics: selectedStats
        }, function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            // Afficher la description
            $('#indicator-description').html(response.description).show();
            
            updatePlotlyChart(response.data);
            updateStats(response.stats);
            
            $('#welcome-message').hide();
            $('#plotly-chart').show();
        });
    }
    
    // Mise à jour du graphique Plotly
    function updatePlotlyChart(data) {
        const traces = [];
        const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'];
        
        let i = 0;
        for (let countryId in data) {
            const countryName = $('#countries option[value="' + countryId + '"]').text();
            traces.push({
                x: data[countryId].years,
                y: data[countryId].values,
                name: countryName,
                type: 'scatter',
                mode: 'lines+markers',
                line: {
                    color: colors[i],
                    width: 2
                },
                marker: {
                    size: 6,
                    color: colors[i]
                }
            });
            i++;
        }

        const indicatorName = $('#indicator option:selected').text();
        
        const layout = {
            title: {
                text: `Évolution du ${indicatorName}`,
                font: {
                    size: 24
                }
            },
            xaxis: {
                title: 'Année',
                gridcolor: '#eee'
            },
            yaxis: {
                title: indicatorName,
                gridcolor: '#eee'
            },
            hovermode: 'closest',
            showlegend: true,
            legend: {
                x: 1,
                xanchor: 'right',
                y: 1
            },
            plot_bgcolor: 'white',
            paper_bgcolor: 'white',
            margin: {
                l: 50,
                r: 50,
                t: 80,
                b: 50
            }
        };
        
        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtons: [
                ['zoom2d', 'pan2d'],
                ['zoomIn2d', 'zoomOut2d'],
                ['autoScale2d'],
                ['resetScale2d']
            ]
        };
        
        Plotly.newPlot('plotly-chart', traces, layout, config);
    }
    
    // Mise à jour des statistiques
    function updateStats(stats) {
        let html = '<h3>Statistiques</h3>';
        
        // Définition des noms en français pour chaque statistique
        const statNames = {
            'mean': 'Moyenne',
            'std': 'Écart-type',
            'var': 'Variance',
            'median': 'Médiane',
            'seasonality': 'Saisonnalité',
            'skewness': 'Asymétrie',
            'kurtosis': 'Aplatissement'
        };

        for (let countryId in stats) {
            const countryName = $('#countries option[value="' + countryId + '"]').text();
            html += `
                <div class="country-stats" style="margin-bottom: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
                    <h4 style="color: #007bff; margin-bottom: 10px;">${countryName}</h4>
                    <table style="width: 100%;">
            `;

            // Parcourir toutes les statistiques disponibles pour ce pays
            for (let statKey in stats[countryId]) {
                const value = stats[countryId][statKey];
                
                // Ne pas afficher les statistiques null ou undefined
                if (value !== null && value !== undefined) {
                    // Formater la valeur avec 2 décimales pour les nombres
                    const formattedValue = typeof value === 'number' ? value.toFixed(2) : value;
                    html += `
                        <tr>
                            <td style="padding: 5px;"><strong>${statNames[statKey] || statKey}:</strong></td>
                            <td style="padding: 5px; text-align: right;">${formattedValue}</td>
                        </tr>
                    `;
                }
            }

            html += `
                    </table>
                </div>
            `;
        }

        if (Object.keys(stats).length === 0) {
            html += '<p>Aucune donnée statistique disponible.</p>';
        }

        $('#stats-container').html(html);
    }

    // Événements pour la mise à jour automatique
    $('#indicator, #countries').on('change', updateVisualization);
    $('#start-year, #end-year').on('input', updateVisualization);
    $('input[name="statistics"]').on('change', updateVisualization);
});