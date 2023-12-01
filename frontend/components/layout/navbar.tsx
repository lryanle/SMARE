"use client";

import useScroll from "@/lib/hooks/use-scroll";
import { Session } from "next-auth";
import Image from "next/image";
import Link from "next/link";
import { useSignInModal } from "./sign-in-modal";
import UserDropdown from "./user-dropdown";

export default function NavBar({ session }: { session: Session | null }) {
  const { SignInModal, setShowSignInModal } = useSignInModal();
  const scrolled = useScroll(50);

  return (
    <>
      <SignInModal />
      <div
        className={`fixed top-0 w-full flex justify-center ${
          scrolled
            ? "border-b border-gray-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60"
            : "bg-white/0"
        } z-30 transition-all`}
      >
        <div className="mx-5 flex h-16 max-w-screen-xl items-center justify-between w-full">
          <Link href="/" className="flex items-center font-display text-2xl">
            <Image
              src="/logos/smare.png"
              alt="SMARE logo"
              width="156"
              height="50"
              className="mr-2 rounded-sm"
            ></Image>
          </Link>
          <div className="flex flex-row align-center justify-end items-center space-x-6 text-sm font-medium">
            <Link href="/" className="align-middle text-gray-600 hover:text-gray-800 transition-all">
              Home
            </Link>
            <Link href="/dashboard" className="align-middle text-gray-600 hover:text-gray-800 transition-all">
              Dashboard
            </Link>
            <>
            {session ? (
              <UserDropdown session={session} />
            ) : (
              <button
                className="rounded-full border-2 border-statefarm bg-statefarm p-1.5 px-4 text-sm text-white transition-all hover:bg-white hover:text-statefarm"
                onClick={() => setShowSignInModal(true)}
              >
                Sign In
              </button>
            )}
            </>
          </div>
        </div>
      </div>
    </>
  );
}
