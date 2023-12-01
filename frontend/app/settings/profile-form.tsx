"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { FaLinkedin } from "react-icons/fa";
import { FaGoogle } from "react-icons/fa";
import { FaDiscord } from "react-icons/fa";
import { FaGithub } from "react-icons/fa";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { toast } from "@/components/ui/use-toast";
import { getProviders, getSession, signIn, useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { authOptions } from "../api/auth/[...nextauth]/authOptions";
import { redirect } from "next/navigation";
import { Session } from "next-auth";
import useSWR from "swr";

const providers = [
  { type: "github", icon: <FaGithub size="1.25rem" /> },
  { type: "google", icon: <FaGoogle size="1.25rem" /> },
  { type: "discord", icon: <FaDiscord size="1.25rem" /> },
  { type: "linkedin", icon: <FaLinkedin size="1.25rem" /> },
];

const profileFormSchema = z.object({
  name: z
    .string()
    .min(2, {
      message: "Name must be at least 2 characters.",
    })
    .max(30, {
      message: "Name must not be longer than 30 characters.",
    }),
  email: z
    .string({
      required_error: "Please select an email to display.",
    })
    .email(),
  connected_accounts: z
    .array(z.string())
    .min(1, {
      message: "You must have at least one connected account.",
    })
    .max(4, {
      message: "You can only have up to 4 connected accounts.",
    })
    .refine((accounts) => {
      const validAccounts = providers;
      return accounts.every((account) =>
        validAccounts.some((validAccount) =>
          account.includes(validAccount.type)
        )
      );
    }, "You can only connect accounts from Google, Discord, LinkedIn, or GitHub.")
    .optional(),
});

type ProfileFormValues = z.infer<typeof profileFormSchema>;

const fetcher = (url: string) => fetch(url, { next: { revalidate: 60 }}).then((res) => res.json());

export function ProfileForm() {
  // if (!session) { redirect('/api/auth/signin')  }
  const [defaultValues, setDefaultValues] = useState<Partial<ProfileFormValues>>({ name: "", email: "", connected_accounts: [""] })

  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues,
    mode: "onChange",
  });
  // const { data } = useSWR(`/api/user?userId=${session}`, fetcher);

  useEffect(() => {
    // const { data } = useSWR(`/api/user?userId=${session}`, fetcher);
    const getSesh = async () => {
      const provs = Object.keys(await getProviders() as Object);
      const session = await getSession() as Session;
      console.log(provs)
      const newDefaultValues = { 
        name: session?.user?.name || '', 
        email: session?.user?.email || '', 
        connected_accounts: provs || [''] 
      };
      setDefaultValues(newDefaultValues);
      form.reset(newDefaultValues); // Reset the form with new default values
    }
    getSesh();
  }, [form]);

  function onSubmit(data: ProfileFormValues) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }


  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Full display name" {...field} />
              </FormControl>
              <FormDescription>
                This is should be your real name. This data is only used for
                personal display and for user verification purposes.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="Select a verified email to display" {...field} disabled/>
              </FormControl>
              <FormDescription>
                Your email is linked to the provider you signed in with. To sign
                in to a different account, log in through a provider with a
                different linked email.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <div>
          {providers.map((provfield, index) => (
            <FormField
              control={form.control}
              key={provfield.type}
              name={`connected_accounts.${index}`}
              render={({ field }) => (
                <FormItem>
                  <FormLabel className={cn(index !== 0 && "sr-only")}>
                    URLs
                  </FormLabel>
                  <FormDescription className={cn(index !== 0 && "sr-only")}>
                    Add links to your website, blog, or social media profiles.
                  </FormDescription>
                  <FormControl>
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button
                          variant={
                            field.value === provfield.type
                              ? "outline"
                              : "secondary"
                          }
                          className="gap-4"
                          {...field}
                          disabled={field.value === provfield.type}
                        >
                          {provfield.icon}
                          <span className="text-left">
                            {provfield.type.charAt(0).toUpperCase() +
                              provfield.type.slice(1)}
                            {field.value === provfield.type ? (
                              <p className="text-green-500 text-xs leading-none">
                                {" "}
                                Connected
                              </p>
                            ) : (
                              <p className="text-red-500 text-xs leading-none">
                                {" "}
                                Disconnected
                              </p>
                            )}
                          </span>
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="sm:max-w-[425px]">
                        <DialogHeader>
                          <DialogTitle>
                            Continue to{" "}
                            {provfield.type.charAt(0).toUpperCase() +
                              provfield.type.slice(1)}
                            ?
                          </DialogTitle>
                          <DialogDescription>
                            Any unsaved changes will be lost. Are you sure you
                            want to continue?
                          </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                          <div className="flex flex-row justify-between items-center w-full">
                            <Button
                              type="submit"
                              variant="secondary"
                              onClick={() => {
                                signIn(provfield.type);
                              }}
                            >
                              Connect to{" "}
                              {provfield.type.charAt(0).toUpperCase() +
                                provfield.type.slice(1)}
                            </Button>

                            <DialogClose asChild>
                              <Button type="submit">Go back</Button>
                            </DialogClose>
                          </div>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          ))}
        </div>
        <Button type="submit">Update account</Button>
      </form>
    </Form>
  );
}
