"use client";

import type { NextPage } from "next";
import { useEffect } from "react";

function Custom404({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    // eslint-disable-next-line no-console
    console.error(error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong!</h2>

      <div
        className="my-5 mb-4 rounded-lg bg-red-50 p-4 text-sm text-red-800 transition-opacity duration-300 ease-in"
        role="alert"
      >
        <span className="font-medium">{error.name}</span>
        {error.message && (
          <span className="ml-2 border-l-2 border-current pl-2">
            {error.message}
          </span>
        )}
      </div>

      <button
        type="button"
        className="
          group mb-2 mr-2 inline-flex items-center justify-center overflow-hidden rounded-lg
          bg-blue-500 p-0.5 text-sm
          font-medium text-gray-900 hover:bg-blue-600 hover:text-white
          focus:outline-none focus:ring-4 focus:ring-blue-300"
        onClick={
          // Attempt to recover by trying to re-render the segment
          () => reset()
        }
      >
        <span className="rounded-md bg-white px-[1.1rem] py-1.5 transition-colors duration-75 ease-in group-hover:bg-opacity-0">
          Try Again
        </span>
      </button>
    </div>
  );
}

export default Custom404 as NextPage<{ error: Error; reset: () => void }>;
