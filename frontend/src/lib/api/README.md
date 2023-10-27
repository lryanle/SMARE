# Understand the api client

We use [axios](https://github.com/axios/axios) client for the api calls, and [SWR](https://swr.vercel.app) to cache the results and to use the api with React hooks.

The most basic api example would be something like this:

```javascript
import useSWR from "swr";
import axios from "axios";

const client = axios.create();

const getPosts = {
  key: () => "/posts",
  get() {
    return client.get("/posts");
  },
};

export function usePosts() {
  const { data, error } = useSWR(getPosts.key, () =>
    getPosts.get().then((res) => res.data)
  );

  return {
    posts: data,
    error,
    loading: !error && !data,
  };
}

// In React component: //

const MyPage = () => {
  const { posts, error, loading } = usePosts();

  return (
    <div>
      {loading && <p>Posts are loading...</p>}
      {error && <p>{error?.message}</p>}
      <div>{posts && JSON.stringify(posts)}</div>
    </div>
  );
};
```

The `key` is very important here, without it SWR wouldn't know how to cache the results.

Note that when the api receives parameters we need to use the same parameters in the key
to cache it properly:

```javascript
const getPost = {
  key: (id) => `/post/${id}`,
  get: (id) => client.get(`/post/${id}`),
};
```

And it would be better to reuse the `key` when possible:

```javascript
const getPost = {
  key: (id) => `/post/${id}`,
  get(id) {
    return client.get(this.key(id));
  },
};
```

### When the parameter is not ready

> SWR will not start the request if the `key` function throws or returns a falsy value , or if `key` is null  
> (From [SWR Conditional Fetching](https://swr.vercel.app/docs/conditional-fetching))

We can use this behavior for api parameters that are not ready:

```javascript
const getPost = {
  key: ({ id }) => `/post/${id}`,
  get(arg) {
    return client.get(this.key(arg));
  },
  data(arg) {
    return this.get(arg).then((res) => res.data);
  },
};

export function usePost(arg) {
  const nArg = arg.id ? arg : null; // the id parameter may not be ready

  // Option 1: key function throws an error when nArg is null
  const { data, error } = useSWR(
    () => getPost.key(nArg),
    () => getPost.data(nArg)
  );

  // Option 2: key is null when nArg is null
  const { data, error } = useSWR(nArg ? getPost.key(nArg) : null, () =>
    getPost.data(nArg)
  );

  // Option 3 (recommended): the same as Option 2 but with shorter syntax
  const { data, error } = useSWR(nArg && getPost.key(nArg), () =>
    getPost.data(nArg)
  );

  return {
    post: data,
    error,
    loading: !error && !data,
  };
}

// In React component: //

const MyPage = () => {
  const id = getId(); // string or undefined
  const { post, error, loading } = usePost({ id });

  return (
    <div>
      {loading && <p>Post is loading...</p>}
      {error && <p>{error?.message}</p>}
      <div>{post && JSON.stringify(post)}</div>
    </div>
  );
};
```

## Helper functions

### createGETApiEndpoint(keyFunc)

> Create simple GET endpoint

Usage:

- Create GET endpoint:

  ```typescript
  const getPosts = createGETApiEndpoint<Post[]>(() => "/posts");
  ```

  Which equal to:

  ```typescript
  const getPosts = {
    key: () => "/posts",
    get() {
      return client.get<Post[]>(this.key());
    },
    data() {
      return this.get().then((res) => res.data);
    },
  };
  ```

- Create GET endpoint with arguments:
  ```typescript
  type Args = { id: string };
  const getPost = createGETApiEndpoint<Post, Args>(({ id }) => `/posts/${id}`);
  ```
  Which equal to:
  ```typescript
  type Args = { id: string };
  const getPost = {
    key: ({ id }: Args) => `/posts/${id}`,
    get(arg: Args) {
      return client.get<Post>(this.key(arg));
    },
    data(arg: Args) {
      return this.get(arg).then((res) => res.data);
    },
  };
  ```
