import postsData from "@/assets/fakedata/posts.json";
import type { Post } from "@/lib/models/post";
import { NextResponse } from "next/server";

export default async function GET() {
  const data: Post[] = postsData.objects;
  return NextResponse.json(data);
}
