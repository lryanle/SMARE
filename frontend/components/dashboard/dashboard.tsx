"use client";

import { promises as fs } from "fs"
import path from "path"
import { z } from "zod"
import React, { useEffect, useState } from "react";
import { CalendarDateRangePicker } from "@/components/dashboard/date-range-picker";
import { Overview } from "@/components/dashboard/overview";
import { RecentListings } from "@/components/dashboard/recent-listings";
import { RecentListingsCount } from "@/components/dashboard/recent-listings-count";
import DashboardCards from "@/components/dashboard/dashboard-cards";
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
import { DataTable } from "@/components/datatable/data-table";
import { rawListingSchema, listingSchema } from "@/components/datatable/schema";
import { columns } from "@/components/datatable/columns";

type Props = {};

interface Listing {
  id: string;
  make: string;
  model: string;
  year: string;
  riskscore: string;
  url: string;
  marketplace: string,
  date: string;

  model_scores: {
    model_1: number;
    model_2: number;
    model_3: number;
    model_4: number;
    model_5: number;
    model_6: number;
  };
  model_versions: {
    model_1: number;
    model_2: number;
    model_3: number;
    model_4: number;
    model_5: number;
    model_6: number;
  };
  cleaner_version: number;
  scraper_version: number;
  price: number;
}

export default function Dashboard({}: Props) {
  const localTime = new Date();
  const today = new Date(localTime.getTime() + (localTime.getTimezoneOffset() * 60000));

  const [date, setDate] = useState<DateRange | undefined>({
    from: addDays(today, -30),
    to: today,
  });

  const [listings, setListings] = useState<Listing[]>([]);

  useEffect(() => {
    async function fetchTasks() {
      const response = await fetch('/api/listings');
      const data = await response.json();
      const validTasks = z.array(rawListingSchema).parse(data.data);
  
      const transformedTasks = validTasks.map(task => ({
        url: task.link,
        make: task.make,
        model: task.model,
        riskscore: String(task.risk_score),
        marketplace: task.source,
        year: String(task.year),
        id: task._id,
        date: task.scrape_date,

        model_scores: {
          model_1: task.model_scores.model_1,
          model_2: task.model_scores.model_2,
          model_3: task.model_scores.model_3,
          model_4: task.model_scores.model_4,
          model_5: task.model_scores.model_5,
          model_6: task.model_scores.model_6,
        },
        model_versions: {
          model_1: task.model_versions.model_1,
          model_2: task.model_versions.model_2,
          model_3: task.model_versions.model_3,
          model_4: task.model_versions.model_4,
          model_5: task.model_versions.model_5,
          model_6: task.model_versions.model_6,
        
        },
        cleaner_version: task.cleaner_version,
        scraper_version: task.scraper_version,
        // human_flag: task.human_flag,
        price: task.price,
      }));
  
      setListings(transformedTasks);
    }
  
    fetchTasks().catch(console.error);
  }, []);  

  return (
    <div className="flex-1 space-y-4 md:p-8 pt-24 md:pt-6">
      <div className="flex flex-col md:flex-row justify-center items-center md:justify-between text-center md:text-left space-y-2">
        <h2 className="text-3xl font-bold tracking-tight my-4 md:my-0">
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
          <TabsTrigger value="listings">
            Listings
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
                <CardTitle>Flagged Listings</CardTitle>
              </CardHeader>
              <CardContent className="pl-2">
                <Overview date={date}/>
              </CardContent>
            </Card>
            <Card className="col-span-4 md:col-span-3">
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
        <TabsContent value="listings" className="space-y-4">
          <Card className="h-full flex-1 flex-col space-y-8 md:p-8 md:flex">
            <div className="flex items-center justify-between space-y-2">
              <CardHeader>
                <CardTitle className="text-2xl font-bold tracking-tight">Listings View</CardTitle>
                <CardDescription className="text-muted-foreground">
                  View and filter through all social marketplace listings
                </CardDescription>
              </CardHeader>
            </div>
            <DataTable data={listings} columns={columns} />
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
