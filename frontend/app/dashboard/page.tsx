/* eslint-disable new-cap */
import { authOptions } from "@/app/api/auth/[...nextauth]/authOptions";
import { Metadata } from "next";
import { getServerSession } from "next-auth/next";

import Dashboard from "@/components/dashboard/dashboard";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Dashboard | Statefarm SMARE",
  description: "Listing Dashboard to view and manage risky marketplace listings.",
};

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);
  if (!session) {
    redirect("/api/auth/signin");
  }

  return (
    session && (
      <div className="md:py-24 md:w-10/12">
        <div className="bg-whitehidden flex-col md:flex">
          <Dashboard />
        </div>
      </div>
    )
  );
}
