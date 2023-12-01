import type { NextApiRequest, NextApiResponse } from 'next';
import prisma from '@/lib/prisma'; // adjust the import path as needed
import { getSession, useSession } from 'next-auth/react'
import { NextRequest } from 'next/server';
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url, { next: { revalidate: 60 }}).then((res) => res.json())

export async function GET(request: NextRequest) {
  const session = request.nextUrl.searchParams.get('userId')
  const { data } = useSWR(`/api/auth/session`, fetcher);
  console.log(data)
  
  try {
    if (session) {
      const provRaw = await prisma.account.findMany({ select: { provider: true } }, { where: {id: session }})
      
      const provArray = provRaw.map((prov: {provider: string}) => {
        return prov.provider
      })
      return Response.json(provArray);
    } else {
      return Response.json({ message: 'Unauthorized' })
    }
  } catch (error) {
    return Response.json({ message: 'Server error' });
  }
}