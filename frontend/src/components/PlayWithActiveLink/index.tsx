"use client";

import ActiveLink from "@/components/ActiveLink";
import { useSearchParams } from "next/navigation";

function PlayWithActiveLink({ className }: { className: string }) {
  const searchParams = useSearchParams();
  const initialIsActive = searchParams.get("active");
  const isActive = initialIsActive === null || initialIsActive === "true";

  return (
    <div className={className}>
      <ActiveLink
        isActive={isActive}
        searchParams={new URLSearchParams(`active=${!isActive}`).toString()}
      >
        Test ActiveLink
      </ActiveLink>
    </div>
  );
}

export default PlayWithActiveLink;
