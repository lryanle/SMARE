"use client";

import React, { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  SquareChevronDown,
  SquareChevronLeft,
  SquareChevronRight,
  SquareChevronUp,
  Flag,
  FlagOff,
  Sigma,
} from "lucide-react";
import { Listing } from "../datatable/schema";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "@/components/ui/carousel";
import { capitalize } from "@/lib/utils";
import Link from "next/link";

type Props = {};

export default function DataLabeling({}: Props) {
  const [listingData, setListingData] = useState<
    Listing & {
      _id: number;
      images: string[];
      title: string;
      post_body: string;
      odometer: string;
      link: string;
      length: number;
      source: string;
    }
  >();
  const [statsData, setStatsData] = useState({
    totalLabel: 0,
    totalFlagged: 0,
    totalNotFlagged: 0,
  });
  const [api, setApi] = useState<CarouselApi>();
  const [current, setCurrent] = useState(0);
  const [count, setCount] = useState(0);
  const [historyStack, setHistoryStack] = useState<
    (Listing & {
      _id: number;
      images: string[];
      title: string;
      post_body: string;
      odometer: string;
      link: string;
      length: number;
      source: string;
    })[]
  >([]);

  useEffect(() => {
    if (!api) {
      return;
    }

    setCurrent(api.selectedScrollSnap() + 1);

    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });
  }, [api]);

  const fetchListingData = useCallback(async () => {
    console.log("Fetching a New Listing's Data");
    // no caching
    const response = await fetch("/api/ext/", { cache: "no-store" });
    if (!response.ok) {
      console.error("Failed to fetch listingData");
      return;
    }

    const result = await response.json();
    if (result.success && result.data) {
      setHistoryStack((prevHistory) => {
        const newHistory = [result.data, ...prevHistory];
        if (newHistory.length > 10) {
          newHistory.pop();
        }
        return newHistory;
      });
      setListingData(result.data);
      setCount(result.data ? result.data.images.length : 0);
      fetchStatsData();
    }
  }, []);

  const fetchStatsData = async () => {
    console.log("Fetching a Stats Data");
    const response = await fetch("/api/ext/stats");
    if (!response.ok) {
      console.error("Failed to fetch statsData");
      return;
    }

    const result = await response.json();
    if (result.success && result.stats) {
      setStatsData(result.stats);
    }
  };

  useEffect(() => {
    fetchListingData();
    fetchStatsData();
  }, [fetchListingData]);

  const replaceImageSize = (url: string) => {
    return url.replace("_50x50c.jpg", "_600x450.jpg");
  };

  const isFacebook = (url: string) => {
    return !url.includes("scontent");
  };

  const numberWithCommas = (x: string) => {
    return x.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  // enhanced uri decode that utilizes uridecode but also 3A, 3b, 2C, 3f, 26 right after the uri decode
  const decodeString = (uri: string) => {
    return decodeURI(uri).replace(
      /%3A|%3B|%2C|%3F|%26|%23|%3D|%24/gi,
      (match) => {
        switch (match.toLowerCase()) {
          case "%23":
            return "#";
          case "%24":
            return "$";
          case "%3a":
            return ":";
          case "%3b":
            return ";";
          case "%3d":
            return "=";
          case "%2c":
            return ",";
          case "%3f":
            return "?";
          case "%26":
            return "&";
          default:
            return match;
        }
      }
    );
  };

  const createKBBLink = (make: string, model: string, year: string) => {
    return `https://www.kbb.com/${make}/${model}/${year}/?ref=smare`;
  };

  const createEdmundsLink = (make: string, model: string, year: string) => {
    return `https://www.edmunds.com/${make}/${model}/${year}/?ref=smare`;
  };

  const removeQRCode = (text: string) => {
    return text.replace("QR Code Link to This Post", "");
  };

  const leftHandler = useCallback(() => {
    console.log(`Sending back a listing`);
    setHistoryStack((prevHistory) => {
      if (prevHistory.length > 0) {
        if (prevHistory[0].id === listingData?.id) {
          const [_, lastViewed, ...newHistory] = prevHistory;
          setListingData(lastViewed);
          setCount(lastViewed ? lastViewed.images.length : 0);

          return newHistory;
        } else {
          const [lastViewed, ...newHistory] = prevHistory;
          setListingData(lastViewed);
          setCount(lastViewed ? lastViewed.images.length : 0);

          return newHistory;
        }
      }
      return prevHistory;
    });
  }, [listingData]);

  const upHandler = useCallback(async () => {
    if (!listingData) {
      return;
    }
    console.log(`Flagging ${listingData?._id} as sus`);
    fetch("/api/ext/label", {
      method: "POST",
      headers: { secret: "oI6S1wwFSY4cltXGtsGUkb7rOhGdQ5SgvluijEBOtX0" },
      body: JSON.stringify({
        listingId: listingData._id,
        label: "label-flagged",
      }),
    });
    fetchListingData();
  }, [fetchListingData, listingData]);

  const downHandler = useCallback(async () => {
    if (!listingData) {
      return;
    }
    console.log(`Flagging ${listingData?._id} as not sus`);
    fetch("/api/ext/label", {
      method: "POST",
      headers: { secret: "oI6S1wwFSY4cltXGtsGUkb7rOhGdQ5SgvluijEBOtX0" },
      body: JSON.stringify({
        listingId: listingData._id,
        label: "label-notflagged",
      }),
    });
    fetchListingData();
  }, [fetchListingData, listingData]);

  const rightHandler = useCallback(async () => {
    console.log("Sending to new listing");
    fetchListingData();
  }, [fetchListingData]);

  useEffect(() => {
    const handleKeydown = (e: any) => {
      switch (e.key) {
        case "ArrowUp":
          upHandler();
          break;
        case "ArrowDown":
          downHandler();
          break;
        case "ArrowLeft":
          leftHandler();
          break;
        case "ArrowRight":
          rightHandler();
          break;
      }
    };

    window.addEventListener("keydown", handleKeydown);

    return () => {
      window.removeEventListener("keydown", handleKeydown);
    };
  }, [downHandler, leftHandler, rightHandler, upHandler]);

  return (
    <div className="h-full w-full flex justify-between items-center gap-2 border p-4 rounded-lg">
      <div className="w-1/2 flex flex-col justify-center items-between gap-4 p-2">
        <div className="flex justify-center items-center">
          <div className="w-full">
            <Carousel setApi={setApi} className="w-full">
              <CarouselContent>
                {listingData?.images ? (
                  listingData.images.map((image, index) =>
                    isFacebook(image) ? (
                      <CarouselItem key={index}>
                        <Card className="h-full flex justify-center items-center">
                          <CardContent className="flex items-center justify-center p-6 min-h-64 max-h-80 max-w-96 aspect-auto">
                            <img
                              src={replaceImageSize(image)}
                              className="w-full h-full"
                            />
                          </CardContent>
                        </Card>
                      </CarouselItem>
                    ) : (
                      <CarouselItem key={index}>
                        <Card>
                          <CardContent className="flex items-center justify-center p-6 h-80 w-full aspect-auto">
                            Facebook Images Not Supported
                          </CardContent>
                        </Card>
                      </CarouselItem>
                    )
                  )
                ) : (
                  <CarouselItem>
                    <Card>
                      <CardContent className="flex items-center justify-center p-6 h-80 w-full">
                        <span className="text-4xl font-semibold text-center">
                          Loading...
                        </span>
                      </CardContent>
                    </Card>
                  </CarouselItem>
                )}
              </CarouselContent>
              <CarouselPrevious
                className="translate-x-[4rem] drop-shadow"
                variant="default"
              />
              <CarouselNext
                className="-translate-x-[4rem] drop-shadow"
                variant="default"
              />
            </Carousel>
            <div className="py-2 text-center text-sm text-muted-foreground">
              Slide {current} of {count}
            </div>
          </div>
        </div>
        <div className="flex justify-center items-center gap-2">
          <div className="flex justify-center items-center gap-1 border p-1 rounded-lg">
            <Flag />
            {statsData.totalFlagged}
          </div>
          <div className="flex justify-center items-center gap-1 border p-1 rounded-lg">
            <FlagOff />
            {statsData.totalNotFlagged}
          </div>
          <div className="flex justify-center items-center gap-1 border p-1 rounded-lg">
            <Sigma />
            {statsData.totalLabel}
          </div>
        </div>
        <div className="flex justify-center items-end gap-1 border p-4 rounded-lg">
          <div className="flex flex-col justify-center items-center">
            <Button
              onClick={leftHandler}
              className="w-32 flex justify-start items-center gap-2 px-3 text-md"
              disabled={historyStack?.length === 0}
            >
              <SquareChevronLeft size={28} />
              Back
            </Button>
          </div>
          <div className="flex flex-col justify-center items-stretch gap-1">
            <Button
              onClick={upHandler}
              className="w-32 flex justify-start items-center gap-2 px-3 text-md"
            >
              <SquareChevronUp size={28} />
              Sus
            </Button>
            <Button
              onClick={downHandler}
              className="w-32 flex justify-start items-center gap-2 px-3 text-md"
            >
              <SquareChevronDown size={28} />
              Not Sus
            </Button>
          </div>
          <div className="flex flex-col justify-center items-center">
            <Button
              onClick={rightHandler}
              className="w-32 flex justify-start items-center gap-2 px-3 text-md"
            >
              <SquareChevronRight size={28} />
              New
            </Button>
          </div>
        </div>
      </div>
      <div className="h-[32rem] flex flex-1 border-l w-0.5"></div>
      <div className="w-1/2 flex flex-col justify-start items-between wrap p-4 gap-1 border rounded-lg">
        <span className="text-lg font-semibold">
          {decodeString(listingData?.title as string)}
        </span>
        <span className="text-md max-h-48 overflow-y-scroll">
          {removeQRCode(decodeString(listingData?.post_body as string))}
        </span>
        <div className="flex justify-start items-baseline gap-2 mt-2">
          <span className="text-lg font-semibold">Marketplace:</span>
          <span className="text-md">
            {capitalize(listingData?.source as string)}
          </span>
        </div>
        <div className="flex justify-start items-baseline gap-2">
          <span className="text-lg font-semibold">Make:</span>
          <span className="text-md">
            {capitalize(listingData?.make as string)}
          </span>
        </div>
        <div className="flex justify-start items-baseline gap-2">
          <span className="text-lg font-semibold">Model:</span>
          <span className="text-md">
            {capitalize(listingData?.model as string)}
          </span>
        </div>
        <div className="flex justify-start items-baseline gap-2">
          <span className="text-lg font-semibold">Year:</span>
          <span className="text-md">{listingData?.year}</span>
        </div>
        <div className="flex justify-start items-baseline gap-2">
          <span className="text-lg font-semibold">Price:</span>
          <span className="text-md">{`$${numberWithCommas(
            String(listingData?.price)
          )}`}</span>
        </div>
        <div className="flex justify-start items-baseline gap-2">
          <span className="text-lg font-semibold">Odometer:</span>
          <span className="text-md">{`${listingData?.odometer} miles`}</span>
        </div>
        <div className="flex justify-start items-center gap-1">
          {listingData?.link && (
            <Link href={listingData.link} target="_blank" className="mt-2">
              <Button className="flex justify-center items-center gap-2 px-3 text-md">
                View Listing
              </Button>
            </Link>
          )}
          {listingData?.make && listingData?.model && listingData?.year && (
            <Link
              href={createKBBLink(
                listingData?.make,
                listingData?.model,
                listingData?.year
              )}
              target="_blank"
              className="mt-2"
            >
              <Button className="flex justify-center items-center gap-2 px-3 text-md">
                View on KBB
              </Button>
            </Link>
          )}
          {listingData?.make && listingData?.model && listingData?.year && (
            <Link
              href={createEdmundsLink(
                listingData?.make,
                listingData?.model,
                listingData?.year
              )}
              target="_blank"
              className="mt-2"
            >
              <Button className="flex justify-center items-center gap-2 px-3 text-md">
                View on Edmunds
              </Button>
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
