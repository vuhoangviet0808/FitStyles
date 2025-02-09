
import React, { useContext } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';

import Entypo from 'react-native-vector-icons/Entypo';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import FontAwsome6 from 'react-native-vector-icons/FontAwesome6';

import LogoScreen from './src/screens/LogoScreen';
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import HomeScreen from './src/screens/HomeScreen';
import { Text } from 'react-native';
import ProductDetailsScreen from './src/screens/ProductDetailsScreen';
import CartScreen from './src/screens/CartScreen';
import { CartContext, CartProvider } from './src/context/CartContext';
import { View } from 'react-native';



// Khởi tạo Stack và Tab Navigator
const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function HomeStackNavigator() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="HomeScreen" component={HomeScreen} />
      <Stack.Screen name="ProductDetails" component={ProductDetailsScreen} />
    </Stack.Navigator>
  );
}

function HomeTabs() {
  return (
    <CartProvider>
         <Tab.Navigator
        screenOptions={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarActiveTintColor: "#a52a2a",
        }}
      >
        <Tab.Screen name="HOME" component={HomeStackNavigator} options={{
          tabBarIcon:({size, focused, color})=>{
            return <Entypo name={"home"} size={size} color={color}/>
            
          },
        }} />
        <Tab.Screen name="REORDER" component={HomeScreen} options={{
          tabBarIcon:({size, color}) => {
            return <MaterialIcons name={"reorder"} size={size} color={color}/>
          },
        }}/>
        <Tab.Screen name="CART" component={CartScreen} options={{
          tabBarIcon:({size, focused, color})=>{
            const {carts} = useContext(CartContext);
            
            return(
              <View style ={{position: "relative"}}>
                  <MaterialCommunityIcons 
                  name={"cart"} 
                  size={size} 
                  color={color}
                  />    
                  <View style={{
                    height: 14,
                    width: 14,
                    borderRadius: 7,
                    backgroundColor: color,
                    alignItems: "center",
                    position: "absolute",
                    top: -10,
                    right: -5,
                  }}>
                    <Text style={{
                      fontSize: 10,
                      color: "white",

                    }}>{carts.length}</Text>
                  </View>
              </View>
          
            );
          },
        }}/>
        <Tab.Screen name="ACCOUNT" component={HomeScreen} options={{
          tabBarIcon:({size, color})=>{
            return <FontAwsome6 name={"user"} size={size} color={color}/>
            
          },
        }} />
      </Tab.Navigator>
    </CartProvider>
  );
}
function HomeStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="HomeTabs" component={HomeTabs} />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Splash" component={LogoScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="SignUp" component={RegisterScreen} />
        {/* Sau khi login, HomeTabs sẽ xuất hiện */}
        <Stack.Screen name="Home" component={HomeStack} />
        
      </Stack.Navigator>
    </NavigationContainer>
  );  
}