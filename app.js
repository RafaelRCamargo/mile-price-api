const express = require("express");
const app = express();

//Routes
const companies = require("./routes/companies");
app.use("/companies", companies);

//Index Route
app.use("/", (req, res, next) => {
  res.status(200).send({
    message: "index mile price api",
  });
});

//Export Routes
module.exports = app;
