"use client";

import { usePost } from "@/lib/api/posts";
import type { NextPage } from "next";

function PostPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const { post, error, loading } = usePost({ id });

  return (
    <div>
      <div>
        <h1>Post</h1>
        {loading && <p>Post is loading...</p>}
        {error && <p>{error?.message}</p>}
        <div>{post && JSON.stringify(post)}</div>
      </div>
    </div>
  );
}

export default PostPage as NextPage<{ params: { id: string } }>;
