import { Link } from "expo-router";
import { Text, View } from "react-native";
import { Button } from "~/components/Button";
import { Container } from "~/components/Container";

export default function Groups() {
    return (
        <>
            <Container>

                <Text>Groups</Text>
                <View className="flex flex-col gap-2 ">
                    <Link href="/login" asChild className="">
                        <Button title="Login" />
                    </Link>
                    <Link href="/signup" asChild>
                        <Button title="Signup" />
                    </Link>
                </View>
            </Container>
        </>
    )
}