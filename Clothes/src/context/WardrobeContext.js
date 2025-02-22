import React, { createContext, useContext, useState } from "react";

const WardrobeContext = createContext();

export const WardrobeProvider = ({ children }) => {
    const [images, setImages] = useState([]); // Danh sách ảnh

    const addImage = (imageUri) => {
        setImages((prevImages) => [...prevImages, imageUri]);
    };

    return (
        <WardrobeContext.Provider value={{ images, addImage }}>
            {children}
        </WardrobeContext.Provider>
    );
};

export const useWardrobe = () => useContext(WardrobeContext);
