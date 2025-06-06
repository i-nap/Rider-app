import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, ActivityIndicator } from 'react-native';
import { useForm, Controller, useWatch } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import axios from 'axios';
import { Button } from '~/components/Button';
import { navigate } from 'expo-router/build/global-state/routing';

const signupSchema = z.object({
  fName: z.string().min(1, 'First name is required'),
  lName: z.string().min(1, 'Last name is required'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  confirmPassword: z.string().min(1, 'Confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type SignupFormData = z.infer<typeof signupSchema>;

export default function Signup() {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      fName: '',
      lName: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const [emailStatus, setEmailStatus] = useState<'idle' | 'checking' | 'valid' | 'invalid'>('idle');
  const [emailMessage, setEmailMessage] = useState<string | null>(null);
  const watchedEmail = useWatch({ control, name: 'email' });

  useEffect(() => {
    if (!watchedEmail || !watchedEmail.includes('@')) {
      setEmailStatus('idle');
      setEmailMessage(null);
      return;
    }

    setEmailStatus('checking');
    setEmailMessage(null);

    const timer = setTimeout(async () => {
      try {
        const response = await axios.post('test', {
          email: watchedEmail,
        });

        const { status, message } = response.data;

        if (status === 'valid') {
          setEmailStatus('valid');
          setEmailMessage(message);
        } else if (status === 'invalid') {
          setEmailStatus('invalid');
          setEmailMessage(message);
        } else {
          setEmailStatus('invalid');
          setEmailMessage('Unexpected status from server');
        }
      } catch (err) {
        console.error('Email check error:', err);
        setEmailStatus('invalid');
        setEmailMessage('Error contacting server');
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [watchedEmail]);


  const baseInputClass = "w-full rounded-xl p-4 mb-1 text-black border";
  const emailBorderColor =
    emailStatus === 'valid' ? 'border-green-500'
      : emailStatus === 'invalid' ? 'border-red-500'
        : 'border-gray-300';

  const onSubmit = (data: SignupFormData) => {
    console.log('Form Data:', data);
    navigate('/otp')
  };

  return (
    <View className="flex-1 justify-center items-center bg-white px-6">
      <Text className="text-3xl font-bold mb-8 text-black">Sign Up</Text>

      <View className="w-full mb-3">
        <Controller
          control={control}
          name="fName"
          render={({ field: { onChange, value } }) => (
            <TextInput
              className="w-full border border-gray-300 rounded-xl p-4 mb-1 text-black"
              placeholder="Enter First Name"
              placeholderTextColor="#aaa"
              value={value}
              onChangeText={onChange}
              autoCapitalize="words"
            />
          )}
        />
        {errors.fName && (
          <Text className="text-red-500 text-sm mt-1">{errors.fName.message}</Text>
        )}
      </View>

      <View className="w-full mb-3">
        <Controller
          control={control}
          name="lName"
          render={({ field: { onChange, value } }) => (
            <TextInput
              className="w-full border border-gray-300 rounded-xl p-4 mb-1 text-black"
              placeholder="Enter Last Name"
              placeholderTextColor="#aaa"
              value={value}
              onChangeText={onChange}
              autoCapitalize="words"
            />
          )}
        />
        {errors.lName && (
          <Text className="text-red-500 text-sm mt-1">{errors.lName.message}</Text>
        )}
      </View>

      <View className="w-full mb-3">
        <Controller
          control={control}
          name="email"
          render={({ field: { onChange, value } }) => (
            <View className="relative">
              <TextInput
                className={`${baseInputClass} ${emailBorderColor}`}
                placeholder="Enter Email"
                placeholderTextColor="#aaa"
                keyboardType="email-address"
                value={value}
                onChangeText={onChange}
                autoCapitalize="none"
              />
              {emailStatus === 'checking' && (
                <ActivityIndicator
                  color="#3b82f6"
                  style={{
                    position: 'absolute',
                    top: '50%',
                    right: 16,
                    transform: [{ translateY: -12 }],
                  }}
                />
              )}
            </View>
          )}
        />
        {!errors.email && emailMessage && (
          <Text
            className={`text-sm mt-1 ${emailStatus === 'valid' ? 'text-green-600' : 'text-red-500'
              }`}
          >
            {emailMessage}
          </Text>
        )}
        {errors.email && (
          <Text className="text-red-500 text-sm mt-1">{emailMessage}</Text>
        )}
      </View>

      {/* Password */}
      <View className="w-full mb-3">
        <Controller
          control={control}
          name="password"
          render={({ field: { onChange, value } }) => (
            <TextInput
              className="w-full border border-gray-300 rounded-xl p-4 mb-1 text-black"
              placeholder="Enter Password"
              placeholderTextColor="#aaa"
              secureTextEntry
              value={value}
              onChangeText={onChange}
              autoCapitalize="none"
            />
          )}
        />
        {errors.password && (
          <Text className="text-red-500 text-sm mt-1">{errors.password.message}</Text>
        )}
      </View>

      {/* Confirm Password */}
      <View className="w-full mb-4">
        <Controller
          control={control}
          name="confirmPassword"
          render={({ field: { onChange, value } }) => (
            <TextInput
              className="w-full border border-gray-300 rounded-xl p-4 mb-1 text-black"
              placeholder="Confirm Password"
              placeholderTextColor="#aaa"
              secureTextEntry
              value={value}
              onChangeText={onChange}
              autoCapitalize="none"
            />
          )}
        />
        {errors.confirmPassword && (
          <Text className="text-red-500 text-sm mt-1">{errors.confirmPassword.message}</Text>
        )}
      </View>

      {/* Submit Button */}
      <Button
        title="Create Account"
        onPress={handleSubmit(onSubmit)}
        className="w-full"
        disabled={emailStatus !== 'valid'}
      />    </View>
  );
}
