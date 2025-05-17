import { Stack, Link } from 'expo-router';
import UserAccountPage from '~/app/screens/UserAccountPage';

import { Button } from '~/components/Button';
import { Container } from '~/components/Container';
import { ScreenContent } from '~/components/ScreenContent';

export default function Home() {
  return (
    <>
      <Stack.Screen options={{ title: 'Home' }} />
      <Container>
        <UserAccountPage />
        <Link href={{ pathname: '/details', params: { name: 'Dan' } }} asChild>
          <Button title="Hello World" />
        </Link>
      </Container>
    </>
  );
}
