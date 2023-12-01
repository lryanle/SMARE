"use client"

import Meta, { defaultMetaProps } from "@/components/layout/meta";
import { ArrowBigLeftDash, ArrowLeft } from "lucide-react";
import { useRouter } from 'next/navigation';

export default function NotFound() {
  const router = useRouter();

  return (
    <div className="h-screen w-full flex justify-center items-center bg-white min-h-screen flex-col bg-gradient-to-br from-indigo-50 via-white to-red-100">
      <Meta
        props={{
          ...defaultMetaProps,
          title: "Not Found | Statefarm SMARE",
          ogUrl: "https://smare.lryanle.com/500",
        }}
      />
      <h1 className="text-2xl font-light text-black">
        Not Found <span className="mx-3 text-4xl">|</span> Could not find requested resource 
      </h1>

      <button onClick={() => router.back()} className="group flex mt-4 max-w-fit items-center justify-center space-x-2 rounded-full border border-statefarm bg-statefarm px-5 py-2 text-sm text-white transition-colors hover:bg-white hover:text-statefarm">
        <ArrowLeft size={16} className="text-white group-hover:text-statefarm" />
        <p>Go Back</p>
      </button>
    </div>  
  );
}
