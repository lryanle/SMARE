/* eslint-disable camelcase */
import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { displayListing, scrapeListing } from "@/types/smare";
import { capitalize, cn } from "@/lib/utils";

export default function ListingsItem({source, make, model, year, scrape_date, risk_score}: displayListing) {
  const converted_risk_score = parseFloat(risk_score) === -1 ? 0 : parseFloat(risk_score)

  // date to the format of "Apr. 4, 2024 12:00 PM CDT"
  const date = new Date(scrape_date).toLocaleString("en-US", {  
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    timeZoneName: "short"
  });

  return (
    <div className={cn("flex items-center p-2", converted_risk_score > 50 ? "bg-red-500 rounded-lg text-white font-bold py-3" : "")}>
      <Avatar className="h-9 w-9">
        <AvatarImage src={`/logos/${source}.png`} alt="Avatar" />
      </Avatar>
      <div className="ml-4 space-y-1">
        <p className={cn("text-sm leading-none", converted_risk_score > 50 ? "text-white font-bold" : "font-medium")}>{`${capitalize(make)} ${capitalize(model)} ${year ? `(${year})` : ""}`}</p>
        <p className={cn("text-sm", converted_risk_score > 50 ? "text-white font-bold" : "text-muted-foreground")}>{`${date}`}</p>
      </div>
      <div className={cn("ml-auto", converted_risk_score > 50 ? "text-white font-bold" : "font-medium")}>{`${parseFloat(String(converted_risk_score)).toFixed(2)}%`}</div>
    </div>
  );
}
