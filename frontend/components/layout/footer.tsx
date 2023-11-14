import { Statefarm, Uta } from "@/icons";
import Link from "next/link";

export default function Footer() {
  return (
    <div className="absolute w-full py-5 text-center">
      <p className="text-gray-500 inline-flex items-center gap-2">
        <Link
          className="font-semibold text-slate-500 hover:text-statefarm transition-colors inline-flex items-center gap-1"
          href="https://github.com/lryanle/SMARE"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Uta className="h-4 w-4 inline" />{" "}
          University of Texas at Arlington CSE
        </Link>
        {" "}×{" "}
        <Link
          className="font-semibold text-slate-500 hover:text-statefarm transition-colors inline-flex items-center gap-1"
          href="https://statefarm.com"
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
