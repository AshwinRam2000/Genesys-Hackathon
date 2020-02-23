
// const express = require('express');
// const VoiceResponse = require('twilio').twiml.VoiceResponse;

// const app = express();

// // Create a route that will handle Twilio webhook requests, sent as an
// // HTTP POST to /voice in our application
// app.post('/incoming', (request, response) => {
//   // Use the Twilio Node.js SDK to build an XML response
//   const twiml = new VoiceResponse();
//   twiml.say({ voice: 'alice' }, `Welcome to Genesys! We are pleased to serve you.
//   Please leave a message after the beep.`);

//   // twiml.record({ transcribe: true, maxLength: 10, recordingStatusCallback: "/record", playBeep: true })
//   twiml.gather({ input: 'dtmf speech', language: 'ta-IN', method: 'POST', action: '/record', timeout: 10 })
//   // Render the response as XML in reply to the webhook request
//   response.type('text/xml');
//   response.send(twiml.toString());
// });


// app.post('/record', (req, res) => {
//   console.log(req);
//   console.log(req.body, req.SpeechResult);
//   res.send("ok");
// })

// // Create an HTTP server and listen for requests on port 3000
// app.listen(5000, () => {
//   console.log(
//     'Now listening on port 5000. ' +
//     'Be sure to restart when you make code changes!'
//   );
// });

require("dotenv").config();
const express = require('express')
const dialogflow = require('dialogflow')
const client = require("twilio")(
  process.env.ACCOUNT_SID,
  process.env.AUTH_TOKEN
);
const VoiceResponse = require('twilio').twiml.VoiceResponse
const morgan = require('morgan')
const bodyParser = require('body-parser')

const app = express();

const port = process.env.PORT
const projectId = process.env.GCLOUD_PROJECT

const server = require('http').createServer(app);
const io = require('socket.io')(server);


// io.on('connection', (client) => {
//   console.log("Client connected on port 8080");
// })


server.listen(8080);
// Loggin
app.use(morgan('combined'))

// Body parsing
app.use(bodyParser.urlencoded({
  extended: true
}));

// Dialogflow integration
async function getAnswer(query, userId, type) {

  // A unique identifier for the given session based on phone number -to be encrypted..
  const sessionId = userId;

  // Create a new session
  const sessionClient = new dialogflow.SessionsClient()
  const sessionPath = sessionClient.sessionPath(projectId, sessionId)

  // Dialogflow request
  let request = {
    session: sessionPath,
    queryInput: {},
  };

  // Type text
  if (type === 'text') {
    request.queryInput.text = {
      text: query,
      languageCode: 'en-US',
    };
    // Type event
  } else {
    request.queryInput.event = {
      name: query,
      languageCode: 'en-US',
    };
  }

  // Send request
  const responses = await sessionClient.detectIntent(request)

  return responses[0].queryResult
}
var callData = null;
app.post('/twilio/hook', async (req, res, next) => {
  try {

    const { body } = req
    callData = body;
    let answer
    console.log(body);
    // Check if we received transcript or if it's start of conversation.
    if (body.CallStatus === 'ringing') {
      // Query Dialogflow
      answer = await getAnswer('Welcome', body.From, 'event')
    } else {
      // instead of directly giving body.SpeechResult, pass it to knowledgebaseapi and fetch matched query and send its responses
      answer = await getAnswer(body.SpeechResult, body.From, 'text')
    }

    // Prepare Twilio response (Twiml gather)
    const response = new VoiceResponse()
    const gather = response.gather({
      input: 'speech',
    });
    // console.log(answer);
    gather.say(answer.fulfillmentText)
    if (answer.fulfillmentText.includes("Oops") != -1) {
      io.emit("callComing", { data: body });

    }
    // Send response to Twilio
    res.type('text/xml')
    res.status(200)
      .send(response.toString())
      .end();

  } catch (error) {
    return next(error)
  }
})

app.post('/getContext', (req, res) => {
  console.log(req);
})

const ClientCapability = require('twilio').jwt.ClientCapability;
app.get('/token', (req, res) => {
  const capability = new ClientCapability({
    accountSid: process.env.ACCOUNT_SID,
    authToken: process.env.AUTH_TOKEN
  });
  capability.addScope(new ClientCapability.IncomingClientScope("Aravind"));
  const token = capability.toJwt();
  res.set('Content-Type', 'application/jwt');
  res.send(token);
})

app.post('/routeCall', (req, res) => {
  const twiml = new VoiceResponse();
  twiml.dial().client("Aravind");
  res.type('text/xml');
  res.send(twiml.toString());
})

app.post("/answerCall", (req, res) => {
  client.calls(req.body.id).update({
    url: "https://6ca794e3.ngrok.io/routeCall",
    method: "POST"
  }, (err, call) => {
    console.log(err);
    console.log(call);
  })
})
// Basic 404 handler
app.use((req, res) => {
  res.status(404).send('Not Found')
})

// Basic error handler
app.use((err, req, res, next) => {
  res.status(500).send(err.message || 'Something broke!')
})

// Start application
// app.listen(port, () => console.log(`App listening on port ${port}!`))
