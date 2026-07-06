const lineChartTemplate = `
    <div style="min-height: 300px;">
        <ApolloLoader :loading="$apollo.loading">
            <line-chart
                :data="statsData"
                :library="chartOptions"
            />
        </ApolloLoader>
    </div>
`;

// eslint-disable-next-line import/prefer-default-export
export { lineChartTemplate };
