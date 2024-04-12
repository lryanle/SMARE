import { NextRequest } from "next/server";
import clientPromise from "@/lib/mongodb";

type Data = {
  success: boolean;
  data?: any[];
  error?: string;
};

async function getRecentListings(max: number) {
  try {
    const client = await clientPromise;
    const db = client.db("scrape");
    const listings = await db
      .collection("listings")
      .find({ stage: 'clean' })
      .sort({ scrape_date: -1 })
      .limit(max)
      .toArray();
    
    return listings;
  } catch (error) {
    throw error;
  }
}

export async function GET(request: NextRequest) {
  let max = parseInt(request.nextUrl.searchParams.get("max") as string);

  if (isNaN(max)) {
    max = 0;
  }

  try {
    const listings = await getRecentListings(max);
    return Response.json({ success: true, data: listings });
  } catch (error) {
    return Response.json({ success: false, error: error.message });
  }
}