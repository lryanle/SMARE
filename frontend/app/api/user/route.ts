import type { NextApiRequest, NextApiResponse } from "next";
import prisma from "@/lib/prisma";
import { NextRequest } from "next/server";

const fetcher = (url: string) =>
  fetch(url, { next: { revalidate: 60 } }).then((res) => res.json());

export async function GET(request: NextRequest) {
  const userId = request.nextUrl.searchParams.get("userId");
  const email = request.nextUrl.searchParams.get("email");
  const name = request.nextUrl.searchParams.get("name");
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

  // Normalize and format the dates
  const beforeDate = before ? new Date(before) : new Date();
  beforeDate.setUTCHours(0, 0, 0, 0);
  const afterDate = after ? new Date(after) : new Date();
  afterDate.setUTCHours(23, 59, 59, 999);
  
  const session = { userId: userId, name: name, email: email };

  try {
    if (session) {
      const provRaw = await prisma.account.findMany({
        select: { provider: true },
        where: {
          id: session.userId,
          createdAt: {
            gte: afterDate,
            lte: beforeDate,
          },
        },
      });

      const provArray = provRaw.map((prov: { provider: string }) => {
        return prov.provider;
      });

      return Response.json({ name: name, providers: provArray, email: email });
    } else {
      return Response.json(session);
    }
  } catch (error) {
    return Response.json({ message: "Server error" });
  }
}
