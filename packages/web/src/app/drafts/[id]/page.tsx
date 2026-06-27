import { redirect } from 'next/navigation';

export default function DraftDetailPage({ params }: { params: { id: string } }) {
  redirect(`/drafts/${params.id}/review`);
}
