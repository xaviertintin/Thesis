const MongoClient = require("mongodb").MongoClient;
const csvtojson = require("csvtojson");
const fs = require("fs");

let uri = process.env.MONGO_DB_URI;
let client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

async function processCSV() {
  try {
    await client.connect();
    const database = client.db("collect");
    const collection = database.collection("transactions");

    let csvFilePath = "/data/transactions.csv";
    const jsonArray = await csvtojson().fromFile(csvFilePath);

    await collection.insertMany(jsonArray);
    console.log("Data inserted to MongoDB");
  } finally {
    await client.close();
  }
}

processCSV().catch(console.error);
