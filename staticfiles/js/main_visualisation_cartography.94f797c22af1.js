$(document).ready(function() {
    $('.select2').select2({
        language: {
            noResults: function() {
                return "Aucun résultat trouvé";
            }
        }
    });

    const GET_MAP_DATA_URL = "{% url 'Visualisation_app:get_map_data' %}";

    function updateMap() {
        const indicator = $('#indicator').val();
        const countries = $('#countries').val();
        const year = $('#year').val();
        
        if (!indicator || !countries || countries.length === 0) {
            $('#welcome-message').show();
            $('#plotly-map').hide();
            $('#indicator-description').hide();
            return;
        }
        
        $.get(GET_MAP_DATA_URL, {
            indicator: indicator,
            countries: countries,
            year: year
        }, function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            const data = [{
                type: 'choropleth',
                locationmode: 'ISO-3',
                locations: Object.keys(response.data),
                z: Object.values(response.data).map(d => d.value),
                text: Object.values(response.data).map(d => 
                    `${d.name}<br>${response.indicator_name}: ${d.value}`
                ),
                colorscale: [
                    [0, 'rgb(240, 240, 255)'],  
                    [1, 'rgb(0, 0, 150)']       
                ],

                colorbar: {
                    title: response.indicator_name,
                    thickness: 20
                },
                name: '',
                showscale: true
            }];

            const layout = {
                title: `${response.indicator_name} en ${year}`,
                geo: {
                    scope: 'africa',
                    showframe: false,
                    showcoastlines: true,
                    projection: {
                        type: 'mercator'
                    }
                },
                //bgcolor: 'rgb(230, 255, 230)',  
                bgcolor : "lightgreen",
                //landcolor: 'rgb(240, 255, 240)',
                margin: {
                    l: 0,
                    r: 0,
                    b: 0,
                    t: 30,
                    pad: 4
                },
                paper_bgcolor: 'rgb(230, 255, 230)',  
                plot_bgcolor: 'lightgreen'
            };

            const config = {
                responsive: true,
                displayModeBar: true
            };
            
            $('#indicator-description').html(response.description).show();
            $('#welcome-message').hide();
            $('#plotly-map').show();
            
            Plotly.newPlot('plotly-map', data, layout, config);
        });
    }

    // Événements pour la mise à jour automatique
    $('#indicator, #countries, #year').on('change', updateMap);
});