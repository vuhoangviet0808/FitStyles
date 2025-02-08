import React, { useState} from 'react';
import { View, Text, TextInput, TouchableOpacity, ImageBackground, Image, StyleSheet } from 'react-native';
import { globalStyles, colors } from '../theme/globalStyles';
import {useNavigation} from '@react-navigation/native';

import { loginUser } from '../services/authService';

export default function LoginScreen() {
  const navigation = useNavigation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await loginUser(email, password);
      if (response.success) {
        navigation.replace('Home'); // Chuyển đến HomeScreen
      } else {
        Alert.alert('Login Failed', response.message);
      }
    } catch (error) {
      Alert.alert('Error', 'Something went wrong.');
    }
  };

  return (
    <View style={styles.container}>
      <ImageBackground source={require('../assets/images/backgroundbrown.jpg')} style={styles.topBackground} resizeMode="cover">
        <Text style={styles.headerTitle}>Welcome{"\n"}Back!</Text>
      </ImageBackground>
      <ImageBackground source={require('../assets/images/backgroundwhite.jpg')} style={styles.bottomBackground} resizeMode="cover">
        <View style={styles.formContainer}>
          <Text style={globalStyles.label}>Email</Text>
          <View style={styles.inputWrapper}>
            <Image source={require('../assets/icon/email.png')} style={styles.icon} />
            <TextInput
              style={styles.input}
              placeholder="Enter your Email Address"
              placeholderTextColor={colors.textDark}
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              keyboardType="email-address"
            />
          </View>

          <Text style={globalStyles.label}>Password</Text>
          <View style={styles.inputWrapper}>
            <Image source={require('../assets/icon/lock.png')} style={styles.icon} />
            <TextInput
              style={styles.input}
              placeholder="Enter your Password"
              secureTextEntry
              placeholderTextColor={colors.textDark}
              value={password}
              onChangeText={setPassword}
            />
          </View>
          <View style={styles.rowContainer}>
            <TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
              <Text style={styles.signUp}>Sign Up</Text>
            </TouchableOpacity>
            <Text style={styles.forgotPassword}>Forgot Password?</Text>
          </View>

          <View style={{ alignItems: 'center' }}>
            <TouchableOpacity style={globalStyles.button} onPress={handleLogin}>
              <Text style={globalStyles.buttonText}>Sign In</Text>
            </TouchableOpacity>
          </View>
          
        </View>
        <Text style={styles.orText}>Or Sign In With</Text>

          <View style={styles.socialContainer}>
            <TouchableOpacity style={styles.socialButton}>
              <Image source={require('../assets/icon/google.jpg')} style={styles.socialIcon} />
            </TouchableOpacity>
            <TouchableOpacity style={styles.socialButton}>
              <Image source={require('../assets/icon/apple.png')} style={styles.socialIcon} />
            </TouchableOpacity>
            <TouchableOpacity style={styles.socialButton}>
              <Image source={require('../assets/icon/facebook.png')} style={styles.socialIcon} />
            </TouchableOpacity>
          </View>
      </ImageBackground>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'flex-start',
    backgroundColor: colors.background,
  },
  topBackground: {
    width: '100%',
    height: '70%', 
    justifyContent: 'center',
    alignItems: 'center',
  },
  bottomBackground: {
    width: '100%',
    height: '80%',
    borderTopLeftRadius: 40,
    borderTopRightRadius: 40,
    overflow: 'hidden',
    backgroundColor: 'white',
    padding: 20,
    marginTop: -120,
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'left',
    width: '80%',
  },
  formContainer: {
    justifyContent: 'flex-start',
    paddingTop: 10,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    paddingHorizontal: 10,
    marginBottom: 10,
  },
  icon: {
    width: 20,
    height: 20,
    marginRight: 10,
  },
  input: {
    flex: 1,
    height: 50,
  },
  rowContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    paddingHorizontal: 10, 
  },
  signUp: {
    color: colors.primary,
  },
  forgotPassword: {
    color: 'red',
  },
  orText: {
    textAlign: 'center',
    marginVertical: 10,
    fontSize: 16,
    fontWeight: 'bold',
  },
  socialContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 20,
  },
  socialButton: {
    width: 50,
    height: 50,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 25,
    marginHorizontal: 10,
  },
  socialIcon: {
    width: 30,
    height: 30,
  },
  backButton: {
    width: '100%',
    height: 50,
    borderWidth: 1,
    borderColor: '#9E6D4B',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 8,
  },
  backButtonText: {
    color: '#9E6D4B',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

