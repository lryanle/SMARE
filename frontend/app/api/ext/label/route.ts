import { NextRequest, NextResponse } from "next/server";
import clientPromise from '@/lib/mongodb';
import { ObjectId } from "mongodb";
import dynamic from "next/dynamic";

type Data = {
  success: boolean;
  error?: string;
};

async function updateListingLabel(listingId: ObjectId, label: string) {
  try {
    const client = await clientPromise;
    const db = client.db('scrape');

    let updateDoc;

    if (label === 'remove') {
      updateDoc = { $unset: { label: "" } };
    } else if (['label-flagged', 'label-notflagged'].includes(label)) {
      updateDoc = { $set: { label: label } };
    } else {
      throw new Error("Invalid label value provided.");
    }

    const result = await db.collection('listings').updateOne(
      { _id: listingId },
      updateDoc
    );

    if (result.matchedCount === 0) {
      throw new Error("No listing found with the provided ID.");
    }

    return;
  } catch (error) {
    throw error;
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { listingId, label } = body;
    const extensionSecret = request.headers.get('secret');

    if (extensionSecret !== process.env.EXTENSION_SECRET) {
      throw new Error("Invalid extension secret.");
    }

    if (!listingId || !label) {
      throw new Error("Missing listingId or label in the request body.");
    }

    await updateListingLabel(listingId, label);
    return new Response(JSON.stringify({ success: true }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store, max-age=0',
      },
      status: 200
    });
  } catch (error) {
    return new Response(JSON.stringify({ success: false, error: error.message }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store, max-age=0',
      },
      status: 400
    });
  }
}
