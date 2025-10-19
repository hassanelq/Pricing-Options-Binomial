import "./globals.css";
import type { ReactNode } from "react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Quant Pricing - Options Pricing Analysis",
  description:
    "Professional options pricing toolkit with Black-Scholes, binomial and trinomial tree methods, Greeks analysis, and convergence visualization.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="container pt-16 pb-8 min-h-screen">{children}</main>
      </body>
    </html>
  );
}
