import "next-auth";

declare module "next-auth" {
  /**
   * Returned by `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
   */
  interface Session {
    accessToken?: any;
    user: {
      id?: any;
    } & DefaultSession["user"];
  }

  interface User {
    // access_token: any
    // id: any
    // & DefaultSession["user"]
  }
}

declare module "next-auth/jwt" {
  /** Returned by the `jwt` callback and `getToken`, when using JWT sessions */
  interface JWT {
    /** OpenID ID Token */
    access_token?: string;
    id?: string;
  }
}
