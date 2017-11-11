"use strict";

var Alex = require("alexa-sdk");

exports.handler = function(event, context, callback){
    var alexa = Alexa.handler(event, context, callback);
    alexa.registerHandlers(handlers);
    alexa.execute();
};

var states = {
  GETMEAL: "_GETMEAL";
  GETTEXT: "_GETTEXT";
};

// The handlers object tells Alexa how to handle various actions
var handlers = {
  "YesIntent" = function() {

  }

  "NoIntent" = function() {

  }

  "RequestMealPlan" = function() {

  }
};
