import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

type Props = {
  source: string;
  name: string;
  year: string;
  date: string;
  riskScore: number;
  _id?: string;
  title?: string;
  price?: string;
  odometer?: string;
  link?: string;
  seller_website?: string;
  post_body?: string;
  makemodel?: string;
  latitude?: string;
  longitude?: string;
  attributes?: { label: string; value: string }[];
  images?: string[];
  scraper_version?: number;
  scrape_date?: string;
  stage?: string;
};

export default function ListingsItem({source, name, year, date, riskScore}: Props) {
  return (
    <div className="flex items-center">
      <Avatar className="h-9 w-9">
        <AvatarImage src={`/logos/${source}.png`} alt="Avatar" />
      </Avatar>
      <div className="ml-4 space-y-1">
        <p className="text-sm font-medium leading-none">{`${decodeURI(name)} (${year})`}</p>
        <p className="text-sm text-muted-foreground">{date}</p>
      </div>
      <div className="ml-auto font-medium">{`${riskScore * 100}/100`}</div>
    </div>
  );
}
