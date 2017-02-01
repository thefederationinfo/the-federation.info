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
  chart.render();
  return chart;
}

function refreshChart(chart, data) {
  chart.series[0].data = data;
  chart.render();
}
