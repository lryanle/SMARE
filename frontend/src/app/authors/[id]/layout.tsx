import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Author page",
};

const RootLayout = ({ children }: { children: React.ReactNode }) => children;

export default RootLayout;
