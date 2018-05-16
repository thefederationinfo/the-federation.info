import gql from 'graphql-tag'

function getQuery(name) {
    return gql`
        query Stats($type: String!, $value: String!) {
            ${name}(itemType: $type, value: $value) {
                date
                count
            }
        }`
}

const lineChartTemplate = `
    <div style="min-height: 300px;">
        <ApolloLoader :loading="$apollo.loading">
            <line-chart
                :data="statsData"
                :library="chartOptions"
            />
        </ApolloLoader>
    </div>
`

// eslint-disable-next-line import/prefer-default-export
export {getQuery, lineChartTemplate}
