function updateVisualization() {
    const country = $('#country').val();
    const indicators = $('#indicators').val();
    const selectedStats = $('input[name="statistics"]:checked').map(function() {
        return this.value;
    }).get();
    
    if (!country || !indicators || indicators.length === 0) {
        $('#welcome-message').show();
        $('#charts-grid').hide();
        $('#stats-container').empty();
        return;
    }
    
    const startYear = $('#start-year').val();
    const endYear = $('#end-year').val();
    
    
    $.get(GET_DATA_URL_INDICATOR, {
        country: country,
        indicators: indicators,
        start_year: startYear,
        end_year: endYear,
        statistics: selectedStats
    }, function(response) {
        if (response.error) {
            alert(response.error);
            return;
        }
        
        updateCharts(response.data);
        updateStats(response.stats);
        
        $('#welcome-message').hide();
        $('#charts-grid').show();
    });
}




function updateCharts(data) {
    const numIndicators = Object.keys(data).length;
    const chartsGrid = $('#charts-grid');
    chartsGrid.empty();
    
    // Définir la disposition de la grille en fonction du nombre d'indicateurs
    if (numIndicators <= 2) {
        chartsGrid.css('grid-template-columns', '1fr');
    } else {
        chartsGrid.css('grid-template-columns', '1fr 1fr');
    }
    
    // Créer un conteneur pour chaque graphique
    Object.keys(data).forEach((indicatorId, index) => {
        const chartDiv = $('<div>')
            .addClass('chart-container')
            .attr('id', `chart-${index}`)
            .appendTo(chartsGrid);
        
        const indicatorData = data[indicatorId];
        
        const trace = {
            x: indicatorData.years,
            y: indicatorData.values,
            type: 'scatter',
            mode: 'lines+markers',
            name: indicatorData.name
        };
        
        const layout = {
            title: indicatorData.name,
            xaxis: { title: 'Année' },
            yaxis: { title: indicatorData.name },
            margin: { t: 30 },
            height: 400
        };
        
        Plotly.newPlot(`chart-${index}`, [trace], layout, {
            responsive: true
        });
    });
}



function updateStats(stats) {
    let html = '<h3>Statistiques</h3>';
    
    const statNames = {
        'mean': 'Moyenne',
        'std': 'Écart-type',
        'var': 'Variance',
        'median': 'Médiane',
        'seasonality': 'Saisonnalité',
        'skewness': 'Asymétrie',
        'kurtosis': 'Aplatissement'
    };
    
    for (let indicatorId in stats) {
        const indicatorName = $(`#indicators option[value="${indicatorId}"]`).text();
        html += `
            <div class="indicator-stats" style="margin-bottom: 20px;">
                <h4 style="color: #007bff;">${indicatorName}</h4>
                <table style="width: 100%;">
        `;
        
        for (let statKey in stats[indicatorId]) {
            const value = stats[indicatorId][statKey];
            if (value !== null && value !== undefined) {
                const formattedValue = typeof value === 'number' ? value.toFixed(2) : value;
                html += `
                    <tr>
                        <td><strong>${statNames[statKey]}:</strong></td>
                        <td style="text-align: right;">${formattedValue}</td>
                    </tr>
                `;
            }
        }
        
        html += '</table></div>';
    }
    
    $('#stats-container').html(html);
}