type Nil = undefined | null;

type IdArg = {
  id: string;
};

type MaybeIdArg = {
  id: string | Nil;
};

type ApiError = {
  error: string;
};
