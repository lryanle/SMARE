import { LoadingDots } from "@/components/icons";
import ClusterProvisioning from "@/components/layout/cluster-provisioning";
import Meta, { MetaProps } from "@/components/layout/meta";
import { ResultProps } from "@/lib/api/user";
import { useRouter } from "next/router";
import { ReactNode, useState } from "react";
import Navbar from "./navbar";

export default function Layout({
  meta,
  results,
  totalUsers,
  username,
  clusterStillProvisioning,
  children,
}: {
  meta: MetaProps;
  results: ResultProps[];
  totalUsers: number;
  username?: string;
  clusterStillProvisioning?: boolean;
  children: ReactNode;
}) {
  const router = useRouter();

  const [sidebarOpen, setSidebarOpen] = useState(false);

  if (router.isFallback) {
    return (
      <div className="h-screen w-screen flex justify-center items-center bg-black">
        <LoadingDots color="white" />
      </div>
    );
  }

  // You should remove this once your MongoDB Cluster is fully provisioned
  if (clusterStillProvisioning) {
    return <ClusterProvisioning />;
  }

  return (
    <div className="w-full mx-auto h-screen flex overflow-hidden bg-white">
      <Meta props={meta} />
      {/* <Toast username={username} /> */}
      {/* <Sidebar
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        results={results}
        totalUsers={totalUsers}
      /> */}

      <div className="flex flex-col min-w-0 flex-1 overflow-hidden">
        <div className="flex-1 relative z-0 flex overflow-hidden">
          <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none xl:order-last">
            {/* Navbar */}
            <Navbar setSidebarOpen={setSidebarOpen} />

            {/* {children} */}
          </main>
          {/* <div className="hidden md:order-first h-screen md:flex md:flex-col">
            <Directory results={results} totalUsers={totalUsers} />
          </div> */}
        </div>
      </div>
    </div>
  );
}
