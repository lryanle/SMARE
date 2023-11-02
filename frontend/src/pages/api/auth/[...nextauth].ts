/* eslint-disable new-cap */
import clientPromise from "@/lib/mongodb";
import { MongoDBAdapter } from "@auth/mongodb-adapter";
import NextAuth, { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import GitHubProvider from "next-auth/providers/github";

export const authOptions: NextAuthOptions = {
  adapter: MongoDBAdapter(clientPromise),
  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
      profile(profile) {
        return {
          id: profile.id.toString(),
          name: profile.name ?? profile.login,
          username: profile.login,
          email: profile.email,
          image: profile.avatar_url,
          followers: profile.followers,
          verified: true,
        };
      },
    }),
    CredentialsProvider({
      name: "credentials",
      credentials: {
        username: { label: "Email", type: "text", placeholder: "contact@smare.com" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials, req) {
        // Find your user in the database using MongoDBAdapter
        const user = await authOptions.adapter.getUser(
          "6471f710f772cf139bc5142e"
        );
        if (user) {
          return user;
        } else {
          return null;
        }
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    // Set it as jwt instead of database
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, account }) {
      // Persist the OAuth access_token and or the user id to the token right after signin
      if (account) {
        token.accessToken = account.access_token;
        token.id = account.id;
      }
      return token;
    },
    async session({ session, token, user }) {
      // Send properties to the client, like an access_token and user id from a provider.
      session.accessToken = token.accessToken;
      session.user.id = token.id;

      return session;
    },
  },
};

const handler = NextAuth(authOptions);
export default handler;
