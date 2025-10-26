import "./globals.css";
import type { ReactNode } from "react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Quant Pricing - Options Pricing Analysis",
  description:
    "Professional options pricing toolkit with Black-Scholes, binomial and trinomial tree methods, Greeks analysis, and convergence visualization.",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon.ico",
    apple: "/favicon.ico",
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="min-h-screen">{children}</main>
        {/* Footer */}
        <footer className="bg-gray-900 text-gray-300 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
              <p className="text-sm">
                © 2025 Hassan El Qadi. All rights reserved.
              </p>
              <div className="flex gap-6 text-sm">
                <a
                  href="https://github.com/hassanelq/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  Github
                </a>
                <a
                  href="https://elqadi.vercel.app/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  Portfolio
                </a>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
