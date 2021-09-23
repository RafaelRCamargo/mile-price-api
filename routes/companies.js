const express = require("express");
const router = express.Router();

//Firebase app
var firebase = require("firebase/app");

//Require firebase
var realtime = require("firebase/database");

//Firebase config
const app = firebase.initializeApp({
  apiKey: "AIzaSyCeJTmYPQUFodrvW23tNE4mDog0V6-UjPM",
  authDomain: "mile-price-bot.firebaseapp.com",
  databaseURL: "https://mile-price-bot-default-rtdb.firebaseio.com",
  projectId: "mile-price-bot",
  storageBucket: "mile-price-bot.appspot.com",
  messagingSenderId: "688116496009",
  appId: "1:688116496009:web:0fb129b25cd1d0c00f3858",
  measurementId: "G-X6FJE0M4LN",
});

router.get("/:company", (req, res, next) => {
  //Url company name
  const company = req.params.company;

  //Database reference
  const dbRef = realtime.ref(realtime.getDatabase());

  //Database get
  realtime.get(realtime.child(dbRef, `${company.toLowerCase()}`)).then((snapshot) => {
    //Check if that company exists in the db
    if (snapshot.exists()) {
      //Const 1k miles price
      const price = snapshot.val().pre / snapshot.val().quantity 
      
      //Response Data
      res.status(200).send({
        "company": company,
        "quantity": snapshot.val().quantity,
        "prices": {
          "pre": snapshot.val().pre,
          "pos": snapshot.val().pos,
          "1k": price
        }
      });  
    } else {
      //Response Not Found
      res.status(404).send({
        company: undefined
      });    
    } 
  }).catch((error) => { //Catch Error
    //Response Error
    res.status(500).send({
      error: error,
    });
  });  
});

//Response Index
router.get("/", (req, res, next) => {
  res.status(200).send({
    company: undefined,
  });
});

module.exports = router;
