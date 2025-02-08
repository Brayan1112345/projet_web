$(document).ready(function() {
    $('.select2').select2();
    
    $('#indicators').on('select2:select', function(e) {
        if ($(this).val() && $(this).val().length > 4) {
            $(this).val($(this).val().slice(0, 4)).trigger('change');
            alert('Vous ne pouvez pas sélectionner plus de 4 indicateurs');
        }
    });
    
    function updateVisualization() {
        const countries = $('#countries').val();
        const indicators = $('#indicators').val();
        
        if (!countries || !indicators || countries.length === 0 || indicators.length === 0) {
            $('#welcome-message').show();
            $('#visualization').hide();
            $('#stats').empty();
            return;
        }
        
        const year = $('#year').val();
        const chartType = $('#chart-type').val();
        const selectedStats = $('input[name="statistics"]:checked').map(function() {
            return $(this).val();
        }).get();
        
        const GET_DATA_URL_DISTRIBUTE = "{% url 'Visualisation_app:get_distribution_data' %}";
        $.get(GET_DATA_URL_DISTRIBUTE, {
            countries: countries,
            indicators: indicators,
            year: year,
            statistics: selectedStats
        }, function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            $('#welcome-message').hide();
            $('#visualization').show();
            
            // Afficher les descriptions
            let descriptionsHtml = '';
            indicators.forEach(indicator => {
                if (response.descriptions[indicator]) {
                    descriptionsHtml += `
                        <div class="indicator-description">
                            <strong>${$('#indicators option[value="' + indicator + '"]').text()}</strong>: 
                            ${response.descriptions[indicator]}
                        </div>
                    `;
                }
            });
            $('#descriptions').html(descriptionsHtml);
            
            // Créer les graphiques
            $('#visualization').empty();
            const numIndicators = indicators.length;
            const columns = numIndicators <= 2 ? numIndicators : 2;
            
            indicators.forEach((indicator, index) => {
                const containerId = `chart-${indicator}`;
                $('#visualization').append(`<div id="${containerId}" class="chart-container"></div>`);
                
                const trace = {
                    values: response.data[indicator].values,
                    labels: response.data[indicator].labels,
                    type: chartType,
                    name: $('#indicators option[value="' + indicator + '"]').text()
                };
                
                if (chartType === 'bar') {
                    trace.type = 'bar';
                    trace.x = response.data[indicator].labels;
                    trace.y = response.data[indicator].values;
                }
                
                const layout = {
                    title: $('#indicators option[value="' + indicator + '"]').text(),
                    showlegend: true,
                    height: 400
                };
                
                Plotly.newPlot(containerId, [trace], layout);
            });
            
            // Mettre à jour les statistiques
            updateStats(response.stats, response.data);
        });
    }
    
    function updateStats(stats, data) {
        let html = '<h3>Statistiques</h3>';
        
        for (let indicator in stats) {
            const indicatorName = $('#indicators option[value="' + indicator + '"]').text();
            html += `
                <div class="indicator-stats" style="margin-bottom: 20px;">
                    <h4 style="color: #007bff;">${indicatorName}</h4>
                    <table style="width: 100%;">
            `;
                
            if (stats[indicator].mean !== null) {
                html += `<tr>
                    <td>Moyenne:</td>
                    <td>${stats[indicator].mean.toFixed(2)}</td>
                </tr>`;
            }
            
            if (stats[indicator].variance !== null) {
                html += `<tr>
                    <td>Variance:</td>
                    <td>${stats[indicator].variance.toFixed(2)}</td>
                </tr>`;
            }
            
            if (stats[indicator].percentage) {
                html += '<tr><td colspan="2"><strong>Parts en pourcentage:</strong></td></tr>';
                data[indicator].labels.forEach((label, index) => {
                    html += `<tr>
                        <td>${label}:</td>
                        <td>${stats[indicator].percentage[index].toFixed(2)}%</td>
                    </tr>`;
                });
            }
            
            html += '</table></div>';
        }
        
        $('#stats').html(html);
    }
    
    // Événements pour la mise à jour automatique
    $('#countries, #indicators, #year, #chart-type').on('change', updateVisualization);
    $('input[name="statistics"]').on('change', updateVisualization);
});