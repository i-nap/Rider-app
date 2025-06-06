import { forwardRef } from 'react';
import { Text, TouchableOpacity, TouchableOpacityProps, View } from 'react-native';

type ButtonProps = {
  title: string;
} & TouchableOpacityProps;

export const Button = forwardRef<View, ButtonProps>(({ title, disabled, ...touchableProps }, ref) => {
  const baseStyle = 'items-center rounded-3xl shadow-md p-4';
  const enabledStyle = 'bg-black';
  const disabledStyle = 'bg-neutral-500';

  return (
    <TouchableOpacity
      ref={ref}
      {...touchableProps}
      disabled={disabled}
      className={`${baseStyle} ${disabled ? disabledStyle : enabledStyle} ${touchableProps.className || ''}`}
    >
      <Text className="text-white text-lg font-semibold text-center">{title}</Text>
    </TouchableOpacity>
  );
});

Button.displayName = 'Button';
