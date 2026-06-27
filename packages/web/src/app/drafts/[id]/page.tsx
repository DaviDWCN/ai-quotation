import { redirect } from 'next/navigation';

export default function DraftPage({ params }: { params: { id: string } }) {
  redirect(`/drafts/${params.id}/review`);
}
