import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getListingsByMonth() {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');
    const twelveMonthsAgo = new Date();
    twelveMonthsAgo.setFullYear(twelveMonthsAgo.getFullYear() - 1);
    twelveMonthsAgo.setMonth(twelveMonthsAgo.getMonth() + 1);
    twelveMonthsAgo.setDate(1);
    twelveMonthsAgo.setHours(0, 0, 0, 0);
    const formattedDate = `${twelveMonthsAgo.getFullYear()}-${String(twelveMonthsAgo.getMonth() + 1).padStart(2, '0')}`;

    const results = await db.collection('listings').aggregate([
      {
        $match: {
          scrape_date: { $gte: formattedDate }
        }
      },
      {
        $project: {
          yearMonth: { $substr: ['$scrape_date', 0, 7] },
          count: { $literal: 1 }
        }
      },
      {
        $group: {
          _id: '$yearMonth',
          total: { $sum: '$count' }
        }
      },
      { $sort: { '_id': 1 } }
    ]).toArray();

    return results.map(({ _id, total }) => ({
      name: _id,
      total
    }));
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const data = await getListingsByMonth();
    return Response.json({ success: true, data });
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}