import { BellIcon, EyeNoneIcon, PersonIcon } from "@radix-ui/react-icons"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { BellDot } from "lucide-react";
import Link from "next/link";
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

const NotiLists = [{ type: "facebook", car: "Honda Accord 2010", date: "2023-12-01", time: "10:27AM CST" },
                   { type: "craigslist", car: "Toyota Camry 2006", date: "2023-11-30", time: "10:26AM CST" }]

export function Notifications() {
  return (
    <>
      <CardHeader className="p-1 pb-3">
        <CardTitle>Notifications</CardTitle>
      </CardHeader>
      <Separator />
      <div className="space-y-2 py-2">
      {NotiLists.map((noti) => (
        (<div className="flex items-center space-x-4" key={`${noti.type}-${noti.car}-${noti.date}`}>
          <Avatar className=" h-8 w-8">
            <AvatarImage className="h-fit" src={`/logos/${noti.type}.png`} alt={`${noti.type} listing`} />
            <AvatarFallback>FB</AvatarFallback>
          </Avatar>
          <div>
            <p className="text-sm font-medium leading-none">New Flagged Listing</p>
            <p className="text-sm text-muted-foreground">{`${noti.date} ${noti.time}`}</p>
          </div>
        </div>)
      ))}
      </div>
      <Separator />
      <CardContent className="grid gap-1 p-1 pb-0">
        <Link href="/settings/notifications" className="-mx-2 flex items-start space-x-4 rounded-md p-2 transition-all hover:bg-accent hover:text-accent-foreground">
        <BellDot size={16} />
          <div className="space-y-1">
            <p className="text-sm font-medium leading-none">Notification Preferences</p>
            <p className="text-sm text-muted-foreground">
              Edit notification settings
            </p>
          </div>
        </Link>
      </CardContent>
    </>
  )
}