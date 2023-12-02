import type { NextApiRequest, NextApiResponse } from "next";
import prisma from "@/lib/prisma"; // adjust the import path as needed
import { getSession, useSession } from "next-auth/react";
import { NextRequest } from "next/server";
import useSWR from "swr";

const fetcher = (url: string) =>
  fetch(url, { next: { revalidate: 60 } }).then((res) => res.json());

export async function GET(request: NextRequest) {
  const userId = request.nextUrl.searchParams.get("userId");
  const email = request.nextUrl.searchParams.get("email");
  const name = request.nextUrl.searchParams.get("name");

  const session = { userId: userId, name: name, email: email };

  try {
    if (session) {
      const provRaw = await prisma.account.findMany(
        { select: { provider: true } },
        { where: { id: session.userId } }
      );

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
