import type { AxiosResponse } from "axios";
import client from "./client";

type KeyFunc<TArg> = (arg: TArg) => string;

interface GETApiEndpoint<TData, TArg = void> {
  key: KeyFunc<TArg>;
  get(arg: TArg): Promise<AxiosResponse<TData, any>>;
  data(arg: TArg): Promise<TData>;
}

/**
 * **Create simple GET api endpoint**
 *
 * Usage:
 *
 * * To create GET endpoint like this:
 * ```
 * const getPosts = {
 *     key: () => '/posts',
 *     get() { return client.get<Post[]>(this.key()) },
 *     data() { return this.get().then((res) => res.data) },
 * }
 * ```
 * Do this:
 * ```
 * const getPosts = createGETApiEndpoint<Post[]>(() => '/posts')
 * ```
 *
 * * To create GET endpoint with arguments:
 * ```
 * const getPost = {
 *     key: ({ id }: { id: string }) => `/posts/${id}`,
 *     get(arg: { id: string }) { return client.get<Post>(this.key(arg)) },
 *     data(arg: { id: string }) { return this.get(arg).then((res) => res.data) },
 * }
 * ```
 * Do this:
 * ```
 * const getPost = createGETApiEndpoint<Post, { id: string }>(({ id }) => `/posts/${id}`)
 * ```
 * * Use the endpoint:
 * ```
 * const post = getPost.data({ id: '1' })
 * ```
 */
export default function createGETApiEndpoint<TData, TArg = void>(
  keyFunc: KeyFunc<TArg>
): GETApiEndpoint<TData, TArg> {
  const getFunc = (arg: TArg) => client.get<TData>(keyFunc(arg));
  const dataFunc = (arg: TArg) => getFunc(arg).then((res) => res.data);

  const endpoint = {
    key: keyFunc,
    get: getFunc,
    data: dataFunc,
  };
  return endpoint;
}
