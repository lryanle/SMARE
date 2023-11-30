import Meta, { defaultMetaProps } from "@/components/layout/meta";

export default function NotFound() {
  return (
    <div className="h-screen w-full flex justify-center items-center bg-black">
      <Meta
        props={{
          ...defaultMetaProps,
          title: "Not Found | Statefarm SMARE",
          ogUrl: "https://smare.lryanle.com/500",
        }}
      />
      <h1 className="text-2xl font-light text-white">
        Not Found <span className="mx-3 text-4xl">|</span> Could not find requested resource 
      </h1>
    </div>  
  );
}
