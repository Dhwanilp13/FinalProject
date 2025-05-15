// this function executes our search via an AJAX call
function runSearch() {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    $('#loading').show();

    // Get form data
    var data = {
        sequence: $('#sequence').val(),
        search_term: $('#search_term').val(),
        source_db: $('#source_db').val()
    };
    
    console.log('Sending data:', data);

    $.ajax({
        url: './gene_finder.cgi',
        dataType: 'json',
        data: data,
        success: function(data, textStatus, jqXHR) {
            $('#loading').hide();
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#loading').hide();
            console.log('Error response:', jqXHR.responseText);
            alert("Failed to perform gene search: " + errorThrown);
        }
    });
}

// this processes a passed JSON structure representing gene matches
function processJSON(data) {
    console.log('Processing results:', data);
    
    if (data.error) {
        alert(data.error);
        return;
    }

    // Update match count
    $('#match_count').text(data.match_count);
    
    // iterate over each match and add a row to the result table for each
    $.each(data.matches, function(i, item) {
        var row = $('<tr/>');
        
        // add cells in the correct order matching the HTML table headers
        $('<td/>').text(item.id).appendTo(row);
        $('<td/>').text(item.name).appendTo(row);
        $('<td/>').text(item.class).appendTo(row);
        $('<td/>').text(item.mechanism).appendTo(row);
        $('<td/>').text(item.source).appendTo(row);
        $('<td/>').text(item.identity_percentage + '%').appendTo(row);
        $('<td/>').text(item.match_position).appendTo(row);
        // Create sequence cell with scrolling
        $('<td/>').addClass('sequence-cell').text(item.sequence).appendTo(row);
        
        row.appendTo('tbody');
    });
    
    // show results section
    $('#results').show();
}

// run our javascript once the page is ready
$(document).ready(function() {
    console.log('Page ready');
    
    // Set up autocomplete for gene search
    $('#search_term').autocomplete({
        source: function(request, response) {
            console.log('Autocomplete request:', request.term);
            
            $.ajax({
                url: './gene_finder.cgi',
                dataType: 'json',
                data: {
                    search_term: request.term,
                    source_db: $('#source_db').val()
                },
                success: function(data) {
                    console.log('Autocomplete response:', data);
                    if (data.matches) {
                        response(data.matches.map(function(item) {
                            return {
                                label: item.name,
                                value: item.name
                            };
                        }));
                    }
                }
            });
        },
        minLength: 2
    });

    // Handle form submission
    $('#gene_finder').submit(function(e) {
        e.preventDefault();
        var sequence = $('#sequence').val();
        if (!sequence) {
            alert('Please enter a DNA sequence');
            return;
        }
        runSearch();
    });
});