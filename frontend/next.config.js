/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  swcMinify: true,
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
  async redirects() {
    return [
      {
        source: "/github",
        destination: "https://github.com/lryanle/seniordesign",
        permanent: false,
      },
    ];
  },
};
