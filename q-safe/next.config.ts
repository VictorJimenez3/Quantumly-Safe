import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async redirects() {
    return [
      {
        source: "/404",
        destination: "/not-found",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
