import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar";

export function RecentListings() {
  return (
    <div className="space-y-8">
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/logos/facebook.png" alt="Avatar" />
          <AvatarFallback>FB</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Toyota Camry 2010</p>
          <p className="text-sm text-muted-foreground">
            Date
          </p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="flex h-9 w-9 items-center justify-center space-y-0 border">
          <AvatarImage src="/logos/facebook.png" alt="Avatar" />
          <AvatarFallback>FB</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Ford Mustang 2018</p>
          <p className="text-sm text-muted-foreground">Date</p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/logos/facebook.png" alt="Avatar" />
          <AvatarFallback>FB</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Honda Civic 2015</p>
          <p className="text-sm text-muted-foreground">
            Date
          </p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/logos/craigslist.png" alt="Avatar" />
          <AvatarFallback>CL</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Chevrolet Silverado 2020</p>
          <p className="text-sm text-muted-foreground">Date</p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/logos/craigslist.png" alt="Avatar" />
          <AvatarFallback>CL</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">BMW 3 Series 2013</p>
          <p className="text-sm text-muted-foreground">Date</p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
    </div>
  )
}