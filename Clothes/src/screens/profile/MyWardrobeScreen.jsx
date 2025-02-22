import React, { useState } from "react";
import { View, Text, TouchableOpacity, Image, StyleSheet, ScrollView, FlatList } from "react-native";
import { useNavigation } from "@react-navigation/native";
import Ionicons from "react-native-vector-icons/Ionicons";
import AntDesign from 'react-native-vector-icons/AntDesign';
import Category from "../../components/Category";
import { useWardrobe } from "../../context/WardrobeContext";

const MyWardrobeScreen = () => {
    const navigation = useNavigation();
    const categories = [
        { name: "All", count: 23 },
        { name: "Shirt", count: 10 },
        { name: "Pants", count: 4 },
        { name: "Skirt", count: 4 },
        { name: "Trousers", count: 2 },
        { name: "Jackets", count: 3 },
    ];
    const [selectedCategory, setSelectedCategory] = useState(null);

    const { images } = useWardrobe();



    return (
        
        <View style={styles.container}>
            {/* Header */}
            <View style={styles.headerContainer}>
                <TouchableOpacity onPress={() => navigation.goBack()} style={styles.appIconContainer}>
                    <Ionicons name="chevron-back" size={24} color="#E96E6E" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>My wardrobe</Text>
            </View>

            {/* Upload Clothes Section */}
            {/* <Text style={styles.subTitle}>Upload your clothes</Text> */}

            {/* Category Bar */}

            <FlatList
                data={categories}
                horizontal={true} // Hiển thị danh mục theo chiều ngang
                showsHorizontalScrollIndicator={false}
                keyExtractor={(item, index) => index.toString()}
                contentContainerStyle={{ paddingHorizontal: 16, paddingVertical: 10, paddingBottom: 30 }}
                renderItem={({ item }) => {
                    const isSelected = selectedCategory === item.name;
                    return (
                        <TouchableOpacity
                            style={[styles.categoryButton, isSelected && styles.selectedCategory]}
                            onPress={() => setSelectedCategory(item.name)}
                        >
                            <Text style={[styles.categoryText, isSelected && styles.selectedText]}>
                                {item.name}: {item.count}
                            </Text>
                        </TouchableOpacity>
                    );
                }}

            />

            {/* <FlatList
                data={images}
                numColumns={2}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <Image source={item} style={styles.imageItem} />
                )}
                contentContainerStyle={{ paddingBottom: 80 }} 
            /> */}
            
            <FlatList
                data={images}
                numColumns={2}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => {
                    console.log("MyWD Screen image:", item);
                    return item ? (
                        <><Image source={{ uri: item }} style={styles.image} /><Text style={styles.errorText}>OK Image</Text></>
                    ) : (
                        <Text style={styles.errorText}>Invalid Image</Text>
                    );
                }}
                
            />

            {/* Nút Upload More cố định dưới màn hình */}
            <View style={styles.uploadMoreContainer}>
                <TouchableOpacity style={styles.uploadMoreButton} onPress={() => navigation.navigate("MyWardrobeUploadScreen")}>
                    <Text style={styles.buttonText}>Upload more</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};
export default MyWardrobeScreen;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#FDF0F3"
    },
    headerContainer: {
        flexDirection: "row",
        alignItems: "center",
        padding: 16,
        backgroundColor: "#FDF0F3",
        justifyContent: "space-between",
        position: "relative",
        marginVertical: 20,

    },
    appIconContainer: {
        position: "absolute",
        left: 16,
        backgroundColor: "#FFF",
        padding: 8,
        borderRadius: 22
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: "300",
        color: "#000",
        position: "absolute",
        left: "50%",
        transform: [{ translateX: -50 }],
    },
    subTitle: {
        marginLeft: 16,
        fontSize: 15,
        fontWeight: "bold",
        color: "black"
    },
    uploadContainer: {
        alignItems: "center",
        marginTop: 20
    },
    uploadBox: {
        width: 150,
        height: 150,
        backgroundColor: "#EEE",
        justifyContent: "center",
        alignItems: "center"
    },
    uploadIcon: {
        width: 50,
        height: 50
    },
    saveButton: {
        backgroundColor: "#A36A2C",
        padding: 12,
        marginTop: 20,
        borderRadius: 8,

    },
    buttonText: {
        color: "#FFF",
        fontWeight: "bold",
    },

    categoryBar: {
        marginVertical: 10,
        paddingHorizontal: 16,
        flexDirection: "row",
        gap: 10,  // Thêm khoảng cách giữa các button
    },
    categoryButton: {
        minHeight: 45,  // Tăng chiều cao để tránh bị cắt chữ
        minWidth: 100,  // Đảm bảo chiều rộng phù hợp
        backgroundColor: "#EEE",
        paddingVertical: 12,
        paddingHorizontal: 20,  // Tăng padding ngang để chữ không bị dính mép
        borderRadius: 10,
        justifyContent: "center",
        alignItems: "center",
        marginHorizontal: 5, // Khoảng cách giữa các button
    },
    categoryText: {
        fontSize: 16,
        fontWeight: "500",  // Giúp chữ rõ nét hơn
        color: "#555",
        textAlign: "center",  // Đảm bảo chữ nằm giữa
    },
    selectedCategory: {
        backgroundColor: "#E96E6E",
    },

    selectedText: {
        color: "#FFF",
    },

    uploadMoreButton: {
        backgroundColor: "#E96E6E",
        padding: 10,
        marginVertical: 10,
        marginHorizontal: 10,
        borderRadius: 8,
        alignItems: "center",

    },
    imageGrid: {
        flexDirection: "row",
        flexWrap: "wrap",
        justifyContent: "center",
        margin: 10,
    },
    imageItem: {
        width: "45%",
        height: 200,
        margin: 10,
        borderRadius: 10,
    }
});


