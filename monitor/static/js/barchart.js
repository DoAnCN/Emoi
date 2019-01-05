function barChart(barvalue){
    console.log(barvalue);
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Agent');
    data.addColumn('number', 'Usage');
    data.addColumn('number', 'Free');
    data.addRows(barvalue);

    var options_stacked = {
        isStacked: true,
        height: 300,
        legend: {position: 'top', maxLines: 10},
        hAxis: {minValue: 0}
      };
  

    var chart = new google.visualization.ColumnChart(document.getElementById('barchart'));

    google.visualization.events.addListener(chart, 'ready', afterDraw);

    chart.draw(data, options_stacked);

    }
    function afterDraw(){
        console.log('all done');
    }
}