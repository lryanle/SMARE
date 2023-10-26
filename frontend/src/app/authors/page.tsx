"use client";

import { useAuthors } from "@/lib/api/authors";
import type { NextPage } from "next";

function AuthorsPage() {
  const { authors, error, loading } = useAuthors();

  return (
    <div>
      <div>
        <h1>Authors</h1>
        {loading && <p>Authors are loading...</p>}
        {error && <p>{error?.message}</p>}
        <ul>
          {authors?.map((author) => (
            <li key={author.id}>
              <h2>{author.name}</h2>
              <div>
                age:
                {author.age}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default AuthorsPage as NextPage;
