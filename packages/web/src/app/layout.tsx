import '../styles/globals.css';

export const metadata = {
  title: 'Human Review System',
  description: 'AI-Human Collaborative Quotation System',
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
