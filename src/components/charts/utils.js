import gql from 'graphql-tag'

function getQuery(name) {
    return gql`
        query Stats($platform: String!) {
            ${name}(platform: $platform) {
                date
                count
            }
        }`
}

const lineChartTemplate = `
    <line-chart
        :data="statsData"
        :library="chartOptions"
    />    
`

// eslint-disable-next-line import/prefer-default-export
export {getQuery, lineChartTemplate}
