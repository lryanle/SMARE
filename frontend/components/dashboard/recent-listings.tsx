"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useEffect, useState } from "react";
import ListingsItem from "@/components/dashboard/listings-item";
import { scrapeListing } from "@/types/smare";

export function RecentListings() {
  const [data, setData] =
    useState<scrapeListing[]>();

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("/api/listings");
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

  return (
    <div className="space-y-3 overflow-y-scroll h-[30rem]">
      {data ? (
        data.map((item) => <ListingsItem source={item.source} make={item.make} model={item.model} year={item.year} scrape_date={item.scrape_date} risk_score={item.risk_score} key={item._id} />)
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
}
