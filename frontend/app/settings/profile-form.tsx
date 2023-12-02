"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { FaLinkedin, FaGoogle, FaDiscord, FaGithub } from "react-icons/fa";

import { redirect } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
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
import { getProviders, getSession, signIn } from "next-auth/react";
import { useEffect, useState } from "react";
import { Session } from "next-auth";
import useSWR from "swr";
import { is } from "date-fns/locale";
import { Check, SendHorizontal } from "lucide-react";

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

const fetcher = (url: string) =>
  fetch(url, { next: { revalidate: 60 } }).then((res) => res.json());

export function ProfileForm() {
  const { data: session, isValidating: isSessionLoading } = useSWR(
    "/api/auth/session",
    fetcher
  );
  const { data: userData, isValidating: isUserDataLoading } = useSWR(
    () =>
      `/api/user?userId=${session.user.id}&email=${encodeURI(
        session.user.email
      )}&name=${encodeURI(session.user.name)}`,
    fetcher
  );

  // exit if session doesnt have a valid email if session is not loading
  useEffect(() => {
    if (!session?.user?.email && !isSessionLoading) {
      redirect("/api/auth/signin");
    }
  }, [session, isSessionLoading]);

  const [isDataReady, setIsDataReady] = useState(false);
  const [defaultValues, setDefaultValues] = useState<
    Partial<ProfileFormValues>
  >({
    name: "",
    email: "",
    connected_accounts: [],
  });

  // set default values once userData is loaded
  useEffect(() => {
    if (userData && !isUserDataLoading) {
      const newDefaultValues = {
        name: userData.name,
        email: userData.email,
        connected_accounts: userData.providers,
      };
      setDefaultValues(newDefaultValues);
      setIsDataReady(true);
    }
  }, [userData, isUserDataLoading]);

  // set default values once userData is loaded
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues,
    mode: "onChange",
  });

  useEffect(() => {
    if (isDataReady) {
      form.reset(defaultValues); // Reset the form with new default values
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isDataReady, defaultValues]);

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
        {/* NAME FIELD */}
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                {!isDataReady ? (
                  <Skeleton className="h-9 w-full" /> // Skeleton Loader
                ) : (
                  <Input placeholder="Full display name" {...field} disabled />
                )}
              </FormControl>
              <FormDescription>
                This is should be your real name. This data is only used for
                personal display and for user verification purposes.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* EMAIL FIELD */}
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                {!isDataReady ? (
                  <Skeleton className="h-9 w-full" /> // Skeleton Loader
                ) : (
                  <Input
                    placeholder="Select a verified email to display"
                    {...field}
                    disabled
                  />
                )}
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

        {/* CONNECTED ACCOUNTS FIELD */}
        <div>
          {providers.map((provfield, index) => (
            <FormField
              key={provfield.type}
              name={`connected_accounts.${index}`}
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormLabel className={cn(index !== 0 && "sr-only")}>
                    Connected Accounts
                  </FormLabel>
                  <FormDescription className={cn(index !== 0 && "sr-only")}>
                    Add links to your website, blog, or social media profiles.
                  </FormDescription>
                  <FormControl>
                    {!isDataReady ? (
                      <Skeleton key={provfield.type} className="h-9 w-36" />
                    ) : (
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button
                            variant={
                              field.value === provfield.type
                                ? "outline"
                                : "secondary"
                            }
                            className="gap-4 w-36 justify-start"
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
                    )}
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          ))}
        </div>
        {/* <Button type="submit" className="gap-2">Update account<Check size={16} strokeWidth={2} className="text-white group-hover:text-statefarm" /></Button> */}
      </form>
    </Form>
  );
}
