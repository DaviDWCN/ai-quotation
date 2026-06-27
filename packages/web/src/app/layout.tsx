import '../styles/globals.css';

export const metadata = {
  title: 'AI Quotation Human-in-the-Loop',
  description: 'AI-assisted quotation review system',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
