"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useEffect, useState } from "react";
import ListingsItem from "@/components/dashboard/listings-item";

export function RecentListings() {
  const [data, setData] =
    useState<
      {
        _id: string;
        title: string;
        price: string;
        odometer: string;
        link: string;
        seller_website: string;
        post_body: string;
        year: string;
        makemodel: string;
        latitude: string;
        longitude: string;
        attributes?: { label: string; value: string }[];
        images: string[];
        source: string;
        scraper_version: number;
        scrape_date: string;
        stage: string;
      }[]
    >();

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
    <div className="space-y-8  overflow-y-scroll h-80">
      {data ? (
        data.map((item) => <ListingsItem source={item.source} name={item.makemodel} year={item.year} date={item.scrape_date} riskScore={0} key={item._id} />)
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
}
