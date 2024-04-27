import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getCleanListingsWithLabel() {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');

    const results = await db.collection('listings').find({
      stage: 'clean',
      label: { $exists: true }
    }).toArray();

    return results;
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const listings = await getCleanListingsWithLabel();
    return new Response(JSON.stringify({ success: true, data: listings }), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({ success: false, error: error.message }), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}
