import dotenv from 'dotenv';
import { MongoClient } from 'mongodb';

dotenv.config();
const uri = process.env.MONGODB_URI as string; // your MongoDB connection string

if (!uri) {
  throw new Error(`MONGODB_URI ${process.env} is not set`);
}

const options = {};

declare global {
  // eslint-disable-next-line no-var
  var _mongoClientPromise: Promise<MongoClient>;
}

class Singleton {
  private static _instance: Singleton;
  private client: MongoClient;
  private clientPromise: Promise<MongoClient>;
  private constructor() {
    this.client = new MongoClient(uri, options);
    this.clientPromise = this.client.connect();
    if (process.env.NODE_ENV === 'development') {
      // In development mode, use a global variable so that the value
      // is preserved across module reloads caused by HMR (Hot Module Replacement).
      globalThis._mongoClientPromise = this.clientPromise;
    }
  }

  public static get instance() {
    if (!this._instance) {
      this._instance = new Singleton();
    }
    return this._instance.clientPromise;
  }
}
const clientPromise = Singleton.instance;

// Export a module-scoped MongoClient promise. By doing this in a
// separate module, the client can be shared across functions.
export default clientPromise;