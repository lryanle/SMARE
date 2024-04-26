export const dynamic = 'force-dynamic'
import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getTopMakeModels() {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');

    const results = await db.collection('listings').aggregate([
      {
        $match: {
          stage: 'clean',
          risk_score: { $gte: 50 }
        }
      },
      {
        $group: {
          _id: { make: '$make', model: '$model' },
          count: { $sum: 1 }
        }
      },
      {
        $sort: { count: -1 }
      }
    ]).toArray();

    return results.map(({ _id, count }) => ({
      make: _id.make,
      model: _id.model,
      count
    }));
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const data = await getTopMakeModels();
    return Response.json({ success: true, data });
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}
