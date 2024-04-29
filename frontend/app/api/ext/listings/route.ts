import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';
export const fetchCache = 'force-no-store';
export const dynamic = "force-dynamic"
export const revalidate = 0;

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getCleanListingsWithLabel() {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');

    const pipeline = [
      {
        $match: {
          stage: 'clean',
          label: { $exists: true },
          "model_scores.model_3": { $ne: -1 }
        }
      },
      {
        $facet: {
          flagged: [
            { $match: { label: 'label-flagged' } },
            { $project: { _id: 1, title: 1, price: 1, odometer: 1, post_body: 1, year: 1, make: 1, model: 1, source: 1, images: 1 } }
          ],
          notflagged: [
            { $match: { label: 'label-notflagged' } },
            { $project: { _id: 1, title: 1, price: 1, odometer: 1, post_body: 1, year: 1, make: 1, model: 1, source: 1, images: 1 } }
          ],
        }
      }
    ];

    const result = await db.collection('listings').aggregate(pipeline).toArray();
    const listings = {
      flagged: result[0].flagged.map((item: any) => ({
        ...item,
        imageCount: item.images?.length
      })),
      notflagged: result[0].notflagged.map((item: any) => ({
        ...item,
        imageCount: item.images?.length
      }))
    };

    return listings;
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const listings = await getCleanListingsWithLabel();
    return new Response(JSON.stringify({ success: true, data: listings }), {
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
