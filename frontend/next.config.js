/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  // Create a standalone folder which copies only the necessary files for production
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "loremflickr.com",
        port: "",
      },
      {
        protocol: "https",
        hostname: "avatars.githubusercontent.com"
      }
    ],
  },
};
