import React, { useRef, useState } from 'react';
import { View, Text, ActivityIndicator, Alert } from 'react-native';
import { useForm } from 'react-hook-form';
import { Button } from '~/components/Button';
import OTPTextInput from 'react-native-otp-textinput';
import axios from 'axios';

type OTPForm = {
  otp: string;
};

export default function OTPVerification() {
  const { handleSubmit, setValue, watch } = useForm<OTPForm>({
    defaultValues: { otp: '' },
  });

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const otpInputRef = useRef<OTPTextInput>(null);

  const onSubmit = async () => {
    const otp = watch('otp');
    if (!otp || otp.length < 4) {
      setErrorMessage('OTP must be at least 4 digits');
      return;
    }

    setLoading(true);
    setErrorMessage(null);
    try {
      const response = await axios.post('otp', { otp });

      if (response.data?.status === 'success') {
        Alert.alert('Success', 'OTP verified!');
      } else {
        setErrorMessage(response.data?.message || 'Invalid OTP');
      }
    } catch (error) {
      console.error(error);
      setErrorMessage('Server error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 items-center justify-center px-6 bg-white">
      <Text className="text-2xl font-semibold text-black mb-6">Enter OTP</Text>

      <OTPTextInput
        ref={otpInputRef}
        inputCount={6}
        handleTextChange={(text) => {
          setValue('otp', text);
        }}
        offTintColor="#d1d5db"
        containerStyle={{ marginBottom: 16 }}
        textInputStyle={{
          borderRadius: 8,
          borderWidth: 1,
          borderColor: '#ccc',
        }}
      />

      {errorMessage && <Text className="text-red-500 mt-2 text-sm">{errorMessage}</Text>}

      <View className="w-full mt-6">
        <Button
          title={loading ? 'Verifying...' : 'Verify OTP'}
          onPress={handleSubmit(onSubmit)}
          disabled={loading}
        />
        {loading && (
          <ActivityIndicator
            size="small"
            color="#3b82f6"
            style={{ marginTop: 12 }}
          />
        )}
      </View>
    </View>
  );
}
