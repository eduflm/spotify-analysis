const router = require('express').Router()

module.exports = (app) => {
  app.use('/test', router)

  // Create a new product
  router.get('/', (req, res) => {
      return res.status(200).json("Tested!")
  })

}