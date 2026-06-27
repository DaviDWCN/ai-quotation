import "@/styles/globals.css";

export const metadata = {
  title: "AI Quotation Human-in-the-Loop",
  description: "Review and approve AI-generated quotation drafts",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
