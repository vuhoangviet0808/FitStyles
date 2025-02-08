import React, { useEffect } from 'react';
import { View, ImageBackground, Text, StatusBar } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { globalStyles } from '../theme/globalStyles';

export default function LogoScreen() {
  const navigation = useNavigation();

  useEffect(() => {
    setTimeout(() => {
      navigation.replace('Login');
    }, 3000);
  }, []);

  return (
    <View style={globalStyles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#9E6D4B" />
      <ImageBackground
        source={require('../assets/images/logoScreen.webp')}
        style={{ width: '100%', height: '100%', justifyContent: 'center', alignItems: 'center' }}
        resizeMode="cover"
      >
        {/* <Text style={globalStyles.title}>FitStyle</Text> */}
      </ImageBackground>
    </View>
  );
}
