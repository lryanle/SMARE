import { MongoClient } from "mongodb";
import { faker } from "@faker-js/faker";
import dotenv from "dotenv";

dotenv.config();

const setup = async () => {
  let client;

  try {
    client = new MongoClient(process.env.MONGODB_URI);
    await client.connect();

    const hasData = await client
      .db("Test")
      .collection("users")
      .countDocuments();

    if (hasData) {
      console.log("Database already exists with data");
      client.close();
      return;
    }

    const records = [...Array(10)].map(() => {
      const [fName, lName] = faker.person.fullName().split(" ");
      const username = faker.internet.userName({ fName, lName });
      const email = faker.internet.email({ fName, lName });
      const image = faker.image.urlLoremFlickr({
        width: 640,
        height: 480,
        category: "people",
      });

      return {
        name: `${fName} ${lName}`,
        username,
        email,
        image,
        followers: 0,
        emailVerified: null,
      };
    });

    const insert = await client
      .db("Test")
      .collection("users")
      .insertMany(records);

    if (insert.acknowledged) {
      console.log("Successfully inserted records");
    }
  } catch (error) {
    return "Database is not ready yet";
  } finally {
    if (client) {
      await client.close();
    }
  }
};

try {
  setup();
} catch {
  console.warn("Database is not ready yet. Skipping seeding...");
}

export { setup };
