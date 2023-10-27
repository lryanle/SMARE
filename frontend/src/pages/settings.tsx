import { defaultMetaProps } from '@/components/layout/meta';
import Profile from '@/components/profile';
import { UserProps, getAllUsers, getUser, getUserCount } from '@/lib/api/user';
import { GetServerSideProps } from 'next';
import { getSession } from 'next-auth/react';

export default function Settings({ user }: { user: UserProps }) {
  return <Profile settings={true} user={user} />;
}

export const getServerSideProps: GetServerSideProps = async ({ req }) => {
  const session = await getSession({ req });
  if (!session) {
    return {
      redirect: {
        permanent: false,
        destination: '/'
      }
    };
  }

  const results = await getAllUsers();
  const totalUsers = await getUserCount();

  const user = await getUser(session.user?.name as string);

  const meta = {
    ...defaultMetaProps,
    title: `Settings | MongoDB Starter Kit`
  };

  return {
    props: {
      meta,
      results,
      totalUsers,
      user
    }
  };
};
