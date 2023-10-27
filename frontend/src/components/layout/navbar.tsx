'use client'

import { LoadingDots } from '@/components/icons';
import { Bars3Icon } from '@heroicons/react/24/outline';
import { signIn, useSession } from 'next-auth/react';
import Image from 'next/image';
import Link from 'next/link';
import { useState } from 'react';

export default function Navbar({
  setSidebarOpen
}: {
  setSidebarOpen: (open: boolean) => void;
}) {
  const { data: session, status } = useSession();
  const [loading, setLoading] = useState(false);

  return (
    <nav
      className="absolute right-0 w-full flex items-center justify-between px-4 h-16 bg-white drop-shadow-md"
      aria-label="Navbar"
    >
      <Image src="/logos/smare.png" width="200" height="28" alt="statefarm logo" />
      <button
        type="button"
        className="inline-flex md:hidden items-center justify-center rounded-md text-gray-700 hover:text-gray-900 focus:outline-none focus:ring-0"
        onClick={() => setSidebarOpen(true)}
      >
        <span className="sr-only">Open sidebar</span>
        <Bars3Icon className="h-6 w-6" aria-hidden="true" />
      </button>
      {status !== 'loading' &&
        (session?.user ? (
          <Link href={`/${session.user?.name}`} legacyBehavior>
            <a className="w-8 h-8 rounded-full overflow-hidden">
              <Image
                src={
                  session.user?.image ||
                  `https://avatar.tobi.sh/${session.user.name}`
                }
                alt={session.user?.name || 'User'}
                width={300}
                height={300}
                placeholder="blur"
                blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQYV2PYsGHDfwAHNAMQumvbogAAAABJRU5ErkJggg=="
              />
            </a>
          </Link>
        ) : (
          <button
            disabled={loading}
            onClick={() => {
              setLoading(true);
              signIn('github', { callbackUrl: `/profile` });
            }}
            className={`${
              loading
                ? 'bg-gray-200 border-gray-300'
                : 'bg-red-600 hover:bg-white border-red-600'
            } w-36 h-8 py-1 text-white hover:text-red-600 border-2 rounded-md text-sm transition-all`}
          >
            {loading ? <LoadingDots color="gray" /> : 'Log in with GitHub'}
          </button>
        ))}
    </nav>
  );
}
