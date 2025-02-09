import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import React from "react";
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';

const imageurl = "https://res.cloudinary.com/dlc5c1ycl/image/upload/v1710567612/qichw3wrcioebkvzudib.png"
const CartCard = () =>{
    return (
       <View style={styles.container}>
            <Image source={{uri : imageurl}} style={styles.coverImage}/>
            
            <View style={styles.cardContent}>
                <Text style={styles.title}>Jacket Jeans</Text>
                <Text style={styles.price}>$37.3</Text>
                <View style={styles.circleSizeContainer}>
                    <View style={styles.circle}/>
                    <View style={styles.sizeCircle}>
                        <Text style={styles.sizeText}>L</Text>
                    </View>
                </View>
            </View>
            <FontAwesome6 name={"trash"} color={"#F68CB5"} 
                size={22}/>
       </View>
       
    )
}




export default CartCard;




const styles = StyleSheet.create({
    container:{
        marginVertical: 10,
        flexDirection: "row",
    },
    coverImage:{
        height: 125,
        width: "25%",
        borderRadius: 20,
    },
    cardContent:{
        flex: 1,
        marginHorizontal:10,
    },
    title:{
        fontSize: 18,
        color: "#444444",
        fontWeight: "500",
    },
    price:{
        color: "#797979",
        marginVertical: 10,
        fontSize: 18,

    },
    circle:{
        height: 32,
        width: 32,
        borderRadius: 16,
        backgroundColor: "#7094C1"
    },
    circleSizeContainer:{
        flexDirection :"row",
        
    },
    sizeCircle:{
        backgroundColor: "white",
        height: 32,
        width: 32,
        borderRadius: 16,
        justifyContent: "center",
        alignItems: "center",
        marginLeft: 10,
    },
    sizeText:{
        fontSize: 18,
        fontWeight: "500",
    }
})
