"use client";

import { useAuthor } from "@/lib/api/authors";
import type { NextPage } from "next";

function AuthorPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const { author, error, loading } = useAuthor({ id });

  return (
    <div>
      <div>
        <h1>Author</h1>
        {loading && <p>Author is loading...</p>}
        {error && <p>{error?.message}</p>}
        <div>{author && JSON.stringify(author)}</div>
      </div>
    </div>
  );
}

export default AuthorPage as NextPage<{ params: { id: string } }>;
