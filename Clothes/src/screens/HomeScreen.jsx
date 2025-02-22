// import { StyleSheet, Text, View } from "react-native";
// import React, { useState } from "react";
// import Fontisto from 'react-native-vector-icons/Fontisto';

// import LinearGradient from 'react-native-linear-gradient';
// import Header from "../components/Header";
// import { FlatList, TextInput } from "react-native-gesture-handler";
// import Category from "../components/Category";
// import ProductCard from "../components/ProductCard";
// // import data from "../data/data.json";
// import { products } from "../data/data";


// const categories = ['Trending Now', 'All', 'New', 'Men', 'Women']

// const HomeScreen = () =>{
//     const [products, setProducts] = useState(products);
//     const [selectedCategory, setSelectedCategory] = useState(null);


//     const handleLiked = (item) => {
//         const newProducts = products.map((prod) =>{
//             if(prod.id == item.id){
//                 return{
//                     ...prod,
//                     isLiked : !prod.isLiked,
//                 };
//             }
//             return prod;
//         }); 
//         setProducts(newProducts);
//     };
//     return (
//         <LinearGradient 
//             colors={['#FDF0F3', '#FFFBFC']} style={styles.container}>
//             <Header/>

//             {/* Product list*/}

//             <FlatList 
//                 numColumns={2}
//                 ListHeaderComponent={
//                     <>
//                         {/* <Text style={styles.matchText}>Match Your Style</Text> */}
//                         <View style={styles.inputContainer}>
//                             <View style = {styles.iconContainer} >
//                                 <Fontisto name ={"search"} size={26} color={"#C0C0C0"} 
//                                 />
//                             </View>
//                             <TextInput style = {styles.textInput} placeholder="Search"/>
//                         </View>
//                           {/* Category section */}
//                         <FlatList 
//                         data= {categories} 
//                         renderItem={({item}) => (
//                             <Category item = {item}
//                                 selectedCategory={selectedCategory} 
//                                 setSelectedCategory={setSelectedCategory}
//                             />
//                         )} 
//                         keyExtractor={(item) => item}
//                         horizontal= {true}
//                         showsHorizontalScrollIndicator = {false}
//                         />    
//                     </>
//                 }
//                 data={products} 
//                 renderItem={({item, index}) => (
//                     <ProductCard item = {item}
//                     handleLiked={handleLiked} />
//                 )} 
//                 showsVerticalScrollIndicator={false}
//                 keyExtractor={(item) => item.id}
//                 contentContainerStyle ={{
//                     paddingBottom: 150,
//                 }}
//             />


//         </LinearGradient>
//     );
// };

// export default HomeScreen

// const styles = StyleSheet.create({
//     container: {

//         padding: 20,
//     },
//     matchText:{
//         fontSize: 28,
//         color: "#000000",
//         marginTop: 25,
//     },
//     inputContainer:{
//         backgroundColor: "#FFFFFF",
//         height: 48,
//         borderRadius: 12,
//         alignItems:"center",
//         justifyContent: "center",
//         flexDirection :"row",
//         marginVertical: 20,
//     },
//     iconContainer:{
//         marginHorizontal: 20,
//     },
//     textInput:{
//         flex: 1,

//     }
// })
//======================================== Above use data.json========================================================
import { Image, StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import Fontisto from 'react-native-vector-icons/Fontisto';

import LinearGradient from 'react-native-linear-gradient';
import Header from "../components/Header";
import { FlatList, TextInput } from "react-native-gesture-handler";
import Category from "../components/Category";
import ProductCard from "../components/ProductCard";
import { products } from "../data/data"; // Import file data.js thay vì data.json

const categories = ['Trending Now', 'All', 'New', 'Men', 'Women'];

const HomeScreen = () => {
    const [productList, setProductList] = useState(products); // Dùng products từ data.js
    const [selectedCategory, setSelectedCategory] = useState(null);

    const handleLiked = (item) => {
        const newProducts = productList.map((prod) => {
            if (prod.id === item.id) {
                return {
                    ...prod,
                    isLiked: !prod.isLiked,
                };
            }
            return prod;
        });
        setProductList(newProducts);
    };

    return (
        <LinearGradient colors={['#FDF0F3', '#FFFBFC']} style={styles.container}>
            <Header />

            {/* Product list */}
            <FlatList
                numColumns={2}
                ListHeaderComponent={
                    <>
                        <View style={styles.inputContainer}>
                            <View style={styles.iconContainer}>
                                <Fontisto name={"search"} size={26} color={"#C0C0C0"} />
                            </View>
                            <TextInput style={styles.textInput} placeholder="Search" />
                        </View>
                        {/* Category section */}
                        <FlatList
                            data={categories}
                            renderItem={({ item }) => (
                                <Category
                                    item={item}
                                    selectedCategory={selectedCategory}
                                    setSelectedCategory={setSelectedCategory}
                                />
                            )}
                            keyExtractor={(item) => item}
                            horizontal={true}
                            showsHorizontalScrollIndicator={false}
                        />
                        {/* Hero Section */}
                        <View style={styles.heroContainer}>
                            {/* Hero Left Side */}
                            <View style={styles.heroTextContainer}>
                                <View style={styles.lineText}>
                                    <View style={styles.line} />
                                    <Text style={styles.bestSellerText}>OUR BEST SELLER</Text>
                                </View>
                                <Text style={styles.latestArrivals}>Latest Arrivals</Text>
                                <View style={styles.lineText}>
                                    <Text style={styles.shopNowText}>SHOP NOW</Text>
                                    <View style={styles.line} />
                                </View>
                            </View>

                            {/* Hero Right Side - Image */}
                            <Image source={require("../assets/hero_img.png")} style={styles.heroImage} resizeMode="cover" />
                        </View>
                    </>
                }
                data={productList}
                renderItem={({ item }) => (
                    <ProductCard item={item} handleLiked={handleLiked} />
                )}
                showsVerticalScrollIndicator={false}
                keyExtractor={(item) => item.id.toString()}
                contentContainerStyle={{
                    paddingBottom: 150,
                }}
            />
        </LinearGradient>
    );
};

export default HomeScreen;

const styles = StyleSheet.create({
    container: {
        padding: 20,
    },
    inputContainer: {
        backgroundColor: "#FFFFFF",
        height: 48,
        borderRadius: 12,
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "row",
        marginVertical: 20,
    },
    iconContainer: {
        marginHorizontal: 20,
    },
    textInput: {
        flex: 1,
    },
    /* Hero Section */
    heroContainer: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "#fff",
        padding: 20,
        borderRadius: 10,
        marginTop: 20,
        shadowColor: "#000",
        shadowOpacity: 0.1,
        shadowRadius: 5,
        elevation: 5,
    },
    heroTextContainer: {
        width: "50%",
        justifyContent: "center",
    },
    lineText: {
        flexDirection: "row",
        alignItems: "center",
    },
    line: {
        width: 30,
        height: 2,
        backgroundColor: "#414141",
        marginHorizontal: 5,
    },
    bestSellerText: {
        fontSize: 14,
        fontWeight: "600",
        color: "#414141",
    },
    latestArrivals: {
        fontSize: 28,
        fontWeight: "bold",
        marginVertical: 10,
        color: "#414141",
    },
    shopNowText: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#414141",
    },
    heroImage: {
        width: "50%",
        height: 150,
        borderRadius: 10,
    },
});