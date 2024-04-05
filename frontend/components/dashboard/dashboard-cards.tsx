"use client"

import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CalendarDays, Clock4, FileText, ShieldAlert } from "lucide-react";
import { dashboardCardTypes } from "@/types/smare";
import { Skeleton } from "../ui/skeleton";

type Props = {};

export default function DashboardCards({}: Props) {
  const [data, setData] = useState<dashboardCardTypes>();

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("/api/listings/stats");
      if (!response.ok) {
        console.error("Failed to fetch data");
        return;
      }

      const result = await response.json();
      if (result.success && result.data) {
        setData(result.data);
      }
    };

    fetchData();
  }, []);

  // get today's locale month
  const today = new Date();
  const locale = "en-US";
  const month = today.toLocaleDateString(locale, { month: "long" });

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Listings</CardTitle>
          <FileText size={16} strokeWidth={2} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{data ? data?.totalListings : <Skeleton className="h-6 w-32 my-1" />}</div>
          {data ? <p className="text-xs text-muted-foreground">
            {`+${data?.percentIncreaseThisMonth}% from last month`}
          </p> : <Skeleton className="h-3 w-40 my-1 rounded-lg" />}
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Flagged Listings
          </CardTitle>
          <ShieldAlert size={16} strokeWidth={2} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{data ? `+${data?.riskScoreOver50}` : <Skeleton className="h-6 w-32 my-1" />}</div>
          {data ? <p className="text-xs text-muted-foreground">{`+${data?.percentIncreaseRiskScoreThisMonth}% from last month`}</p> : <Skeleton className="h-3 w-40 my-1 rounded-lg" />}
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{month} Listings</CardTitle>
          <CalendarDays size={16} strokeWidth={2} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{data ? `+${data?.listingsThisMonth}` : <Skeleton className="h-6 w-32 my-1" />}</div>
          {data ? <p className="text-xs text-muted-foreground">{`+${data?.listingsLastMonth} from last month`}</p> : <Skeleton className="h-3 w-40 my-1 rounded-lg" />}
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Listings Today</CardTitle>
          <Clock4 size={16} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{data  ?`+${data?.listingsToday}` : <Skeleton className="h-6 w-32 my-1" />}</div>
          {data ? <p className="text-xs text-muted-foreground">
            {`+${data?.listingsThisWeek} this week`}
          </p> : <Skeleton className="h-3 w-40 my-1 rounded-lg" />}
        </CardContent>
      </Card>
    </div>
  );
}
