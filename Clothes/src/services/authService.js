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
      
      const result = await response.json();
      if (response.ok) {
        return { ok: true, message: result.message, data: result.data };
    } else {
        return { ok: false, message: result.message || "Something went wrong" };
    }
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
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseText = await response.text();
      if (!responseText) {
        throw new Error("Empty response from server.");
      }
      const result = JSON.parse(responseText);

      return result;

    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
};
