"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useEffect, useState } from "react";
import ListingsItem from "@/components/dashboard/listings-item";
import { scrapeListing } from "@/types/smare";
import { Skeleton } from "@/components/ui/skeleton";

export function RecentListings() {
  const [data, setData] = useState<scrapeListing[]>();

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("/api/listings?max=100");
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
    <div className="space-y-3 overflow-y-scroll h-[23rem]">
      {data ? (
        data.map((item) => (
          <ListingsItem
            source={item.source}
            make={item.make}
            model={item.model}
            year={String(item.year)}
            scrape_date={item.scrape_date}
            risk_score={String(item.risk_score)}
            key={item._id}
          />
        ))
      ) : (
        <>
          {Array.from({ length: 10 }, (_: any, index: any) => (
            <div
              key={index}
              className="flex flex-row justify-between items-center p-2"
            >
              <div className="flex justify-start items-center gap-4">
                <Skeleton className="h-9 w-9 rounded-full" />
                <div className="flex flex-col justify-center items-start gap-2">
                  <Skeleton className="h-[14px] w-48 rounded-xl" />
                  <Skeleton className="h-[14px] w-44 rounded-xl" />
                </div>
              </div>
              <Skeleton className="h-6 w-16 rounded-xl" />
            </div>
          ))}
        </>
      )}
    </div>
  );
}
