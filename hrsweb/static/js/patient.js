// Patient page js
// patientID:   Global variable set by flask


/**
 * Handles updates to the biometric type select entity
 */
function typeSelectHandler() {
    var type = $("#typeSelect option:selected")[0].value;
    if (type == 'ecg') {
        $('#ecgSelectWrapper').show();
        ecgSelectHandler();
    } else {
        $('#ecgSelectWrapper').hide();
       drawBiometrics(patientID, type);
    }

}

/**
 * Handles updates to the ecg select entity
 */
function ecgSelectHandler() {
    var selected = $("#ecgSelect option:selected")[0].value;
    console.log(selected);
    drawECG(selected);
}


/**
 * Resets the canvas HTML5 tag to clear the previous graph
 */
function resetCanvas() {
    if(window.lineGraph != null) 
        window.lineGraph.destroy();
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

    // Chart data
    var data = {
        labels: data.time,
        datasets: [{
            label: label,
            fill: false,
            borderColor: "rgba(33,150,243,1)",
            data: data.value
        }]
    }

    // Chart options
    var options = {
        responsive: true,
        scales: {
            yAxis: [{
                scaleLabel: {
                    labelString: label
                }
            }]
        }
    }


    window.lineGraph = new Chart(window.graphctx, {
        type: 'line',
        data: data,
        options: options
    }); 
}

/**
 *  Resets and draws a line graph with 2 datasets using the data provided
 *  for blood pressure
 *  @param data1:   Graph data for line 1
 *  @param data2:   Graph data for line 2
 */
function drawBPGraph(data1, data2, time) {
    resetCanvas();

    // Chart data
    var data = {
        labels: time,
        datasets: [{
            label: "Systolic Pressure",
            fill: false,
            borderColor: "rgba(33,150,243,1)",
            data: data1
        },
        {
            label: "Diastolic Pressure",
            fill: false,
            borderColor : "rgba(229,28,35,1)",
            data: data2

        }]
    }

    // Chart options
    var options = {
        responsive: true,
        multiTooltipTemplate: "<%=datasetLabel%> - <%=value%> mm Hg",

        scales: {
            xAxis: [{
                scaleLabel: {
                    labelString: "mm Hg"
                }
            }]
        }
    }

    window.lineGraph = new Chart(window.graphctx, {
        type: 'line',
        data: data,
        options: options
    }); 
}

/**
 *  Resets and draws a line graph with an ECG datasets using the data provided
 *  @param data:   Graph data for ECG graph from api
 */
function drawECGGraph(data) {
    resetCanvas();

    // Chart data
    var data = {
        labels: Array.apply(null, Array(data.length)).map(function (_, i) {return i;}),
        datasets: [{
            label: "ECG",
            fill: false,
            borderColor: "rgba(33,150,243,1)",
            data: data
        }]
    }

    // Chart options
    var options = {
        responsive: true,
        tooltipTemplate: "<%=label%>: <%=value%> " + data.unit,
        title: {
            text: "ECG"
        },
        scales: {
            xAxis: [{
                scaleLabel: {
                    labelString: "mV"
                }
            }]
        }
    }


    window.lineGraph = new Chart(window.graphctx, {
        type: 'line',
        data: data,
        options: options
    }); 
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
                    var data1 = [];
                    var data2 = [];

                    var len = result.value.length;
                    for(var i=0; i<len; i++) {
                        var res = result.value[i].split("/");
                        data1[i] = res[0];
                        data2[i] = res[1];
                    }
                        
                    drawBPGraph(data1, data2, result.time, result.units);
                }
                else {
                    drawLineGraph(result, biometricType, result.units);
                }

            }
        },
        'json'
    );

}


/**
 * Fetch ecg data for a specific IDt
 * @param dataID:        ID of the ECG data record to draw
 */
function drawECG(dataID) {
    $.get("/api/ecgdata", {
            data_id: dataID,
        },
        function (response) {
            if (response) {
                var result = response.response;
                drawECGGraph(result);
            }

        },
        'json'
    );

}

// Entry point on load
window.onload = function() {

    /* Initialise core elements */
    $('.button-collapse').sideNav({'edge' : 'left'});
    $('#typeSelect').material_select();
    $('#typeSelect').change(typeSelectHandler);

    /* Initialise ECG selector */
    $('#ecgSelect').change(ecgSelectHandler);
    $('#ecgSelectWrapper').hide();

    /* Populate options */
    $.get("/api/ecg", {
            patient_id: patientID,
        },
        function (response) {
            if (response) {
                var result = response.response;
                var len = result.length;
                var select = $('#ecgSelect');

                for(var i=0; i<len; i++) {
                    var opt = document.createElement('option');
                    opt.value = result[i].id;
                    opt.innerHTML = result[i].timestamp;
                    select.append(opt);
                }
                select.material_select();
            }
        }, 'json'
     );

    /* Initialise chart */
    window.graphctx = $('#canvas').get(0).getContext('2d');
    window.lineGraph = null;
    drawBiometrics(patientID, 'height');
}

