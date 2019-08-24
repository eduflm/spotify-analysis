const runDB = require('./db.js')
const router = require('express').Router()

const test = require('../routes/test')
const chart = require("../routes/chart")

runDB(db => {
    test(router, db)
    chart(router, db)
})

module.exports = router
