export const dynamic = 'force-dynamic'
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
    beforeDate.setUTCHours(23, 59, 59, 999);
    beforeDate.setDate(beforeDate.getDate() - 1);
    const afterDate = after ? new Date(after) : new Date();
    afterDate.setUTCHours(0, 0, 0, 0);
    afterDate.setDate(afterDate.getDate() - 1);

    const formattedBeforeDate = beforeDate.toISOString();
    const formattedAfterDate = afterDate.toISOString();

    console.log('formattedBeforeDate', formattedBeforeDate, 'formattedAfterDate', formattedAfterDate);

    const results = await db.collection('listings').aggregate([
      {
        $match: {
          scrape_date: {
            $gte: formattedAfterDate,
            $lte: formattedBeforeDate
          },
          stage: 'clean'
        }
      },
      {
        $project: {
          convertedDate: {
            $dateFromString: {
              dateString: '$scrape_date',
            }
          },
          risk_score: 1,
          human_flag: 1,
          count: { $literal: 1 }
        }
      },
      {
        $project: {
          yearMonthDay: { 
            $dateToString: { format: "%Y-%m-%d", date: "$convertedDate" }
          },
          risk_score: 1,
          human_flag: 1,
          count: 1
        }
      },
      {
        $group: {
          _id: '$yearMonthDay',
          flaggedTrue: { 
            $sum: {
              $cond: [
                { $or: [{ $gte: ['$risk_score', 50] }, { $eq: ['$human_flag', true] }] },
                1, 
                0
              ]
            }
          },
          flaggedFalse: {
            $sum: {
              $cond: [{ $or: [{ $lt: ['$risk_score', 50] }, { $ne: ['$human_flag', true] }] }, 1, 0]
            }
          }
        }
      },
      {
        $project: {
          total: { $add: ['$flaggedTrue', '$flaggedFalse'] },
          flaggedTrue: 1,
          flaggedFalse: 1
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
      const tempbeforedate = new Date()
      tempbeforedate.setUTCHours(23, 59, 59, 999)
      before = tempbeforedate.toISOString();
    }

    // default to after 1 year ago
    if (!after) {
      const oneYearAgo = new Date();
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
      after = oneYearAgo.toISOString();
    }

    // Normalize the dates
    const before2 = new Date(before)
    before2.setUTCHours(23, 59, 59, 999)

    const after2 = new Date(after)
    after2.setUTCHours(0, 0, 0, 0)

    const data = await getListingsByDay(before2.toISOString(), after2.toISOString());

    return Response.json({ success: true, data, before, after});
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}