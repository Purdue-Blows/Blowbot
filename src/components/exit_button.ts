import { ActionRowBuilder, ButtonBuilder, ButtonStyle } from "discord.js";

// Define the emoji ID or name for the closed icon
const closedIconEmoji = "🔒"; // You can use any closed icon emoji here

// Prompt user to select key(s)
export const exitButton = new ActionRowBuilder<ButtonBuilder>().addComponents(
  new ButtonBuilder()
    .setStyle(ButtonStyle.Danger) // You can set the style of the button to make it stand out
    .setLabel("Exit") // Optionally, you can add a label to the button
    .setCustomId("exit_button") // Set a custom ID for identifying the button
    .setEmoji(closedIconEmoji) // Set the emoji for the button
);
