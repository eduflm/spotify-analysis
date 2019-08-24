const router = require('express').Router()

const {createChartInfo} = require('../controllers/chart')

module.exports = (app) => {
    app.use('/chart', router)

    console.log("chegou")

    router.post('/', (req, res) => {
        createChartInfo(req.body).then(() => {
            return res.status(201).send("Ok!")
        }).catch((error) => {
            return res.status(400).json("Ocorreu um erro ao gravar o arquivo");
        })
  })
}