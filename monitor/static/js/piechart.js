function pieChart(valuepie){
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  // Draw the chart and set the chart values
  function drawChart() {
    console.log(valuepie);
    var data = google.visualization.arrayToDataTable(
     valuepie
      );

  // var data = google.visualization.arrayToDataTable([
  //   ['Task', 'Hours per Day'],
  //   ['Work', 8],
  //   ['Eat', 5],
  //   ['TV', 4],
  //   ['Gym', 2],
  //   ]);
    

  // Optional; add a title and set the width and height of the chart
  var options = {
    'legend':'bottom',
    'title':'My Big Pie Chart',
    'is3D':true,
    'height':500
  }

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechart'));
  chart.draw(data, options);
  }
}
