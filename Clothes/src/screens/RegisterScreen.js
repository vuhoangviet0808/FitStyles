import React, { useState} from 'react';
import { View, Text, TextInput, Alert, TouchableOpacity, ImageBackground, Image, StyleSheet } from 'react-native';
import { globalStyles, colors } from '../theme/globalStyles';
import { registerUser} from "../services/authService";

export default function RegisterScreen() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    
    const handleRegister = async () => {
        if (!name.trim() || !email.trim() || !password.trim()) {
            Alert.alert("Error", "Please fill in all fields");
            return;
        }

        setLoading(true); 

        try {
            const result = await registerUser(name, email, password);

            if (result.ok) {
                Alert.alert("Success", result.message);
            } else {
                Alert.alert("Error", result.message || "Something went wrong");
            }
        } catch (error) {
            console.error("Registration Error:", error);
            Alert.alert("Error", "Network request failed. Please try again.");
        } finally {
            setLoading(false); 
        }
    };

  return (
    <View style={styles.container}>
      <ImageBackground
        source={require('../assets/images/backgroundbrown.jpg')}
        style={styles.topBackground}
        resizeMode="container"
      >
        <Text style={styles.headerTitle}>Create an{"\n"}account</Text>
      </ImageBackground>
      <ImageBackground
        source={require('../assets/images/backgroundwhite.jpg')} 
        style={styles.bottomBackground}
        resizeMode="cover"
      >
        <View style={styles.formContainer}>
          <Text style={globalStyles.label}>Name</Text>
          <View style={styles.inputWrapper}>
            <Image source={require('../assets/icon/people.png')} style={styles.icon} />
            <TextInput 
                style={styles.input} placeholder="Enter Your Name" 
                placeholderTextColor={colors.textDark}
                value={name}
                onChangeText={setName}
            />
          </View>

          <Text style={globalStyles.label}>Email</Text>
          <View style={styles.inputWrapper}>
            <Image source={require('../assets/icon/email.png')} style={styles.icon} />
            <TextInput 
                style={styles.input} 
                placeholder="Enter Your Email Address" 
                placeholderTextColor={colors.textDark}
                value={email}
                onChangeText={setEmail}
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

          <Text style={styles.agree}>
            Agree with{' '}
            <Text style={styles.link}>Term & Condition</Text>
          </Text>


          <View style={{ alignItems: 'center' }}>
            <TouchableOpacity style={globalStyles.button} onPress={handleRegister}>
              <Text style={globalStyles.buttonText}>Sign Up</Text>
            </TouchableOpacity>
          </View>
          
          <View style={globalStyles.horizontalLine} />

          <Text style={styles.orText}>Or Sign Up With</Text>

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

          <TouchableOpacity style={styles.backButton}>
            <Text style={styles.backButtonText}>Back</Text>
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
    height: '85%',
    borderTopLeftRadius: 40,
    borderTopRightRadius: 40,
    overflow: 'hidden',
    backgroundColor: 'white',
    padding: 10,
    marginTop: -150,
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
  agree: {
    fontSize: 16,
    color: 'black', 
  },
  link: {
    color: 'blue', 
    textDecorationLine: 'underline', 
    fontWeight: 'bold', 
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

