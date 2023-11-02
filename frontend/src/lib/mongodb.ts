import dotenv from "dotenv";
import { MongoClient, MongoClientOptions } from "mongodb";

dotenv.config();
const uri = process.env.MONGODB_URI as string; // your MongoDB connection string

if (!uri) {
  throw new Error(`MONGODB_URI ${process.env} is not set`);
}

const options: MongoClientOptions = {};

let client
let clientPromise: Promise<MongoClient>

if (process.env.NODE_ENV === "development") {
  // In development mode, use a global variable so that the value
  // is preserved across module reloads caused by HMR (Hot Module Replacement).
  if (!global._mongoClientPromise) {
    client = new MongoClient(uri, options)
    global._mongoClientPromise = client.connect()
  }
  clientPromise = global._mongoClientPromise
} else {
  // In production mode, it's best to not use a global variable.
  client = new MongoClient(uri, options)
  clientPromise = client.connect()
}

export default clientPromise
