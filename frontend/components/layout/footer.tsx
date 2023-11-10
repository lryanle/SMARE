import { Statefarm } from "@/icons";
import Link from "next/link";

export default function Footer() {
  return (
    <div className="absolute w-full py-5 text-center">
      <p className="text-gray-500">
        A project by{" "}
        <Link
          className="font-semibold text-statefarm underline-offset-4 transition-colors hover:underline"
          href="https://github.com/lryanle/seniordesign"
          target="_blank"
          rel="noopener noreferrer"
        >
          University of Texas at Arlington CSE
        </Link>
        {" "}×{" "}
        <Link
          className="font-semibold text-statefarm underline-offset-4 transition-colors inline hover:underline"
          href="https://github.com/lryanle/seniordesign"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Statefarm className="h-4 w-4 inline" />{" "}
          Statefarm
        </Link>
      </p>
    </div>
  );
}
