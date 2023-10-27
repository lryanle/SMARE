import { Metadata } from "next";

// 'metadata' only works in server components. See https://github.com/vercel/next.js/issues/46372
export const metadata: Metadata = {
  title: "Authors page",
};

const RootLayout = ({ children }: { children: React.ReactNode }) => children;

export default RootLayout;
