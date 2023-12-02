import prisma from "@/lib/prisma";
import { MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const users = await prisma.user.findMany({
    select: {
      id: true,
    },
    take: 1,
  });

  return [
    {
      url: "https://smare.lryanle.com",
      lastModified: new Date(),
    },
    ...users.map((user: { id: any }) => ({
      url: `https://smare.lryanle.com/${user.id}`,
      lastModified: new Date(),
    })),
  ];
}
