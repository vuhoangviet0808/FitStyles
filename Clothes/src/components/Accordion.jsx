import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import React, {useState }  from "react";


const Accordion = ({ title, content }) => {
    const [expanded, setExpanded] = useState(false);
    return (
        <View style={styles.accordionContainer}>
            <TouchableOpacity onPress={() => setExpanded(!expanded)} style={styles.accordionHeader}>
                <Text style={styles.accordionTitle}>{title}</Text>
                <Text>{expanded ? "-" : ">"}</Text>
            </TouchableOpacity>
            {expanded && <Text style={styles.accordionContent}>{content}</Text>}
        </View>
    );
};

export default Accordion

const styles = StyleSheet.create({
    accordionContainer: {
        margin: 10,
        backgroundColor: "#FFF",
        borderRadius: 8,
        padding: 10
    },
    accordionHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        padding: 10
    },
    accordionTitle: {
        fontSize: 18,
        fontWeight: "bold"
    },
    accordionContent: {
        padding: 10,
        fontSize: 16,
        color: "#666"
    },
})
