function lineChart(value,value_packet){
    google.charts.load('current', {'packages':['line']});
    google.charts.setOnLoadCallback(drawChartNetWorkBytes);
    google.charts.setOnLoadCallback(drawChartNetworkPacktes);

    function drawChartNetWorkBytes() {

      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Scan Time');
      data.addColumn('number', 'Tx_Bytes');
      data.addColumn('number', 'Tx_Errors');
      data.addColumn('number', 'Rx_Bytes');
      data.addColumn('number', 'Rx_Errors');
      data.addRows(value);
      
      

      var options = {
        'height': '500',
        'legend':'bottom',
      };

      var chart = new google.charts.Line(document.getElementById('linechart_bytes'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }

    function drawChartNetworkPacktes() {

      var data_packet = new google.visualization.DataTable();
      data_packet.addColumn('string', 'Scan Time');
      data_packet.addColumn('number', 'Tx_Packets');
      data_packet.addColumn('number', 'Tx_Dropped');
      data_packet.addColumn('number', 'Rx_Packets');
      data_packet.addColumn('number', 'Rx_Dropped');
      data_packet.addRows(value_packet);
      
      

      var options = {
        'height': '500',
        'legend':'bottom',
      };

      var chart = new google.charts.Line(document.getElementById('linechart_packets'));

      chart.draw(data_packet, google.charts.Line.convertOptions(options));
    }
    
}