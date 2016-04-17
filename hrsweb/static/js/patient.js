// Patient page js
// patientID:   Global variable set by flask


/**
 * Handles updates to the biometric type select entity
 */
function typeSelectHandler() {
    var type = $("select option:selected")[0].value;
    drawBiometrics(patientID, type);
}

/**
 * Resets the canvas HTML5 tag to clear the previous graph
 */
function resetCanvas() {
    if(window.lineGraph != null) 
        window.lineGraph.destroy();

    var chartWrapper = document.getElementById("canvas-wrapper");
    chartWrapper.innerHTML = '&nbsp';
    $('#canvas-wrapper').append('<canvas id="canvas"></canvas>');

    window.graphctx = $('#canvas').get(0).getContext('2d');
}

/**
 *  Resets and draws a line graph using the data provided
 *  @param data:    Graph data formatted as follows:
 *      {
 *          "value": [ <value1>, <value2>]
 *          "time":  [ <time1>, <time2> ]
 *          "units": <units>
 *      }
 */
function drawLineGraph(data, label) {
    resetCanvas();
    console.log(data);
    window.lineGraph = new Chart(window.graphctx).Line({
        labels : [],
        datasets : [
            {
                label: label,
                fillColor : "rgba(0,0,0,0)",
                strokeColor : "rgb(33,150,243)",
                pointColor : "rgba(33,150,243,1)",
                pointStrokeColor : "#fff",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(220,220,220,1)",
                data: []
            },
        ]
    },
    {
        responsive: true,
        tooltipTemplate: "<%=label%>: <%=value%> " + data.units,
    }); 

    var len = data.value.length
    for(var i=0; i<len; i++) {
        window.lineGraph.addData([data.value[i]], data.time[i]);
    }
    window.lineGraph.update();
}

/**
 *  Resets and draws a line graph with 2 datasets using the data provided
 *  for blood pressure
 *  @param data1:   Graph data for line 1
 *  @param data2:   Graph data for line 2
 */
function drawBPGraph(data1, data2, time) {
    resetCanvas();
    window.lineGraph = new Chart(window.graphctx).Line({
        labels : [],
        datasets : [
            {
                label: "Systolic Pressure",
                fillColor : "rgba(0,0,0,0)",
                strokeColor : "rgb(33,150,243)",
                pointColor : "rgba(33,150,243,1)",
                pointStrokeColor : "#fff",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(220,220,220,1)",
                data: []
            },
            {
                label: "Diastolic Pressure",
                fillColor : "rgba(0,0,0,0)",
                strokeColor : "rgba(229,28,35,1)",
                pointColor : "rgba(229,28,35,1)",
                pointStrokeColor : "#fff",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(220,220,220,1)",
                data: []
            },
        ]
    },
    {
        responsive: true,
        multiTooltipTemplate: "<%= label %> - <%= value %> mm Hg"
    }); 
    var len = data1.length

    for(var i=0; i<len; i++) {
        window.lineGraph.addData([data1[i], data2[i]], time[i]);
    }
    window.lineGraph.update();
}

/**
 * Fetch biometric data for this patient
 * @param patientID:        ID of the patient
 * @param biometricType:    Name of the biometric type
 */
function drawBiometrics(patientID, biometricType) {
    $.get("/api/biometrics", {
            patient_id: patientID,
            type: biometricType
        },
        function (response) {
            if (response) {
                var result = response.response;
                
                /**
                 * Handle splitting the bp data into 2 datasets
                 * From the database the data is stored as a fraction in a sting
                 * E.G:" 80/100"
                 */
                if (biometricType == "blood pressure") {
                    var data1 = []
                    var data2 = []

                    var len = result.value.length
                    for(var i=0; i<len; i++) {
                        var res = result.value[i].split("/")
                        data1[i] = res[0]
                        data2[i] = res[1]
                    }
                        
                    drawBPGraph(data1, data2, result.time, result.units)
                }
                else {
                    drawLineGraph(result, biometricType, result.units)
                }

            }
        },
        'json'
    );

}

// Entry point on load
window.onload = function() {

    /* Initialise elements */
    $('.button-collapse').sideNav({'edge' : 'left'});
    $('select').material_select();
    $('select').change(typeSelectHandler);

    /* Initialise chart */
    window.lineGraph = null
    drawBiometrics(patientID, 'height');
}

