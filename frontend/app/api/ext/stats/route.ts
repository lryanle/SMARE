import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';
import dynamic from "next/dynamic";
export const fetchCache = 'force-no-store';

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
            { $project: { _id: 1 } }
          ],
          notflagged: [
            { $match: { label: 'label-notflagged' } },
            { $project: { _id: 1 } }
          ],
          totalWithLabel: [
            { $count: "count" }
          ],
        }
      }
    ];

    const result = await db.collection('listings').aggregate(pipeline).toArray();
    const listings = {
      flagged: result[0].flagged.map((item: any) => item._id),
      notflagged: result[0].notflagged.map((item: any) => item._id)
    };

    const stats = {
      totalLabel: result[0].totalWithLabel[0].count ?? 0,
      totalFlagged: result[0].flagged.length ?? 0,
      totalNotFlagged: result[0].notflagged.length ?? 0,
    };


    return { listings, stats };
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const { listings, stats } = await getCleanListingsWithLabel();
    return new Response(JSON.stringify({ success: true, data: listings, stats: stats }), {
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
