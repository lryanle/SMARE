import Footer from "@/layouts/footer";
import Nav from "@/layouts/nav";
import { Analytics } from "@vercel/analytics/react";
import cx from "classnames";
import { Suspense } from "react";
import { inter, sfPro } from "./fonts";
import "./globals.css";

export const metadata = {
  title: "SMARE - Social Marketplace Automotive Risk Engine",
  description:
    "Statefarm SMARE: A University of Texas at Arlington Senior Design Project in collaboration with Statefarm.",
  metadataBase: new URL("https://smare.lryanle.com"),
  // themeColor: "#FFF",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={cx(sfPro.variable, inter.variable)}>
        <div className="fixed h-screen w-full bg-gradient-to-br from-indigo-50 via-white to-red-100" />
        <Suspense fallback="...">
          <Nav />
        </Suspense>
        <main className="flex min-h-screen w-full flex-col items-center justify-center py-32">
          {children}
        </main>
        <Footer />
        <Analytics />
      </body>
    </html>
  );
}
