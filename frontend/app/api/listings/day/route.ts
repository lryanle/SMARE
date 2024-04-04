import { NextRequest } from "next/server";
import clientPromise from '@/lib/mongodb';

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getListingsByDay(before?: string, after?: string) {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');
   
    // Normalize and format the dates
    const beforeDate = before ? new Date(before) : new Date();
    beforeDate.setUTCHours(0, 0, 0, 0);
    const afterDate = after ? new Date(after) : new Date();
    afterDate.setUTCHours(23, 59, 59, 999);

    const formattedBeforeDate = beforeDate.toISOString();
    const formattedAfterDate = afterDate.toISOString();

    const results = await db.collection('listings').aggregate([
      {
        $match: {
          scrape_date: {
            $gte: formattedAfterDate,
            $lte: formattedBeforeDate
          }
        }
      },
      {
        $project: {
          convertedDate: {
            $dateFromString: {
              dateString: '$scrape_date',
            }
          },
          flagged: 1,
          count: { $literal: 1 }
        }
      },
      {
        $project: {
          yearMonthDay: { 
            $dateToString: { format: "%Y-%m-%d", date: "$convertedDate" }
          },
          flagged: 1, 
          count: 1
        }
      },
      {
        $group: {
          _id: '$yearMonthDay',
          total: { $sum: '$count' },
          flaggedTrue: { 
            $sum: {
              $cond: [{ $eq: ['$flagged', true] }, 1, 0]
            }
          },
          flaggedFalse: {
            $sum: {
              $cond: [{ $ne: ['$flagged', true] }, 1, 0]
            }
          }
        }
      },
      { $sort: { '_id': 1 } }
    ]).toArray();

    return results.map(({ _id, total, flaggedTrue, flaggedFalse }) => ({
      name: _id,
      total,
      flaggedTrue,
      flaggedFalse
    }));
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    
    let before = request.nextUrl.searchParams.get("before");
    let after = request.nextUrl.searchParams.get("after");

    // default to before today
    if (!before) {
      before = new Date().toISOString();
    }

    // default to after 1 year ago
    if (!after) {
      const oneYearAgo = new Date();
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
      after = oneYearAgo.toISOString();
    }

    const data = await getListingsByDay(before, after);
    return Response.json({ success: true, data, before, after});
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}