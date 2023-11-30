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
          <AvatarImage src="/avatars/01.png" alt="Avatar" />
          <AvatarFallback>FB</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Facebook MP</p>
          <p className="text-sm text-muted-foreground">
            Toyota Camry 2010
          </p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="flex h-9 w-9 items-center justify-center space-y-0 border">
          <AvatarImage src="/avatars/02.png" alt="Avatar" />
          <AvatarFallback>FB</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Facebook MP</p>
          <p className="text-sm text-muted-foreground">Ford Mustang 2018</p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/avatars/03.png" alt="Avatar" />
          <AvatarFallback>FB</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Facebook MP</p>
          <p className="text-sm text-muted-foreground">
          Honda Civic 2015
          </p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/avatars/04.png" alt="Avatar" />
          <AvatarFallback>CL</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Craigslist</p>
          <p className="text-sm text-muted-foreground">Chevrolet Silverado 2020</p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/avatars/05.png" alt="Avatar" />
          <AvatarFallback>CL</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Craigslist</p>
          <p className="text-sm text-muted-foreground">BMW 3 Series 2013</p>
        </div>
        <div className="ml-auto font-medium">0.0/100</div>
      </div>
    </div>
  )
}