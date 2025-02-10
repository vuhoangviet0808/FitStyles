import React, { useState } from "react";
import { View, Text, TouchableOpacity, Image, StyleSheet, ScrollView, FlatList } from "react-native";
import { useNavigation } from "@react-navigation/native";
import Ionicons from "react-native-vector-icons/Ionicons";
import AntDesign from 'react-native-vector-icons/AntDesign';

const MyWardrobeScreen = () => {
    const navigation = useNavigation();
    const [uploadedClothes, setUploadedClothes] = useState([]);
    const [isUploading, setIsUploading] = useState(true);

    const images = [
        require("../../assets/jacket1.png"),
        require("../../assets/pants1.png"),
        require("../../assets/pants2.png"),
        require("../../assets/shirt1.png"),
        require("../../assets/shirt2.png"),
        require("../../assets/skirt1.png"),
    ];
    return (
        // <ScrollView style={styles.container}>
        //     {/* Header */}
        //     <View style={styles.headerContainer}>
        //         <TouchableOpacity onPress={() => navigation.goBack()} style={styles.appIconContainer}>
        //             <Ionicons name="chevron-back" size={24} color="#A36A2C" />
        //         </TouchableOpacity>
        //         <Text style={styles.headerTitle}>My wardrobe</Text>
        //     </View>

        //     {/* Upload Clothes Section */}
        //     <Text style={styles.subTitle}>Upload your clothes</Text>


        //         <View style={styles.wardrobeList}>
        //             <View style={styles.categoryBar}>
        //                 <Text>Shirt: 10</Text>
        //                 <Text>Pants: 4</Text>
        //                 <Text>Skirt: 4</Text>
        //                 <Text>Trousers: 2</Text>
        //                 <Text>Jackets: 3</Text>
        //                 <TouchableOpacity style={styles.newCategoryButton}>
        //                     <Text>+ New</Text>
        //                 </TouchableOpacity>
        //             </View>
        //             <FlatList
        //                 data={images}
        //                 numColumns={2} // Chia làm 2 cột
        //                 keyExtractor={(item, index) => index.toString()}
        //                 renderItem={({ item }) => (
        //                     <Image source={item} style={styles.imageItem} />
        //                 )}
        //                 // nestedScrollEnabled={true}
        //                 keyboardShouldPersistTaps="handled"
        //             />
        //             <TouchableOpacity style={styles.uploadMoreButton}>
        //                 <Text style={styles.buttonText}>Upload more</Text>
        //             </TouchableOpacity>
        //         </View>

        // </ScrollView>
        <View style={styles.container}>
            {/* Header */}
            <View style={styles.headerContainer}>
                <TouchableOpacity onPress={() => navigation.goBack()} style={styles.appIconContainer}>
                    <Ionicons name="chevron-back" size={24} color="#A36A2C" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>My wardrobe</Text>
            </View>

            {/* Upload Clothes Section */}
            <Text style={styles.subTitle}>Upload your clothes</Text>

            <FlatList
                data={images}
                numColumns={2}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <Image source={item} style={styles.imageItem} />
                )}
                contentContainerStyle={{ paddingBottom: 80 }} // Để tránh che mất item cuối cùng
            />

            {/* Nút Upload More cố định dưới màn hình */}
            <View style={styles.uploadMoreContainer}>
                <TouchableOpacity style={styles.uploadMoreButton}>
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
        justifyContent: "center"
    },
    appIconContainer: {
        position: "absolute",
        left: 16,
        backgroundColor: "#FFF",
        padding: 8,
        borderRadius: 22
    },
    headerTitle: {
        fontSize: 24,
        fontWeight: "bold",
        color: "#A36A2C"
    },
    subTitle: {
        marginLeft: 16,
        fontSize: 16,
        fontWeight: "bold",
        color: "#A36A2C"
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
    wardrobeList: {
        padding: 16
    },
    categoryBar: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginBottom: 10
    },
    newCategoryButton: {
        backgroundColor: "#DDD",
        padding: 5,
        borderRadius: 5
    },

    uploadMoreButton: {
        backgroundColor: "#A36A2C",
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
        width: "45%",  // Điều chỉnh kích thước ảnh phù hợp
        height: 200,
        margin: 10,
        borderRadius: 10,
    }
});


