import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import Fontisto from 'react-native-vector-icons/Fontisto';

import LinearGradient from 'react-native-linear-gradient';
import Header from "../components/Header";
import { FlatList, TextInput } from "react-native-gesture-handler";
import Category from "../components/Category";


const categories = ['Trending Now', 'All', 'New', 'Men', 'Women']

const HomeScreen = () =>{
    const [selectedCategory, setSelectedCategory] = useState(null);
    return (
        <LinearGradient 
            colors={['#FDF0F3', '#FFFBFC']} style={styles.container}>
            <Header/>
            <Text style={styles.matchText}>Match Your Style</Text>

            <View style={styles.inputContainer}>
                <View style = {styles.iconContainer} >
                    <Fontisto name ={"search"} size={26} color={"#C0C0C0"} 
                    />
                </View>
                <TextInput style = {styles.textInput} placeholder="Search"/>
            </View>

            {/* Category section */}
            <FlatList 
            data= {categories} 
            renderItem={({item}) => (
                <Category item = {item}
                    selectedCategory={selectedCategory} 
                    setSelectedCategory={setSelectedCategory}
                />
            )} 
            keyExtractor={(item) => item}
            horizontal= {true}
            showsHorizontalScrollIndicator = {false}
            />
            
        </LinearGradient>
    );
};

export default HomeScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
    },
    matchText:{
        fontSize: 28,
        color: "#000000",
        marginTop: 25,
    },
    inputContainer:{
        backgroundColor: "#FFFFFF",
        height: 48,
        borderRadius: 12,
        alignItems:"center",
        justifyContent: "center",
        flexDirection :"row",
        marginVertical: 20,
    },
    iconContainer:{
        marginHorizontal: 20,
    },
    textInput:{
        flex: 1,
        
    }
})
