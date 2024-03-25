/* eslint-disable new-cap */
import { authOptions } from "@/app/api/auth/[...nextauth]/authOptions";
import { Metadata } from "next";
import { getServerSession } from "next-auth/next";

import { CalendarDateRangePicker } from "@/components/dashboard/date-range-picker";
import { Overview } from "@/components/dashboard/overview";
import { RecentListings } from "@/components/dashboard/recent-listings";
import DashboardCards from "@/components/dashboard/dashboard-cards";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
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
      <div className="py-24 w-10/12">
        <div className="bg-whitehidden flex-col md:flex">
          {/* <div className="border-b">
          <div className="flex h-16 items-center px-4">
            <TeamSwitcher />
            <MainNav className="mx-6" />
            <div className="ml-auto flex items-center space-x-4">
              <Search />
              <UserNav />
            </div>
          </div>
        </div> */}
          <div className="flex-1 space-y-4 p-8 pt-6">
            <div className="flex flex-col md:flex-row justify-center items-center md:justify-between text-center md:text-left space-y-2">
              <h2 className="text-3xl font-bold tracking-tight">
                Marketplace Listings Dashboard
              </h2>
              <div className="flex items-center space-x-2">
                <CalendarDateRangePicker />
                <Button>Download</Button>
              </div>
            </div>
            <Tabs
              defaultValue="overview"
              className="space-y-4 flex-col md:flex-row"
            >
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="analytics" disabled>
                  Analytics
                </TabsTrigger>
                <TabsTrigger value="reports" disabled>
                  Reports
                </TabsTrigger>
                <TabsTrigger value="notifications" disabled>
                  Notifications
                </TabsTrigger>
                <TabsTrigger value="search" disabled>
                  Search
                </TabsTrigger>
              </TabsList>
              <TabsContent value="overview" className="space-y-4">
                <DashboardCards />
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                  <Card className="col-span-4">
                    <CardHeader>
                      <CardTitle>Overview</CardTitle>
                    </CardHeader>
                    <CardContent className="pl-2">
                      <Overview />
                    </CardContent>
                  </Card>
                  <Card className="col-span-3">
                    <CardHeader>
                      <CardTitle>Recent Listings</CardTitle>
                      <CardDescription>
                        8 listings flagged in the last 24 hours
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <RecentListings />
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    )
  );
}
