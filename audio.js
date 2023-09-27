const axios = require("axios");

const voice_id = "2EiwWnXFnvU5JabPnv8n"; // Replace with the actual voice_id you want to use
const url = `https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`;

const headers = {
  Accept: "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "4041172328f2929f0137c762bf7a4c2e",
};

async function main(prompt) {
  const data = {
    text: prompt,
    model_id: "eleven_monolingual_v1",
    voice_settings: { stability: 0.5, similarity_boost: 0.5 },
  };

  axios
    .post(url, data, { headers })
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        // Assuming the API responds with audio data in binary format
        const audioData = response.data;

        // You can save the audio data to a file or process it as needed
        const fs = require("fs");
        fs.writeFileSync("output_audio.mp3", audioData, "binary");

        console.log(
          'Audio generated successfully and saved as "output_audio.mp3"'
        );
      } else {
        console.error(
          `Failed to generate audio. Status code: ${response.status}`
        );
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

module.exports = { main };
