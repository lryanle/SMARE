import { NextRequest } from "next/server";
import clientPromise from "@/lib/mongodb";
import { ObjectId } from "mongodb";

type Data = {
  success: boolean;
  data?: any;
  error?: string;
};

function getMongoFormattedDate(date: Date) {
  return date.toISOString();
}

function calculatePercentIncrease(previous: number, current: number) {
  return previous === 0 ? current*100 : ((current - previous) / previous + 0.000000001) * 100;
}

function startOfWeek(date: Date) {
  const diff = date.getDate() - date.getDay() + (date.getDay() === 0 ? -6 : 0);
  return new Date(date.setDate(diff));
}

async function getStatistics() {
  const client = await clientPromise;
  const db = client.db("scrape");
  const collection = db.collection("listings");

  const now = new Date();
  const firstDayThisMonth = getMongoFormattedDate(new Date(now.getFullYear(), now.getMonth(), 1));
  const firstDayLastMonth = getMongoFormattedDate(new Date(now.getFullYear(), now.getMonth() - 1, 1));
  const firstDayTwoMonthsAgo = getMongoFormattedDate(new Date(now.getFullYear(), now.getMonth() - 2, 1));
  const yesterday = getMongoFormattedDate(new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1, 0, 0, 0 ,0));
  const today = getMongoFormattedDate(new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0 ,0));
  const startOfThisWeek = getMongoFormattedDate(startOfWeek(new Date(now.getFullYear(), now.getMonth(), now.getDate())));

  // Calculate all required statistics
  const totalListings = await collection.estimatedDocumentCount();
  const listingsThisMonth = await collection.countDocuments({ "scrape_date": { "$gte": firstDayThisMonth } });
  const listingsLastMonth = await collection.countDocuments({ "scrape_date": { "$gte": firstDayLastMonth, "$lt": firstDayThisMonth } });
  const listingsTwoMonthsAgo = await collection.countDocuments({ "scrape_date": { "$gte": firstDayTwoMonthsAgo, "$lt": firstDayLastMonth } });

  const percentIncreaseThisMonth = calculatePercentIncrease(listingsLastMonth, listingsThisMonth);
  const percentIncreaseLastMonth = calculatePercentIncrease(listingsTwoMonthsAgo, listingsLastMonth);

  const riskScoreOver50 = await collection.countDocuments({ "risk_score": { "$gt": 50 } });
  const riskScoreOver50ThisMonth = await collection.countDocuments({ "risk_score": { "$gt": 50 }, "scrape_date": { "$gte": firstDayThisMonth } });
  const riskScoreOver50LastMonth = await collection.countDocuments({ "risk_score": { "$gt": 50 }, "scrape_date": { "$gte": firstDayLastMonth, "$lt": firstDayThisMonth } });

  const percentIncreaseRiskScoreThisMonth = calculatePercentIncrease(riskScoreOver50LastMonth, riskScoreOver50ThisMonth);

  const listingsToday = await collection.countDocuments({ "scrape_date": { "$gte": today } });
  const listingsYesterday = await collection.countDocuments({ "scrape_date": { "$gte": yesterday, "$lt": today } });

  const listingsThisWeek = await collection.countDocuments({ "scrape_date": { "$gte": startOfThisWeek } });

  return {
    totalListings,
    percentIncreaseThisMonth,
    percentIncreaseLastMonth,
    riskScoreOver50,
    percentIncreaseRiskScoreThisMonth,
    listingsThisMonth,
    listingsLastMonth,
    listingsToday,
    listingsThisWeek
  };
}

export async function GET(request: NextRequest) {
  try {
    const statistics = await getStatistics();
    return Response.json({ success: true, data: statistics });
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}