"use client"

import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CalendarDays, Clock4, FileText, ShieldAlert } from "lucide-react";

type Props = {};

export default function DashboardCards({}: Props) {
  const [data, setData] = useState<{totalListings: number, riskScoreOver50: number, percentIncreaseToday: number, percentIncreaseThisMonth: number, percentIncreaseRiskScoreThisMonth: number, percentIncreaseLastMonth: number, listingsToday: number, listingsThisMonth: number, listingsLastMonth: number}>();

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

  console.log(data)

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Listings</CardTitle>
          <FileText size={16} strokeWidth={2} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{data?.totalListings}</div>
          <p className="text-xs text-muted-foreground">
            {`+${data?.percentIncreaseThisMonth}% from last month`}
          </p>
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
          <div className="text-2xl font-bold">{`+${data?.riskScoreOver50}`}</div>
          <p className="text-xs text-muted-foreground">{`+${data?.percentIncreaseRiskScoreThisMonth}% from last month`}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">New Listings</CardTitle>
          <CalendarDays size={16} strokeWidth={2} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{`+${data?.listingsThisMonth}`}</div>
          <p className="text-xs text-muted-foreground">{`+${data?.percentIncreaseLastMonth} from last month`}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Listings Today</CardTitle>
          <Clock4 size={16} />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{`+${data?.listingsToday}`}</div>
          <p className="text-xs text-muted-foreground">
            {`+${data?.percentIncreaseToday} from last 24 hours`}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
