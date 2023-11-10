import Modal from "@/components/shared/modal";
import { Discord, Github, Google, Linkedin, LoadingDots } from "@/icons";
import { signIn } from "next-auth/react";
import Image from "next/image";
import {
  Dispatch,
  SetStateAction,
  useCallback,
  useMemo,
  useState,
} from "react";

const SignInModal = ({
  showSignInModal,
  setShowSignInModal,
}: {
  showSignInModal: boolean;
  setShowSignInModal: Dispatch<SetStateAction<boolean>>;
}) => {
  const [signInClickedGithub, setSignInClickedGithub] = useState(false);
  const [signInClickedGoogle, setSignInClickedGoogle] = useState(false);
  const [signInClickedDiscord, setSignInClickedDiscord] = useState(false);
  const [signInClickedLinkedin, setSignInClickedLinkedin] = useState(false);

  return (
    <Modal showModal={showSignInModal} setShowModal={setShowSignInModal}>
      <div className="w-full overflow-hidden shadow-xl md:max-w-md md:rounded-2xl md:border md:border-gray-200">
        <div className="flex flex-col items-center justify-center space-y-3 border-b border-gray-200 bg-white px-4 py-6 pt-8 text-center md:px-16">
          <a href="https://smare.lryanle.com">
            <Image
              src="/favicon.ico"
              alt="Logo"
              className="h-10 w-10 rounded-full"
              width={20}
              height={20}
            />
          </a>
          <h3 className="font-display text-2xl font-bold">Log In</h3>
          <p className="text-sm text-gray-500">
            Log in or create an account to view your social marketplace risky listings dashboard - only your email and profile picture will be stored.
          </p>
        </div>

        <div className="flex flex-col space-y-4 bg-gray-50 px-4 py-8 md:px-16">
        <button
            disabled={signInClickedGithub}
            className={`${
              signInClickedGithub
                ? "cursor-not-allowed border-gray-200 bg-gray-100"
                : "border border-gray-200 bg-white text-black hover:bg-gray-50"
            } flex h-10 w-full items-center justify-center space-x-3 rounded-md border text-sm shadow-sm transition-all duration-75 focus:outline-none`}
            onClick={() => {
              setSignInClickedGithub(true);
              signIn("github"); 
            }}
          >
            {signInClickedGithub ? (
              <LoadingDots color="#808080" />
            ) : (
              <>
                <Github className="h-5 w-5" />
                <p>Sign in with Github</p>
              </>
            )}
          </button>
          <button
            disabled={signInClickedGoogle}
            className={`${
              signInClickedGoogle
                ? "cursor-not-allowed border-gray-200 bg-gray-100"
                : "border border-gray-200 bg-white text-black hover:bg-gray-50"
            } flex h-10 w-full items-center justify-center space-x-3 rounded-md border text-sm shadow-sm transition-all duration-75 focus:outline-none`}
            onClick={() => {
              setSignInClickedGoogle(true);
              signIn("google"); 
            }}
          >
            {signInClickedGoogle ? (
              <LoadingDots color="#808080" />
            ) : (
              <>
                <Google className="h-5 w-5" />
                <p>Sign in with Google</p>
              </>
            )}
          </button>
          <button
            disabled={signInClickedDiscord}
            className={`${
              signInClickedDiscord
                ? "cursor-not-allowed border-gray-200 bg-gray-100"
                : "border border-gray-200 bg-white text-black hover:bg-gray-50"
            } flex h-10 w-full items-center justify-center space-x-3 rounded-md border text-sm shadow-sm transition-all duration-75 focus:outline-none`}
            onClick={() => {
              setSignInClickedDiscord(true);
              signIn("discord");
            }}
          >
            {signInClickedDiscord ? (
              <LoadingDots color="#808080" />
            ) : (
              <>
                <Discord className="h-5 w-5" />
                <p>Sign in with Discord</p>
              </>
            )}
          </button>
          <button
            disabled={signInClickedLinkedin}
            className={`${
              signInClickedLinkedin
                ? "cursor-not-allowed border-gray-200 bg-gray-100"
                : "border border-gray-200 bg-white text-black hover:bg-gray-50"
            } flex h-10 w-full items-center justify-center space-x-3 rounded-md border text-sm shadow-sm transition-all duration-75 focus:outline-none`}
            onClick={() => {
              setSignInClickedLinkedin(true);
              signIn("linkedin");
            }}
          >
            {signInClickedLinkedin ? (
              <LoadingDots color="#808080" />
            ) : (
              <>
                <Linkedin className="h-5 w-5" />
                <p>Sign in with LinkedIn</p>
              </>
            )}
          </button>
        </div>
      </div>
    </Modal>
  );
};

export function useSignInModal() {
  const [showSignInModal, setShowSignInModal] = useState(false);

  const SignInModalCallback = useCallback(() => {
    return (
      <SignInModal
        showSignInModal={showSignInModal}
        setShowSignInModal={setShowSignInModal}
      />
    );
  }, [showSignInModal, setShowSignInModal]);

  return useMemo(
    () => ({ setShowSignInModal, SignInModal: SignInModalCallback }),
    [setShowSignInModal, SignInModalCallback],
  );
}
