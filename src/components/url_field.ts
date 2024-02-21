import { ActionRowBuilder, TextInputBuilder } from "discord.js";

export const upload_comp = new TextInputBuilder()
  .setCustomId("url_input") // Unique identifier for the text input
  .setPlaceholder("Upload the link to your pdf here") // Placeholder text displayed in the input field
  .setMaxLength(500); // Maximum character length for the input

export const upload_input =
  new ActionRowBuilder<TextInputBuilder>().addComponents(upload_comp);
