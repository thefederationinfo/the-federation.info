function initChart(chartContainer, name, data) {
  var chart = new Rickshaw.Graph({
    element: chartContainer,
    renderer: 'line',
    series: [{
      name: name,
      color: 'steelblue',
      data: data
    }],
    height: 250
  });
  var axes = new Rickshaw.Graph.Axis.Time( { graph: chart } );
  var y_axis = new Rickshaw.Graph.Axis.Y( {
        graph: chart,
        orientation: 'left',
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: document.getElementById('y-axis'),
  });
  var hoverDetail = new Rickshaw.Graph.HoverDetail({
    graph: chart
  });

  chart.render();
  return chart;
}

function refreshChart(chart, name, data) {
  chart.series[0].name = name;
  chart.series[0].data = data;
  chart.render();
}
