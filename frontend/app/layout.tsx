/* eslint-disable new-cap */
import Footer from "@/layouts/footer";
import Nav from "@/layouts/nav";
import { cn } from "@/lib/utils";
import { Analytics } from "@vercel/analytics/react";
import cx from "classnames";

import { Suspense } from "react";
import { sfPro } from "./fonts";
import "./globals.css";

import { Inter as FontSans } from "next/font/google";
import { SessionProvider } from "next-auth/react";
import { Toaster } from "@/components/ui/toaster";

export const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata = {
  title: "SMARE - Social Marketplace Automotive Risk Engine",
  description:
    "Statefarm SMARE: A University of Texas at Arlington Senior Design Project in collaboration with Statefarm.",
  metadataBase: new URL("https://smare.lryanle.com"),
  // themeColor: "#FFF",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={
          cx(sfPro.variable) +
          " overscroll-y-none " +
          cn(
            "min-h-screen bg-background font-sans antialiased",
            fontSans.variable
          )
        }
      >
        <Suspense fallback="Loading...">
          <Nav />
        </Suspense>
        <main className="flex min-h-screen w-full flex-col items-center justify-center">
          {children}
        </main>
        <Toaster />
        <Footer />
        <Analytics />
      </body>
    </html>
  );
}
