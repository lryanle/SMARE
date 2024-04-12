"use client";

import { useEffect, useState } from "react";
import { dashboardCardTypes } from "@/types/smare";
import { Skeleton } from "@/components/ui/skeleton";

export function RecentListingsCount() {
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

  return `${
    data ? data?.listingsToday : "..."
  } listings flagged today (${new Date().toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })})`;
}
