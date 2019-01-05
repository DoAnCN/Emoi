function lineChart(value,value2,value3){
    google.charts.load('current', {'packages':['line']});
    google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawChart2);
    google.charts.setOnLoadCallback(drawChart3);

    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Scan Time - WebClient');
      data.addColumn('number', 'Tx_Bytes');
      data.addColumn('number', 'Tx_Errors');
      data.addColumn('number', 'Rx_Bytes');
      data.addColumn('number', 'Rx_Errors');
      data.addRows(value);
      
      

      var options = {
        'height': '500',
        'legend':'bottom',
      };

      var chart = new google.charts.Line(document.getElementById('linechart'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }

    function drawChart2() {

      var data2 = new google.visualization.DataTable();
      data2.addColumn('string', 'Scan Time - Agent10');
      data2.addColumn('number', 'Tx_Bytes');
      data2.addColumn('number', 'Tx_Errors');
      data2.addColumn('number', 'Rx_Bytes');
      data2.addColumn('number', 'Rx_Errors');
      data2.addRows(value2);
      
      

      var options = {
        'height': '500',
        'legend':'bottom',
      };

      var chart = new google.charts.Line(document.getElementById('linechart2'));

      chart.draw(data2, google.charts.Line.convertOptions(options));
    }

    function drawChart3() {

      var data3 = new google.visualization.DataTable();
      data3.addColumn('string', 'Scan Time -Agent100');
      data3.addColumn('number', 'Tx_Bytes');
      data3.addColumn('number', 'Tx_Errors');
      data3.addColumn('number', 'Rx_Bytes');
      data3.addColumn('number', 'Rx_Errors');
      data3.addRows(value3);
      
      var options = {
        'height': '500',
        'legend':'bottom',
      };

      var chart = new google.charts.Line(document.getElementById('linechart3'));

      chart.draw(data3, google.charts.Line.convertOptions(options));
    }
    
}