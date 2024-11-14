import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/api/scrape',
        destination: 'http://localhost:8080/api/scrape',
      }
    ];
  },

  async headers() {
    return [
      {
        source: '/api/scrape',
        headers:[
          {
            key: 'Cache-Control',
            value: 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
          },
        ]
      }
    ];
  }

};

export default nextConfig;
