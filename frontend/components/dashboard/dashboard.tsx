"use client";

import { promises as fs } from "fs";
import path from "path";
import { z } from "zod";
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
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DownloadCSV from "@/components/dashboard/DownloadCSV";
import { DataTable } from "@/components/datatable/data-table";
import { rawListingSchema, listingSchema } from "@/components/datatable/schema";
import { columns } from "@/components/datatable/columns";
import {
  Area,
  Bar,
  BarChart,
  Brush,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  LineChart,
  Rectangle,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { capitalize } from "@/lib/utils";
import DataLabeling from "@/components/dashboard/datalabeling";
import { Badge } from "@/components/ui/badge";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { CircleHelp, Copy, MoveUpRight } from "lucide-react";
import { QuestionMarkCircledIcon, QuestionMarkIcon } from "@radix-ui/react-icons";

type Props = {};

interface Listing {
  id: string;
  make: string;
  model: string;
  year: string;
  riskscore: string;
  url: string;
  marketplace: string;
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
  const today = new Date(
    localTime.getTime() + localTime.getTimezoneOffset() * 60000
  );

  const [date, setDate] = useState<DateRange | undefined>({
    from: addDays(today, -30),
    to: today,
  });

  const [listings, setListings] = useState<Listing[]>([]);

  useEffect(() => {
    async function fetchTasks() {
      const response = await fetch("/api/listings");
      const data = await response.json();
      const validTasks = z.array(rawListingSchema).parse(data.data);

      const transformedTasks = validTasks.map((task) => ({
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

  const [flaggedData, setflaggedData] = useState([]);

  useEffect(() => {
    const fetchflaggedData = async () => {
      const response = await fetch(`/api/flagged`);
      if (!response.ok) {
        console.error("Failed to fetch data");
        return;
      }

      const result = await response.json();
      const mergedData = result.data.map((item: any) => ({
        ...item,
        make_model: `${capitalize(item.make)} ${capitalize(item.model)}`,
      }));
      setflaggedData(mergedData);
    };

    fetchflaggedData();
  }, [date]);

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
          <TabsTrigger value="listings">Listings</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
          <TabsTrigger value="labeling">Data Labeling</TabsTrigger>
          <TabsTrigger value="notifications" disabled>
            Notifications
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
                <Overview date={date} />
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
                <CardTitle className="text-2xl font-bold tracking-tight">
                  Listings View
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  View and filter through all social marketplace listings
                </CardDescription>
              </CardHeader>
            </div>
            <DataTable data={listings} columns={columns} />
          </Card>
        </TabsContent>
        <TabsContent value="reports" className="space-y-4">
          <Card className="h-full flex-1 flex-col space-y-8 md:p-8 md:flex">
            <div className="flex items-center justify-between space-y-2">
              <CardHeader>
                <CardTitle className="text-2xl font-bold tracking-tight">
                  Flagged Listings View
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  View the most flagged make-model combinations
                </CardDescription>
              </CardHeader>
            </div>
            <ResponsiveContainer width="100%" height={384}>
              <BarChart
                width={500}
                height={400}
                data={flaggedData}
                margin={{
                  top: 20,
                  right: 40,
                  bottom: 150,
                  left: 40,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="make_model" angle={-45} textAnchor="end" />
                <YAxis />
                <Tooltip />
                <Bar
                  dataKey="count"
                  fill="red"
                  activeBar={<Rectangle fill="red" stroke="black" />}
                />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>
        <TabsContent value="labeling" className="space-y-4">
          <Card className="h-full flex-1 flex-col space-y-2 md:p-8 md:flex">
            <div className="flex items-center justify-between space-y-2 w-full">
              <CardHeader className="w-full">
                <CardTitle className="w-full text-2xl font-bold tracking-tight flex justify-between items-center gap-2">
                  Data Labeling View
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button variant="outline" size="icon">
                        <CircleHelp />
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-md">
                      <DialogHeader>
                        <DialogTitle>Data Labeling Instructions</DialogTitle>
                        <DialogDescription>
                        <p className="inline"><span>{`When flagging a car as `}</span><Badge className="px-2 py-0">{`Sus`}</Badge><span>{` or `}</span><Badge className="px-2 py-0">{`Not Sus`}</Badge><span>{`, please be sure to do so from the `}<Badge className="px-2 py-0">{`perspective of an insurer`}</Badge>{` looking to potentially provide insurance policies for the vehicle listing. The data you label will serve as the `}<b>{`Ground Truth`}</b>{` for our model. If data in this listing view does not match up with the original listing, please stick primarily with what is in `}<b>{`this view`}</b>{` for any judgment.`}</span></p>
                        <br />
                        <p className="pt-2">{`For example, if the `}<span className="italic">{`Price`}</span>{` is different from what it shows in the description, stick with using the different `}<span className="italic">{`Price`}</span>{` attribute. If the post is from a dealership, please consider the post to be more `}<span className="italic">{`Not Sus`}</span>{`, unless another attribute like `}<span className="italic">{`Price`}</span>{` or `}<span className="italic">{`Title`}</span>{`, and `}<span className="italic">{`Make`}</span>{`, `}<span className="italic">{`Model`}</span>{`, or `}<span className="italic">{`Year`}</span>{` mismatch makes it look otherwise. The idea is that the data listed here `}<b>{`(even if incorrect)`}</b>{` will be used to train a model to make similar judgments based on these examples we feed it.`}</p>
                        <p className="pt-2"><b>{`Some factors that might make a listing more sus:`}</b></p>
                        <ul className="list-disc pl-4 ml-2">
                          <li>
                            {`Listing price is unreasonably `}<b>{`LOWER`}</b>{` than the MSRP (on
                            KBB or Edmunds) while factoring in the odometer (Think 15k
                            asking vs 40k MSRP).`}
                          </li>
                          <li>
                            {`Listing price is `}<b>{`EXTREMELY higher`}</b>{` than MSRP (think 30k
                            MSRP selling for 100k)`}
                          </li>
                          <li>
                            {`The seller feels suspicious. For example asking for cash
                            only, spamming emojis that don't contextually make sense
                            (dealers might use emojis which is okay).`}
                          </li>
                        </ul>
                        </DialogDescription>
                      </DialogHeader>
                      <DialogFooter className="sm:justify-start">
                        <DialogClose asChild>
                          <Button type="button" variant="secondary">
                            Close
                          </Button>
                        </DialogClose>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  {`"Tinder" for social marketplace automotive listings`}
                  <br />
                  <p className="inline-flex justify-start items-center gap-1">{`If this is your first time using this tool, `}<b>{`PLEASE READ THE TUTORIAL ON THE TOP RIGHT `}</b><MoveUpRight /></p>
                </CardDescription>
              </CardHeader>
            </div>
            <DataLabeling />
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
