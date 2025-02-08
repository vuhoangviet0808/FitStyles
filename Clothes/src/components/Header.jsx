import { Image, StyleSheet, Text, View } from "react-native";
import React from "react";
import Icon from 'react-native-vector-icons/FontAwesome';
import AntDesign from 'react-native-vector-icons/AntDesign';
import LinearGradient from 'react-native-linear-gradient';


const Header = () =>{
    return (
        <View style ={styles.container}>
            <View style={styles.appIconContainer}>
                <Image source={require("../assets/appIcon.png")} style={styles.appIcon}/>
            </View>
            <Image source={require("../assets/dp.png")} style={styles.dp}/>
        </View>
    )
}

export default Header

const styles = StyleSheet.create({
    container:{
        flexDirection: "row",
        justifyContent: "space-between",
    },
    appIconContainer:{
        backgroundColor: "#FFFFFF",
        height: 44,
        width: 44,
        borderRadius: 22,
        justifyContent: "center",
        alignItems: "center",
    },
   appIcon:{
    height: 28,
    width: 28,
   },
   dp:{
    height: 44,
    width: 44,
    borderRadius: 22,
   },
})
