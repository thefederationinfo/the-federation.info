'use strict'

// Fetch platform metadata from the "next" repository at build time.
// The result is written to src/api/platform_metadata.json where it is
// bundled into the frontend. A snapshot of the file is committed, so
// when the download fails (offline build) the build keeps working with
// the last known data and this script only prints a warning.

const fs = require('fs')
const https = require('https')
const path = require('path')

const URL = 'https://codeberg.org/thefederationinfo/next/raw/branch/main/Metadata/platform_metadata.json'
const TARGET = path.join(__dirname, '../src/api/platform_metadata.json')
const MAX_REDIRECTS = 5

function get (url, redirects, cb) {
  https.get(url, res => {
    if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
      res.resume()
      if (redirects >= MAX_REDIRECTS) {
        cb(new Error('too many redirects'))
        return
      }
      get(new global.URL(res.headers.location, url).toString(), redirects + 1, cb)
      return
    }
    if (res.statusCode !== 200) {
      res.resume()
      cb(new Error('unexpected status ' + res.statusCode))
      return
    }
    let body = ''
    res.setEncoding('utf8')
    res.on('data', chunk => { body += chunk })
    res.on('end', () => cb(null, body))
  }).on('error', cb)
}

get(URL, 0, (err, body) => {
  if (!err) {
    try {
      const data = JSON.parse(body)
      if (!Array.isArray(data)) {
        err = new Error('expected a JSON array')
      } else {
        fs.writeFileSync(TARGET, JSON.stringify(data, null, 1) + '\n')
        console.log('platform metadata: updated from ' + URL)
        return
      }
    } catch (e) {
      err = e
    }
  }
  console.warn('platform metadata: download failed (' + err.message + '), using committed snapshot')
  if (!fs.existsSync(TARGET)) {
    console.error('platform metadata: no committed snapshot found at ' + TARGET)
    process.exit(1)
  }
})
