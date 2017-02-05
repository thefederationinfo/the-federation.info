function initChart(chartContainer, data) {
  var chart = new Rickshaw.Graph({
    element: chartContainer,
    renderer: 'line',
    series: [ {
            color: 'steelblue',
            data: data
    } ],
    height: 250
  });
  var axes = new Rickshaw.Graph.Axis.Time( { graph: chart } );
  var y_axis = new Rickshaw.Graph.Axis.Y( {
        graph: chart,
        orientation: 'left',
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: document.getElementById('y-axis'),
  });

  chart.render();
  return chart;
}

function refreshChart(chart, data) {
  chart.series[0].data = data;
  chart.render();
}
