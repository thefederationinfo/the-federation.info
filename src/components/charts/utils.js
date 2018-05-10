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
    <ApolloLoader>
        <line-chart
            :data="statsData"
            :library="chartOptions"
        />
    </ApolloLoader>
`

// eslint-disable-next-line import/prefer-default-export
export {getQuery, lineChartTemplate}
