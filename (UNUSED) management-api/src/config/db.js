const mongoose = require('mongoose')

const { DB_HOST, DB_PORT, DB_NAME} = process.env

let mongoURI = ''

mongoURI = `mongodb://${DB_HOST}:${DB_PORT}/${DB_NAME}`

mongoose.Promise = global.Promise

module.exports = callback => {
  let db = mongoose.connect(mongoURI, {useNewUrlParser: true}).then(() => {
    console.log('Connected to database.')
  }, (e) => {
    console.log(`An error has ocurred: ${e}`)
  })
  callback(db)
}