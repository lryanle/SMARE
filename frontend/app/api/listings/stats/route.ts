import { NextRequest } from "next/server";
import clientPromise from "@/lib/mongodb";
import { ObjectId } from "mongodb";

type Data = {
  success: boolean;
  data?: any;
  error?: string;
};

async function getStatistics() {
  const client = await clientPromise;
  const db = client.db("scrape");
  const collection = db.collection("listings");

  const now = new Date();
  const firstDayThisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  const firstDayLastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  const firstDayTwoMonthsAgo = new Date(now.getFullYear(), now.getMonth() - 2, 1);
  const yesterday = new Date(now);
  yesterday.setDate(now.getDate() - 1);

  // Convert dates to MongoDB ObjectId for comparison
  const objectIdThisMonth = ObjectId.createFromTime(firstDayThisMonth.getTime() / 1000);
  const objectIdLastMonth = ObjectId.createFromTime(firstDayLastMonth.getTime() / 1000);
  const objectIdTwoMonthsAgo = ObjectId.createFromTime(firstDayTwoMonthsAgo.getTime() / 1000);
  const objectIdYesterday = ObjectId.createFromTime(yesterday.getTime() / 1000);

  // Calculate all required statistics
  const totalListings = await collection.estimatedDocumentCount();
  const listingsThisMonth = await collection.countDocuments({ "_id": { "$gte": objectIdThisMonth } });
  const listingsLastMonth = await collection.countDocuments({ "_id": { "$gte": objectIdLastMonth, "$lt": objectIdThisMonth } });
  const listingsTwoMonthsAgo = await collection.countDocuments({ "_id": { "$gte": objectIdTwoMonthsAgo, "$lt": objectIdLastMonth } });

  const percentIncreaseThisMonth = calculatePercentIncrease(listingsLastMonth, listingsThisMonth);
  const percentIncreaseLastMonth = calculatePercentIncrease(listingsTwoMonthsAgo, listingsLastMonth);

  const riskScoreOver50 = await collection.countDocuments({ "risk_score": { "$gt": 50 } });
  const riskScoreOver50ThisMonth = await collection.countDocuments({ "risk_score": { "$gt": 50 }, "_id": { "$gte": objectIdThisMonth } });
  const riskScoreOver50LastMonth = await collection.countDocuments({ "risk_score": { "$gt": 50 }, "_id": { "$gte": objectIdLastMonth, "$lt": objectIdThisMonth } });

  const percentIncreaseRiskScoreThisMonth = calculatePercentIncrease(riskScoreOver50LastMonth, riskScoreOver50ThisMonth);

  const listingsToday = await collection.countDocuments({ "_id": { "$gte": ObjectId.createFromTime(now.getTime() / 1000) } });
  const listingsYesterday = await collection.countDocuments({ "_id": { "$gte": objectIdYesterday, "$lt": ObjectId.createFromTime(now.getTime() / 1000) } });

  const percentIncreaseToday = calculatePercentIncrease(listingsYesterday, listingsToday);

  return {
    totalListings,
    percentIncreaseThisMonth,
    percentIncreaseLastMonth,
    riskScoreOver50,
    percentIncreaseRiskScoreThisMonth,
    listingsThisMonth,
    listingsLastMonth,
    listingsToday,
    percentIncreaseToday
  };
}

function calculatePercentIncrease(previous: number, current: number) {
  return previous === 0 ? 0 : ((current - previous) / previous) * 100;
}

export async function GET(request: NextRequest) {
  try {
    const statistics = await getStatistics();
    return Response.json({ success: true, data: statistics });
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}