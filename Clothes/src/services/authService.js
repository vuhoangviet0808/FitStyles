import BASE_URL from "../common/apiConfig";

export const registerUser = async (name, email, password) => {
    try {
      const response = await fetch(`${BASE_URL}/api/register`, {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });
      
      console.log("Raw response:", response);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      return await response.json();
    } catch (error) {
      console.error("Network request failed:", error.message);
      throw error;
    }
  };

export const loginUser = async (email, password) => {
    try {
        const response = await fetch(`${BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({email, password}),
        });

        return await response.json();
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
};