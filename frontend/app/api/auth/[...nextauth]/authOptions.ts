/* eslint-disable new-cap */
import prisma from "@/lib/prisma";
import { PrismaAdapter } from "@next-auth/prisma-adapter";
import { NextAuthOptions } from "next-auth";
import DiscordProvider from "next-auth/providers/discord";
import GitHubProvider from "next-auth/providers/github";
import GoogleProvider from "next-auth/providers/google";
import LinkedInProvider from "next-auth/providers/linkedin";

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
      allowDangerousEmailAccountLinking: true,
      // profile(profile) {
      //   return {
      //     id: profile.id.toString(),
      //     name: profile.name ?? profile.login,
      //     email: profile.email,
      //     image: profile.avatar_url
      //   };
      // },
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
      allowDangerousEmailAccountLinking: true,
      // profile(profile) {
      //   return {
      //     id: profile.id.toString(),
      //     name: profile.name ?? profile.login,
      //     email: profile.email,
      //     image: profile.avatar_url
      //   };
      // },
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code",
        },
      },
    }),
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID as string,
      clientSecret: process.env.DISCORD_CLIENT_SECRET as string,
      allowDangerousEmailAccountLinking: true,
      // profile(profile) {
      //   return {
      //     id: profile.id.toString(),
      //     name: profile.name ?? profile.login,
      //     email: profile.email,
      //     image: profile.avatar_url
      //   };
      // },
    }),
    LinkedInProvider({
      clientId: process.env.LINKEDIN_CLIENT_ID as string,
      clientSecret: process.env.LINKEDIN_CLIENT_SECRET as string,
      allowDangerousEmailAccountLinking: true,
      // profile(profile) {
      //   return {
      //     id: profile.id.toString(),
      //     name: profile.name ?? profile.login,
      //     email: profile.email,
      //     image: profile.avatar_url
      //   };
      // },
      authorization: {
        params: { scope: "openid profile email" },
      },
      issuer: "https://www.linkedin.com",
      jwks_endpoint: "https://www.linkedin.com/oauth/openid/jwks",
      profile(profile, tokens) {
        const defaultImage =
          "https://cdn-icons-png.flaticon.com/512/174/174857.png";
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture ?? defaultImage,
        };
      },
    }),
    // CredentialsProvider({
    //   name: "credentials",
    //   credentials: {
    //     email: { label: "Email", type: "text", placeholder: "contact@smare.com" },
    //     password: { label: "Password", type: "password" },
    //   },
    //   async authorize(credentials, req) {
    //     // Find your user in the database using MongoDBAdapter
    //     const client = await clientPromise;
    //     const users = client.db("auth").collection("users");

    //     // Find user with the email
    //     const result = await users.findOne({
    //         email: credentials?.email,
    //     });

    //     // Not found - send error res
    //     if (!result) {
    //         client.close();
    //         throw new Error('No user found with the email');
    //     }

    //     // Check hased password with DB password
    //     const checkPassword = await compare(credentials?.password, result.password);

    //     // Incorrect password - send response
    //     if (!checkPassword) {
    //         client.close();
    //         throw new Error('Password doesnt match');
    //     }
    //     // Else send success response
    //     client.close();
    //     return { email: result.email }
    //   },
    // }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  // session: {
  //   // Set it as jwt instead of database
  //   strategy: "jwt",
  // },
  callbacks: {
    // async jwt({ token, account }) {
    //   // Persist the OAuth access_token and or the user id to the token right after signin
    //   if (account) {
    //     token.accessToken = account.access_token;
    //     token.id = account.id as string;
    //   }
    //   return token;
    // },
    async session({ session, token, user }) {
      // Send properties to the client, like an access_token and user id from a provider.

      session.user.name = user.name;
      session.user.email = user.email;
      session.user.image = user.image;
      session.user.id = user.id;

      // session.accessToken = token.accessToken as string;
      // session.user.id = token.id;

      return session;
    },
  },
};
