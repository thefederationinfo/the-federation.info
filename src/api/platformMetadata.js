// Enrich platform objects from the DB with metadata maintained in the
// "next" repository. The JSON file is downloaded at build time (see
// build/fetch-platform-metadata.js) and bundled. When the JSON carries
// a non empty value for a field, it wins over the DB value.

import metadata from './platform_metadata.json'

const byName = {}
metadata.forEach((entry) => {
    byName[entry.name.toLowerCase()] = entry
})

// Maps frontend/DB field name to metadata JSON field name
const fields = {
    display_name: 'display_name',
    description: 'description',
    website: 'website_url',
    code: 'sourcecode_url',
    license: 'license',
    install_guide: 'install_guide_url',
}

export default function enrichPlatform(platform) {
    if (!platform || !platform.name) {
        return platform
    }
    const meta = byName[platform.name.toLowerCase()]
    if (!meta) {
        return platform
    }
    const enriched = {...platform}
    Object.keys(fields).forEach((key) => {
        if (meta[fields[key]]) {
            enriched[key] = meta[fields[key]]
        }
    })
    return enriched
}
