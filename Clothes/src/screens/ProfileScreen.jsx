import React from "react";
import { View, Text, Image, StyleSheet, TouchableOpacity, ScrollView } from "react-native";
import Ionicons from "react-native-vector-icons/Ionicons";
import ProfileCard from "../components/ProfileCard";
import { useNavigation } from "@react-navigation/native";
import VirtualModelScreen from "./profile/VirtualModelScreen";

const ProfileScreen = () => {
    const navigation = useNavigation();
    return (
        <ScrollView style={styles.container}>
            {/* Header Section */}
            <View style={styles.headerContainer} >
                <TouchableOpacity onPress ={() => navigation.navigate("HOME")} style={styles.appIconContainer}>
                    <Ionicons name="chevron-back" size={24} color="#E96E6E" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>User Profile</Text>
            </View>

            {/* Profile Section */}
            <View style={styles.profileContainer}>
                <Image
                    source={require("../assets/dp.png")}
                    style={styles.profileImage}
                />
                <View style={styles.userInfoContainer}>
                    <Text style={styles.userName}>Phuc Ngo</Text>
                    <Text style={styles.userEmail}>example@gmail.com</Text>
                </View>
                <TouchableOpacity style={styles.editIconContainer}>
                    <Ionicons name="create-outline" size={20} color="#8B5E3C" />
                </TouchableOpacity>
            </View>

            {/* Action Items */}
            <View style={styles.actionItemsContainer}>
                {actionItems.map((item, index) => (
                    <ProfileCard key={index} className="rounded-lg mb-2">
                        <TouchableOpacity style={styles.actionItem}
                            onPress={() => {
                                if (item.label === "My Virtual Model") {
                                  navigation.navigate("VirtualModelScreen"); // Điều hướng đến trang trống
                                }
                              }}    
                        >
                            <Ionicons name={item.icon} size={24} color="#000" style={styles.actionIcon} />
                            <Text style={styles.actionText}>{item.label}</Text>
                        </TouchableOpacity>
                    </ProfileCard>
                ))}
            </View>
        </ScrollView>
    );
};

const actionItems = [
    { label: "My Orders", icon: "cart-outline" },
    { label: "My Virtual Model", icon: "person-outline" },
    { label: "Shipping Address", icon: "location-outline" },
    { label: "Payment Method", icon: "card-outline" },
    { label: "My Wardrobe", icon: "shirt-outline" },
    { label: "Log Out", icon: "log-out-outline" },
];

export default ProfileScreen;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FDF0F3',
    },
    headerContainer: {
        flexDirection: "row",
        alignItems: "center",
        padding: 16,
        backgroundColor: "#FDF0F3", 
        position: "relative",
        justifyContent: "space-between",
        
    },
    headerTitle: {
        position: "absolute",
        left: "35%",
        fontSize: 28,
        fontWeight: "300",
        color: "#000",
    },
    profileContainer: {
        flexDirection: "row",
        alignItems: "center",
        padding: 16,
        backgroundColor: "#FFF",
    },
    profileImage: {
        height: 80,
        width: 80,
        borderRadius: 40,
    },
    userInfoContainer: {
        flex: 1,
        marginLeft: 16,
    },
    userName: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#000",
    },
    userEmail: {
        fontSize: 14,
        color: "#555",
        marginTop: 4,
    },
    editIconContainer: {
        padding: 8,
        borderRadius: 8,
        backgroundColor: "#F1E4D7",
    },
    actionItemsContainer: {
        padding: 16,
    },
    actionItem: {
        flexDirection: "row",
        alignItems: "center",
        padding: 12,
    },
    actionIcon: {
        marginRight: 12,
    },
    actionText: {
        fontSize: 16,
        color: "#000",
    },
    appIconContainer:{
        backgroundColor: "#FFFFFF",
        height: 44,
        width: 44,
        borderRadius: 22,
        justifyContent: "center",
        alignItems: "center",
    },
});

