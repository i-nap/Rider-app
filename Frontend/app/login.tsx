import { useState } from "react";
import { Text, TextInput, View } from "react-native";
import { Container } from "~/components/Container";

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    return (
        <>
            <Container>

                <View className="flex-1 justify-center items-center bg-white px-6">
                    <Text className="text-3xl font-bold mb-8 text-black">Login</Text>

                    <TextInput
                        className="w-full border border-gray-300 rounded-xl p-4 mb-4 text-black"
                        placeholder="Email"
                        placeholderTextColor="#aaa"
                        value={email}
                        onChangeText={setEmail}
                        keyboardType="email-address"
                        autoCapitalize="none"
                    />

                    <TextInput
                        className="w-full border border-gray-300 rounded-xl p-4 mb-6 text-black"
                        placeholder="Password"
                        placeholderTextColor="#aaa"
                        value={password}
                        onChangeText={setPassword}
                        secureTextEntry
                    />

                </View>
            </Container>
        </>
    )
}