// Patient page js
// patientID:   Global variable set by flask


function randomScalingFactor() {
    return Math.round(Math.random()*100);
}

var charConfig = {
    labels : [],
    datasets : [
        {
            label: "Dataset",
            fillColor : "rgba(220,220,220,0.2)",
            strokeColor : "rgba(220,220,220,1)",
            pointColor : "rgba(220,220,220,1)",
            pointStrokeColor : "#fff",
            pointHighlightFill : "#fff",
            pointHighlightStroke : "rgba(220,220,220,1)",
            data: []
        },
    ]
}

/**
 * Fetch biometric data for this patient
 */
function getBiometrics(patientID, biometricTypeID) {
    $.get("/api/biometrics", {
            patient_id: patientID,
            biometric_type_id: biometricTypeID
        },
        function (response) {
            if (response) {
                var result = response.response;
                var len = result.value.length
                for(var i=0; i<len; i++) {
                    window.lineGraph.addData([result.value[i]], result.time[i]);
                }
                window.lineGraph.update();
            }
        },
        'json'
    );

}

// Static data
var staticData =  [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    //var biometricData = staticData
    
    window.lineGraph = new Chart(ctx).Line(charConfig, {
        responsive: true
    });

    var biometricData = getBiometrics(patientID, 0);
}

