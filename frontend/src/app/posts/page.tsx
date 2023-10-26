"use client";

import { usePosts } from "@/lib/api/posts";
import type { NextPage } from "next";

function PostsPage() {
  const { posts, error, loading } = usePosts();

  return (
    <div>
      <div>
        <h1>Posts</h1>
        {loading && <p>Posts are loading...</p>}
        {error && <p>{error?.message}</p>}
        <ul>
          {posts?.map((post) => (
            <li key={post.id}>
              <h2>{post.title}</h2>
              <div>{post.content}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default PostsPage as NextPage;
