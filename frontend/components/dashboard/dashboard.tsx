"use client";

import React, { useState } from "react";
import { CalendarDateRangePicker } from "@/components/dashboard/date-range-picker";
import { Overview } from "@/components/dashboard/overview";
import { RecentListings } from "@/components/dashboard/recent-listings";
import { RecentListingsCount } from "@/components/dashboard/recent-listings-count";
import DashboardCards from "@/components/dashboard/dashboard-cards";
import { Button } from "@/components/ui/button";
import { addDays } from "date-fns";
import { DateRange } from "react-day-picker";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DownloadCSV from "@/components/dashboard/DownloadCSV";

type Props = {};

export default function Dashboard({}: Props) {
  const [date, setDate] = useState<DateRange | undefined>({
    from: addDays(new Date(), -30),
    to: new Date(),
  });

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex flex-col md:flex-row justify-center items-center md:justify-between text-center md:text-left space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">
          Marketplace Listings Dashboard
        </h2>
        <div className="flex items-center space-x-2">
          <CalendarDateRangePicker date={date} setDate={setDate} />
          <DownloadCSV date={date} />
        </div>
      </div>
      <Tabs defaultValue="overview" className="space-y-4 flex-col md:flex-row">
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
                <Overview date={date}/>
              </CardContent>
            </Card>
            <Card className="col-span-3">
              <CardHeader>
                <CardTitle>Recent Listings</CardTitle>
                <CardDescription>
                  <RecentListingsCount />
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
  );
}
