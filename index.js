const { Client, Events, GatewayIntentBits } = require("discord.js");
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});
const { main } = require("./audio");

// Replace 'YOUR_BOT_TOKEN_HERE' with your bot's token
const BOT_TOKEN =
  "MTE1NDgxNzcwNDI1NjA4NjA3Nw.GF7MHv.M7qBUboQ8_EkpstzR8SsUmbnorFsR3yc6CAokA";

// client.once('ready', () => {
//   console.log(`Logged in as ${client.user.tag}`);
// });
client.once(Events.ClientReady, (c) => {
  console.log(`Ready! Logged in as ${c.user.tag}`);
});

client.on(Events.MessageCreate, (message) => {
  console.log("message", message);
  // Check if the message is from the channel where the webhook posts messages
  if (message.channel.id === "1154542911673860177") {
    // Handle user responses here
    main(message.content);
    console.log(
      `Received a message from ${message.author.tag}: ${message.content}`
    );
  }
});

client.login(BOT_TOKEN);
