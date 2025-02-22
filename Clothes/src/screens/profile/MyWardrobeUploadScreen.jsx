import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, FlatList, Image, StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";
import * as ImagePicker from "react-native-image-picker";
import { useWardrobe } from "../../context/WardrobeContext";

const MyWardrobeUploadScreen = () => {
    const navigation = useNavigation();
    const categories = ["Shirt", "Pants", "Skirt", "Trousers", "Jackets"];
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [newCategory, setNewCategory] = useState("");
    const [images, setImages] = useState([]);

    const { addImage } = useWardrobe(); // Lấy hàm cập nhật ảnh từ context

    const pickImage = () => {
        ImagePicker.launchImageLibrary({ mediaType: "photo" }, (response) => {
            if (!response.didCancel && response.assets) {
                const newImages = response.assets.map((asset) => asset.uri);
                setImages([...images, ...newImages]); // Cập nhật state cục bộ
                newImages.forEach(addImage); // Cập nhật context ngay lập tức
            }
        });
    };


    const handleUpload = () => {
        if (images.length > 0) {
            images.forEach((image) => addImage(image)); // Thêm từng ảnh vào danh sách
            navigation.goBack(); // Quay lại màn hình trước
        } else {
            console.warn("No image selected!");
        }
    };


    return (
        <View style={styles.container}>
            <Text style={styles.title}>Upload Clothes</Text>

            <TouchableOpacity style={styles.uploadButton} onPress={pickImage}>
                <Text style={styles.uploadText}>Choose Image</Text>
            </TouchableOpacity>
            <FlatList
                data={images}
                numColumns={2}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => <Image source={{ uri: item }} style={styles.image} />}
            />
            <TouchableOpacity style={styles.saveButton} onPress={handleUpload}>
                <Text style={styles.buttonText}>Save</Text>
            </TouchableOpacity>

        </View>
    );
};

export default MyWardrobeUploadScreen;

const styles = StyleSheet.create({
    container: { flex: 1, padding: 16, backgroundColor: "#FDF0F3" },
    title: { fontSize: 24, fontWeight: "bold", textAlign: "center", marginBottom: 10 },
    categoryButton: { backgroundColor: "#EEE", padding: 10, margin: 5, borderRadius: 8 },
    selectedCategory: { backgroundColor: "#E96E6E" },
    categoryText: { color: "#555" },
    inputContainer: { flexDirection: "row", alignItems: "center", marginVertical: 10 },
    input: { flex: 1, borderWidth: 1, borderColor: "#CCC", padding: 10, borderRadius: 8 },
    addButton: { backgroundColor: "#E96E6E", padding: 10, borderRadius: 8, marginLeft: 10 },
    addButtonText: { color: "#FFF", fontSize: 18 },
    uploadButton: { backgroundColor: "#E96E6E", padding: 12, marginVertical: 10, borderRadius: 8, alignItems: "center" },
    uploadText: { color: "#FFF", fontWeight: "bold" },
    image: { width: 100, height: 100, margin: 5, borderRadius: 8 },
    saveButton: { backgroundColor: "#A36A2C", padding: 12, marginTop: 20, borderRadius: 8, alignItems: "center" },
    buttonText: { color: "#FFF", fontWeight: "bold" }
});
