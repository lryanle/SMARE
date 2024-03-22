import { NextRequest } from "next/server";
import clientPromise from "@/lib/mongodb";

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getRecentListings() {
  try {
    const client = await clientPromise;
    const db = client.db("scrape");
    const listings = await db
      .collection("listings")
      .find({})
      .sort({ scrape_date: -1 })
      .limit(50)
      .toArray();
    
    return listings;
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  try {
    const listings = await getRecentListings();
    return Response.json({ success: true, data: listings });
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}