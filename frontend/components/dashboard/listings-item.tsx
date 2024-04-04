/* eslint-disable camelcase */
import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { displayListing, scrapeListing } from "@/types/smare";
import { capitalize, cn } from "@/lib/utils";

export default function ListingsItem({source, make, model, year, scrape_date, risk_score}: displayListing) {
  risk_score = risk_score === -1 ? 0 : risk_score
  return (
    <div className={cn("flex items-center p-2", risk_score > 50 ? "bg-red-500 rounded-lg text-white font-bold py-3" : "")}>
      <Avatar className="h-9 w-9">
        <AvatarImage src={`/logos/${source}.png`} alt="Avatar" />
      </Avatar>
      <div className="ml-4 space-y-1">
        <p className={cn("text-sm leading-none", risk_score > 50 ? "text-white font-bold" : "font-medium")}>{`${capitalize(make)} ${capitalize(model)} ${year ? `(${year})` : ""}`}</p>
        <p className={cn("text-sm", risk_score > 50 ? "text-white font-bold" : "text-muted-foreground")}>{scrape_date.toLocaleUpperCase()}</p>
      </div>
      <div className={cn("ml-auto", risk_score > 50 ? "text-white font-bold" : "font-medium")}>{`${risk_score.toFixed(2)}%`}</div>
    </div>
  );
}
