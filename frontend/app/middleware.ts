import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith("/settings")) {
    // Add /settings specific logics
  }
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    // Add /dashboard specific logics
  }
}

export const config = {
  matcher: ["/settings/:path*", "/dashboard/:path*"],
};
