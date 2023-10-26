import type { Author } from "@/lib/models/author";
import useSWR from "swr";
import client from "./client";

/**
 * Get all authors
 */
const getAuthors = {
  key: () => "/authors",
  get() {
    return client.get<Author[]>(this.key());
  },
  data() {
    return this.get().then((res) => res.data);
  },
};

export function useAuthors() {
  const { data, error } = useSWR<Author[]>(getAuthors.key, () =>
    getAuthors.data()
  );
  return { authors: data, error, loading: !error && !data };
}

/**
 * Get one author
 */
const getAuthor = {
  key: ({ id }: IdArg) => `/authors/${id}`,
  get(arg: IdArg) {
    return client.get<Author>(this.key(arg));
  },
  data(arg: IdArg) {
    return this.get(arg).then((res) => res.data);
  },
};

export function useAuthor(arg: MaybeIdArg) {
  const nArg = arg.id ? (arg as IdArg) : null;
  const { data, error } = useSWR<Author>(nArg && getAuthor.key(nArg), () =>
    getAuthor.data(nArg!)
  );

  return { author: data, error, loading: !error && !data };
}

export const authorsApi = {
  getAuthors,
  getAuthor,
};
