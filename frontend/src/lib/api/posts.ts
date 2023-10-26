import createGETApiEndpoint from "@/lib/api/endpointGenerators";
import type { Post } from "@/lib/models/post";
import useSWR from "swr";

/**
 * Get all posts
 */
const getPosts = createGETApiEndpoint<Post[]>(() => "/posts");

export function usePosts() {
  const { data, error } = useSWR<Post[]>(getPosts.key, () => getPosts.data());
  return { posts: data, error, loading: !error && !data };
}

/**
 * Get one post
 */
const getPost = createGETApiEndpoint<Post, IdArg>(({ id }) => `/posts/${id}`);

export function usePost(arg: MaybeIdArg) {
  const nArg = arg.id ? (arg as IdArg) : null;
  const { data, error } = useSWR<Post>(nArg && getPost.key(nArg), () =>
    getPost.data(nArg!)
  );

  return { post: data, error, loading: !error && !data };
}

export const postsApi = {
  getPosts,
  getPost,
};
