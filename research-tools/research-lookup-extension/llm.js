import { GoogleGenerativeAI } from 'https://cdn.skypack.dev/@google/generative-ai';

const API_KEY = 'AIzaSyBl56gfbyjTY5qI1mzTP9-uK_Jg7c2ckaY';

export async function runLLM(prompt) {
    const genAI = new GoogleGenerativeAI(API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

    const result = await model.generateContent(prompt);
    const text = result.response.text();
  
    return text;
}
