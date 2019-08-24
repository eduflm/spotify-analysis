require("dotenv").config()
const express = require("express")
const bodyParser = require("body-parser")
const router = require("./src/config/routes")

const app = express()
app.use(bodyParser.json())
app.use(router)

const port = process.env.PORT

app.listen(port, () => {
     console.log(`Listening on port ${port}`)
})

module.exports = app