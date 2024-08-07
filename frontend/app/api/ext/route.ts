import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';
export const fetchCache = 'force-no-store';
export const dynamic = "force-dynamic"
export const revalidate = 0;

type Data = {
  success: boolean;
  data?: any;
  error?: string;
};

async function getRandomCleanListing() {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');

    const results = await db.collection('listings').aggregate([
      {
        $match: {
          stage: 'clean',
          label: { $exists: false },
          "model_scores.model_3": { $ne: -1 }
        }
      },
      { $sample: { size: 1 } }
    ]).toArray();

    if (results.length > 0) {
      return results[0];
    } else {
      throw new Error('No suitable listing found');
    }
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const listing = await getRandomCleanListing();
    return new Response(JSON.stringify({ success: true, data: listing }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store, no-store, must-revalidate, max-age=0',
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({ success: false, error: error.message }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store, no-store, must-revalidate, max-age=0',
      }
    });
  }
}
