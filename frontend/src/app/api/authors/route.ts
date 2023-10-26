import authorsData from "@/assets/fakedata/authors.json";
import type { Author } from "@/lib/models/author";
import { NextResponse } from "next/server";

export default async function GET() {
  const data: Author[] = authorsData.objects;
  return NextResponse.json(data);
}
